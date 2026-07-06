import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize FastMCP server
mcp = FastMCP("TechGap_GitHub_MCP")

def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

@mcp.tool()
def get_user_repos(username: str, limit: int = 5) -> str:
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

@mcp.tool()
def get_repo_readme(username: str, repo_name: str) -> str:
    """Fetch the contents of the README.md file for a specific repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    headers = get_headers()
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Error fetching README for {username}/{repo_name} (Might not exist or is empty)."
    
    import base64
    content_b64 = response.json().get("content", "")
    try:
        content = base64.b64decode(content_b64).decode('utf-8')
        # Simple truncation if README is extremely long
        if len(content) > 5000:
            content = content[:5000] + "\n...[TRUNCATED]"
        return content
    except Exception as e:
        return f"Error decoding README: {e}"

if __name__ == "__main__":
    # Start the standard input/output server loop
    mcp.run()
