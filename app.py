import streamlit as st
import plotly.graph_objects as go
from agents import run_techgap_pipeline

st.set_page_config(page_title="TechGap AI", layout="wide")

st.title("TechGap AI — Skill Gap Analyzer")
st.markdown("Analisis lowongan kerja, bandingkan dengan bukti di GitHub Anda, dan temukan *skill gap* berbasis data.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Masukkan Detail Anda")
    github_user = st.text_input("GitHub Username", placeholder="e.g., octocat")
    gemini_key = st.text_input("Gemini API Key (opsional jika sudah ada di .env)", type="password")
    
    st.subheader("2. Masukkan Deskripsi Lowongan (Job Description)")
    jd_text = st.text_area("Paste teks lowongan pekerjaan di sini", height=200, placeholder="Requirements: Python, Docker, AWS, React...")
    
    analyze_btn = st.button("Analisis Skill Gap", type="primary")

if analyze_btn:
    if not github_user or not jd_text:
        st.error("Mohon isi GitHub Username dan Job Description.")
    else:
        with st.spinner("Agen sedang bekerja: Parsing JD, Audit GitHub, dan Menganalisis Gap..."):
            result = run_techgap_pipeline(jd_text, github_user, gemini_key)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Analisis selesai!")
                
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
                    st.subheader("Visualisasi Skill Gap (Radar)")
                    if len(all_skills) > 1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatterpolar(
                            r=market_values,
                            theta=all_skills,
                            fill='toself',
                            name='Kebutuhan Pasar (Must-Have)',
                            line_color='red'
                        ))
                        fig.add_trace(go.Scatterpolar(
                            r=user_values,
                            theta=all_skills,
                            fill='toself',
                            name='Skill Anda (Verified)',
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
                        st.info("Data skill tidak cukup untuk menampilkan grafik radar.")

                st.subheader("Rekomendasi Portofolio & Analisis Detail")
                st.markdown(gap_report)
                
                with st.expander("Lihat Bukti Audit GitHub Mentah"):
                    st.json(github_audit)
