import json
from google import genai

def analyze_gap(api_key: str, job_analysis: dict, github_audit: dict) -> str:
    """
    Analyzes the gap between required skills and verified skills.
    Returns a markdown report.
    """
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert Career Coach and Gap Analyzer.
    
    Job Requirements:
    {json.dumps(job_analysis)}
    
    User's Verified GitHub Skills:
    {json.dumps(github_audit)}
    
    Compare the two. Generate a professional and constructive report in Markdown format.
    The report should include:
    1. **Summary of Match**: How well does the user fit the role?
    2. **Strengths**: Skills they have that match the requirements.
    3. **Skill Gaps**: Crucial missing skills (Must-Haves that are missing).
    4. **Actionable Recommendations**: Suggest 1-2 highly specific portfolio projects they can build to close the gap. Be detailed.
    
    Format the output elegantly with Markdown.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error in gap_analyzer: {e}")
        return f"Error generating gap analysis: {e}"
