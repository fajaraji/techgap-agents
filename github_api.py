import os
import requests
import urllib.parse
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

def fetch_repo_tree(username: str, repo_name: str, default_branch: str) -> str:
    """Fetches the entire file tree for a single repository."""
    url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/{default_branch}?recursive=1"
    resp = requests.get(url, headers=get_headers())
    if resp.status_code == 200:
        tree = resp.json().get("tree", [])
        # We only care about files (blobs), ignore directories (trees) to save space
        paths = [item["path"] for item in tree if item["type"] == "blob"]
        
        # Limit to prevent context window bloat for massive repos
        if len(paths) > 500:
            paths = paths[:500] + ["...[TRUNCATED]"]
            
        if paths:
            return f"\n--- Repo: {repo_name} ---\n" + "\n".join(paths)
    return ""

def get_all_repos_trees(username: str) -> str:
    """Fetch the directory trees for all repositories concurrently."""
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    resp = requests.get(repos_url, headers=get_headers())
    if resp.status_code != 200:
        return f"Error fetching repos: {resp.status_code}"
    
    repos = resp.json()
    if not repos:
        return "No repositories found."
        
    repo_details = [(r.get("name"), r.get("default_branch", "main")) for r in repos if isinstance(r, dict)]
    
    from concurrent.futures import ThreadPoolExecutor
    trees_info = []
    
    # Concurrently fetch the tree for every repository
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_repo_tree, username, name, branch) for name, branch in repo_details]
        for future in futures:
            res = future.result()
            if res:
                trees_info.append(res)
                
    return "".join(trees_info)
