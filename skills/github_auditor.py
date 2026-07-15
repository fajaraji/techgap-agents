import json
from google import genai
from google.genai import types
import sys
import os

# Ensure github_api can be imported from root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import github_api

def audit_github_profile(api_key: str, username: str, required_skills: list) -> dict:
    """
    Audits a GitHub profile and returns verified skills using Tree API for 100% accurate file-level evidence.
    """
    try:
        repos_info = github_api.get_all_repos_trees(username)
    except Exception as e:
        return {"error": f"Error running tree fetch: {str(e)}"}

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert Technical Assessor (GitHub Auditor).
    Your job is to strictly verify if the user possesses the following required skills: {required_skills}
    
    You MUST adhere to the Anti-Hallucination policy: Only verify a skill if there is concrete evidence in the provided directory tree paths.
    
    Here is the complete file directory tree for all of the user's GitHub repositories:
    {repos_info}
    
    Look for evidence in file names, extensions, and folder paths (e.g., .sql files indicate SQL, main.tf or folders containing 'gcp' indicate GCP, .py indicates Python).
    
    Respond ONLY with a valid JSON in this exact format:
    {{
        "verified_skills": [
            {{"skill": "GCP", "evidence": "Found in terraform-gcp folder inside de-zoomcamp repo"}}
        ],
        "missing_skills": ["Docker", "Kubernetes"]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error in github_auditor: {e}")
        return {"error": str(e)}
