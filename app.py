import streamlit as st
import plotly.graph_objects as go
from agents import run_techgap_pipeline

st.set_page_config(page_title="TechGap AI", layout="wide")

st.title("TechGap AI — Skill Gap Analyzer")
st.markdown("Analyze job postings, cross-reference with your verifiable GitHub evidence, and discover your data-driven skill gaps.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Enter Your Details")
    github_user = st.text_input("GitHub Username", placeholder="e.g., octocat")
    gemini_key = st.text_input("Gemini API Key (optional if set in .env)", type="password")
    
    st.subheader("2. Enter Job Description")
    jd_text = st.text_area("Paste the job description text here", height=200, placeholder="Requirements: Python, Docker, AWS, React...")
    
    analyze_btn = st.button("Analyze Skill Gap", type="primary")

if analyze_btn:
    if not github_user or not jd_text:
        st.error("Please fill in both the GitHub Username and Job Description.")
    else:
        with st.spinner("Agents are working: Parsing JD, Auditing GitHub, and Analyzing Gaps..."):
            result = run_techgap_pipeline(jd_text, github_user, gemini_key)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Analysis complete!")
                
                job_analysis = result.get("job_analysis", {})
                github_audit = result.get("github_audit", {})
                gap_report = result.get("gap_report", "")
                
                # --- Prepare Data for Radar Chart ---
                must_haves = job_analysis.get("must_have", [])
                
                # Extract skill names from verified_skills (which is a list of dicts)
                verified_dicts = github_audit.get("verified_skills", [])
                verified_skills = [s.get("skill", "") for s in verified_dicts if isinstance(s, dict)]
                # Handle case where LLM returns just strings directly in worst case
                verified_skills = [s if isinstance(s, str) else s.get("skill", "") for s in verified_dicts]
                
                missing_skills = github_audit.get("missing_skills", [])
                
                # All skills for axes
                all_skills = list(set(must_haves + verified_skills + missing_skills))
                
                # Default all to 0, then map values
                market_values = []
                user_values = []
                
                for skill in all_skills:
                    market_values.append(1 if skill in must_haves else 0)
                    user_values.append(1 if skill in verified_skills else 0)
                
                # Close the radar chart loop
                if all_skills:
                    all_skills.append(all_skills[0])
                    market_values.append(market_values[0])
                    user_values.append(user_values[0])

                with col2:
                    st.subheader("Skill Gap Visualization (Radar Chart)")
                    if len(all_skills) > 1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatterpolar(
                            r=market_values,
                            theta=all_skills,
                            fill='toself',
                            name='Market Requirements (Must-Have)',
                            line_color='red'
                        ))
                        fig.add_trace(go.Scatterpolar(
                            r=user_values,
                            theta=all_skills,
                            fill='toself',
                            name='Your Skills (Verified)',
                            line_color='blue'
                        ))
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(visible=True, range=[0, 1])
                            ),
                            showlegend=True
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough skill data to display the radar chart.")

                st.subheader("Portfolio Recommendations & Detailed Analysis")
                st.markdown(gap_report)
                
                with st.expander("View Raw GitHub Audit Evidence"):
                    st.json(github_audit)
