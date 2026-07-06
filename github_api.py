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
