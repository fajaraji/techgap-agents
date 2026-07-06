import streamlit as st
import plotly.express as px
import pandas as pd
from agents import run_techgap_pipeline
from github_api import search_jobs_adzuna_raw

st.set_page_config(page_title="TechGap AI", layout="wide")

st.title("TechGap AI — Skill Gap Analyzer")
st.markdown("Analyze job postings, cross-reference with your verifiable GitHub evidence, and discover your data-driven skill gaps.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Enter Your Details")
    github_user = st.text_input("GitHub Username", placeholder="e.g., octocat")
    
    st.subheader("2. Job Analysis Source")
    tab1, tab2 = st.tabs(["Market Search (Adzuna)", "Manual JD Paste"])
    
    with tab1:
        st.markdown("Search active job postings to analyze market demand.")
        job_title = st.text_input("Job Title", placeholder="e.g., Data Engineer")
        job_location = st.text_input("Location Code (e.g., us, gb, sg, au)", value="sg")
        adzuna_btn = st.button("Analyze Market Demand", type="primary")
        
    with tab2:
        st.markdown("Paste a specific job description.")
        manual_jd = st.text_area("Paste the job description text here", height=200, placeholder="Requirements: Python, Docker, AWS, React...")
        manual_btn = st.button("Analyze Specific JD", type="primary")

analyze_clicked = False
jd_text_to_analyze = ""

if adzuna_btn:
    if not github_user or not job_title:
        st.error("Please fill in GitHub Username and Job Title.")
    else:
        with st.spinner(f"Fetching live job postings for '{job_title}' from Adzuna..."):
            jd_text_to_analyze = search_jobs_adzuna_raw(job_title, job_location, limit=5)
            if jd_text_to_analyze.startswith("ERROR") or jd_text_to_analyze.startswith("No jobs"):
                st.error(jd_text_to_analyze)
            else:
                st.success("Successfully fetched market data!")
                analyze_clicked = True

if manual_btn:
    if not github_user or not manual_jd:
        st.error("Please fill in GitHub Username and Job Description.")
    else:
        jd_text_to_analyze = manual_jd
        analyze_clicked = True

if analyze_clicked and jd_text_to_analyze:
    with st.spinner("Agents are working: Parsing JD, Auditing GitHub (Reading READMEs), and Analyzing Gaps..."):
        # Note: API key is handled by the agent orchestrator via .env
        result = run_techgap_pipeline(jd_text_to_analyze, github_user)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Analysis complete!")
            
            job_analysis = result.get("job_analysis", {})
            github_audit = result.get("github_audit", {})
            gap_report = result.get("gap_report", "")
            
            must_haves = job_analysis.get("must_have", [])
            
            verified_dicts = github_audit.get("verified_skills", [])
            verified_skills = [s.get("skill", "") for s in verified_dicts if isinstance(s, dict)]
            verified_skills = [s if isinstance(s, str) else s.get("skill", "") for s in verified_dicts]
            
            missing_skills = github_audit.get("missing_skills", [])
            
            all_skills = list(set(must_haves + verified_skills + missing_skills))
            
            # Prepare DataFrame for Bar Chart
            data = []
            for skill in all_skills:
                is_required = 1 if skill in must_haves else 0.5 # 0.5 for nice-to-have visual
                
                status = "Acquired" if skill in verified_skills else "Gap (Missing)"
                if skill not in must_haves and skill not in missing_skills:
                    status = "Nice-to-have / Extra"
                
                data.append({
                    "Skill": skill,
                    "Requirement Level": is_required,
                    "Status": status
                })
            
            df = pd.DataFrame(data)

            with col2:
                st.subheader("Skill Gap Visualization (Bar Chart)")
                if not df.empty:
                    df = df.sort_values(by=["Status", "Requirement Level"], ascending=[True, False])
                    
                    color_discrete_map = {
                        "Acquired": "#2ECC71", # Green
                        "Gap (Missing)": "#E74C3C", # Red
                        "Nice-to-have / Extra": "#95A5A6" # Grey
                    }
                    
                    fig = px.bar(
                        df, 
                        x="Skill", 
                        y="Requirement Level", 
                        color="Status",
                        color_discrete_map=color_discrete_map,
                        title="Your Skills vs Market Demand",
                    )
                    
                    fig.update_yaxes(tickvals=[0, 0.5, 1], ticktext=["", "Nice-to-have", "Must-have"])
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough skill data to display the chart.")

            st.subheader("Portfolio Recommendations & Detailed Analysis")
            st.markdown(gap_report)
            
            with st.expander("View Raw GitHub Audit Evidence"):
                st.json(github_audit)
