import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

def get_user_repos_raw(username: str, limit: int = 5) -> str:
    """Fetch the top updated repositories for a given GitHub username."""
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page={limit}"
    response = requests.get(url, headers=get_headers())
    
    if response.status_code != 200:
        return f"Error fetching repos for {username}: {response.text}"
    
    repos = response.json()
    repo_info = []
    for r in repos:
        repo_info.append(f"- Name: {r.get('name')}, Language: {r.get('language')}, URL: {r.get('html_url')}, Description: {r.get('description')}")
        
    return "\n".join(repo_info) if repo_info else "No public repositories found."

def get_repo_readme_raw(username: str, repo_name: str) -> str:
    """Fetch the contents of the README.md file for a specific repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "" # Silently ignore if no readme
    
    import base64
    content_b64 = response.json().get("content", "")
    try:
        content = base64.b64decode(content_b64).decode('utf-8')
        if len(content) > 3000:
            content = content[:3000] + "\n...[TRUNCATED]"
        return content
    except Exception as e:
        return ""

def search_jobs_adzuna_raw(job_title: str, location: str = "us", limit: int = 5) -> str:
    """Search for job descriptions using the Adzuna API, with a fallback to Remotive API."""
    supported_countries = ["at", "au", "be", "br", "ca", "ch", "de", "es", "fr", "gb", "in", "it", "mx", "nl", "nz", "pl", "sg", "us", "za"]
    
    if location.lower() not in supported_countries:
        # Fallback to Remotive API for unsupported countries (searches global remote jobs)
        url = f"https://remotive.com/api/remote-jobs?search={job_title}&limit={limit}"
        response = requests.get(url)
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])[:limit]
            if not jobs:
                return f"No jobs found for '{job_title}' via Global Fallback API."
            compiled_jd = []
            for job in jobs:
                title = job.get("title", "")
                company = job.get("company_name", "Unknown Company")
                import re
                description = re.sub('<[^<]+>', '', job.get("description", ""))
                compiled_jd.append(f"Title: {title}\nCompany: {company}\nDescription: {description[:1500]}...\n")
            return "\n---\n".join(compiled_jd)
        return f"ERROR: Location '{location}' not supported by Adzuna, and Fallback API failed."

    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
    
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return "ERROR: Adzuna API credentials not found in .env"
        
    url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": limit,
        "what": job_title
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"ERROR fetching jobs from Adzuna: {response.text}"
        
    results = response.json().get("results", [])
    if not results:
        return f"No jobs found for {job_title} in {location}."
        
    compiled_jd = []
    for job in results:
        title = job.get("title", "")
        company = job.get("company", {}).get("display_name", "Unknown Company")
        description = job.get("description", "")
        compiled_jd.append(f"Title: {title}\nCompany: {company}\nDescription: {description}\n")
        
    return "\n---\n".join(compiled_jd)
