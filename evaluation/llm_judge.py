import json
import os
import sys
from dotenv import load_dotenv
from google import genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents import run_techgap_pipeline

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def evaluate_agent():
    with open("evaluation/golden_dataset.json", "r") as f:
        dataset = json.load(f)
        
    client = genai.Client(api_key=API_KEY)
    
    for case in dataset["test_cases"]:
        print(f"Running TC: {case['id']}...")
        result = run_techgap_pipeline(case["job_description"], case["github_username"], API_KEY)
        
        if "error" in result:
            print(f"Failed to run agent: {result['error']}")
            continue
            
        missing_skills_predicted = result["github_audit"].get("missing_skills", [])
        
        # LLM as Judge Prompt
        prompt = f"""
        You are an LLM Judge evaluating an AI Agent.
        The Golden (Expected) Missing Skills: {case['expected_missing_skills']}
        The Agent's Predicted Missing Skills: {missing_skills_predicted}
        
        Did the agent correctly identify the missing skills? Respond with 'PASS' or 'FAIL' and a brief reason.
        """
        
        judge_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        print(f"Verdict for {case['id']}:\n{judge_response.text}\n---")

if __name__ == "__main__":
    evaluate_agent()
