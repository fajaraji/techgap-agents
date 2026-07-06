import json
import yaml
from google import genai
from google.genai import types

def parse_job_description(api_key: str, jd_text: str) -> dict:
    """
    Parses a job description and extracts skills based on the taxonomy.
    """
    try:
        with open("specs/skill_taxonomy.yaml", "r") as f:
            taxonomy = yaml.safe_load(f)
    except Exception as e:
        taxonomy = "Taxonomy not found."

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert tech recruiter and Job Analyzer.
    Here is a Job Description:
    {jd_text}
    
    Here is the official skill taxonomy:
    {json.dumps(taxonomy)}
    
    Analyze the JD and extract the required skills. Categorize them into 'must_have' and 'nice_to_have'.
    Map the skills to the closest ones in the official taxonomy where possible.
    Respond ONLY with a valid JSON in this exact format:
    {{
        "role_title": "String",
        "must_have": ["Skill 1", "Skill 2"],
        "nice_to_have": ["Skill 3"]
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
        print(f"Error in job_parser: {e}")
        return {"error": str(e)}
