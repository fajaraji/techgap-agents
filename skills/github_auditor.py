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
    Audits a GitHub profile and returns verified skills.
    """
    try:
        repos_info = github_api.get_user_repos_raw(username)
    except Exception as e:
        return {"error": str(e)}

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert Technical Assessor (GitHub Auditor).
    Your job is to strictly verify if the user possesses the following required skills: {required_skills}
    
    You MUST adhere to the Anti-Hallucination policy: Only verify a skill if there is concrete evidence in the provided GitHub data.
    
    Here is the user's GitHub public repository information:
    {repos_info}
    
    Respond ONLY with a valid JSON in this exact format:
    {{
        "verified_skills": [
            {{"skill": "Python", "evidence": "Used in repo X as main language"}}
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
