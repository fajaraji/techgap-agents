import os
import json
from google import genai
from google.genai import types

FALLBACK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "specs", "indonesia_tech_jobs.json")

def _load_fallback_dataset() -> list:
    """Load the curated fallback Indonesian tech jobs dataset."""
    try:
        with open(FALLBACK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _match_fallback(role_name: str) -> str:
    """Try to find a matching role in the fallback dataset."""
    dataset = _load_fallback_dataset()
    role_lower = role_name.lower()
    for entry in dataset:
        if role_lower in entry.get("role", "").lower():
            return entry.get("description", "")
    return ""

def fetch_live_market_demand(api_key: str, role_name: str) -> str:
    """
    Uses Gemini with Google Search Grounding to fetch current, live job requirements 
    for a specific role in Indonesia. Falls back to curated dataset on failure.
    """
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert tech recruiter and market researcher in Indonesia.
    Please search the web for current, active job vacancies and industry requirements 
    for the role of '{role_name}' in Indonesia over the last few months.
    
    Synthesize a comprehensive and realistic Job Description based on the real companies 
    currently hiring in Indonesia. Include:
    1. A brief summary of the role.
    2. Must-Have technical skills (programming languages, frameworks, cloud providers, tools).
    3. Nice-to-Have technical skills.
    4. Expected years of experience and soft skills.
    
    Make it highly detailed and technical so that a parser can extract the exact skills required.
    Do not mention that you searched the web, just output the Job Description.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}],
            )
        )
        return response.text
    except Exception as e:
        print(f"Google Search Grounding failed: {e}. Trying fallback dataset...")
        fallback_jd = _match_fallback(role_name)
        if fallback_jd:
            print(f"Using fallback dataset for role: {role_name}")
            return fallback_jd
        return f"ERROR: Failed to fetch market demand via Google Search and no fallback data available for '{role_name}'. Details: {e}"

