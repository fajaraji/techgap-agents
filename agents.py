import os
from dotenv import load_dotenv
from security_middleware import sanitize_pii
from skills.job_parser import parse_job_description
from skills.github_auditor import audit_github_profile
from skills.gap_analyzer import analyze_gap

load_dotenv()

def run_techgap_pipeline(job_description: str, github_username: str, gemini_api_key: str = None):
    # Allow passing API key or fallback to env var
    api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not found."}
        
    print("Sanitizing Job Description...")
    safe_jd = sanitize_pii(job_description)
    
    print("Agent 1: Job Parser running...")
    job_analysis = parse_job_description(api_key, safe_jd)
    if "error" in job_analysis:
        return {"error": f"Job Parser Error: {job_analysis.get('error')}"}
        
    required_skills = job_analysis.get("must_have", []) + job_analysis.get("nice_to_have", [])
    
    print("Agent 2: GitHub Auditor running...")
    github_audit = audit_github_profile(api_key, github_username, required_skills)
    if "error" in github_audit:
        return {"error": f"GitHub Auditor Error: {github_audit.get('error')}"}
        
    print("Agent 3: Gap Analyzer running...")
    gap_report = analyze_gap(api_key, job_analysis, github_audit)
    
    return {
        "job_analysis": job_analysis,
        "github_audit": github_audit,
        "gap_report": gap_report
    }
