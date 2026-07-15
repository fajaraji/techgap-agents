import os
from google import genai
from google.genai import types

def fetch_live_market_demand(api_key: str, role_name: str) -> str:
    """
    Uses Gemini with Google Search Grounding to fetch current, live job requirements 
    for a specific role in Indonesia.
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
        print(f"Error in market_researcher: {e}")
        return f"ERROR: Failed to fetch market demand via Google Search. Details: {e}"
