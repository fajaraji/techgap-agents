import os
import time
import requests
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds (exponential backoff: 2, 4, 8)

def _handle_rate_limit(response) -> bool:
    """Check for rate limit and sleep if needed. Returns True if request should be retried."""
    if response.status_code == 429:
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_time - time.time(), 1) if reset_time else 60
        print(f"[WARN] GitHub API rate limit hit. Waiting {wait:.0f}s before retry...")
        time.sleep(wait)
        return True
    if response.status_code == 403 and "rate limit" in response.text.lower():
        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
        wait = max(reset_time - time.time(), 1) if reset_time else 60
        print(f"[WARN] GitHub API secondary rate limit. Waiting {wait:.0f}s...")
        time.sleep(wait)
        return True
    return False

def _make_request(url: str, headers: dict = None) -> requests.Response:
    """Make a GET request with retry logic for rate limits."""
    if headers is None:
        headers = get_headers()
    
    for attempt in range(MAX_RETRIES + 1):
        response = requests.get(url, headers=headers)
        if _handle_rate_limit(response):
            continue  # Retry after waiting
        return response
    return response  # Return last response after all retries exhausted

def get_headers():
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

def get_user_repos_raw(username: str, limit: int = 5) -> str:
    """Fetch the top updated repositories for a given GitHub username."""
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page={limit}"
    response = _make_request(url)
    
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
    
    response = _make_request(url)
    if response.status_code != 200:
        return ""  # Silently ignore if no readme
    
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
    resp = _make_request(url)
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
    resp = _make_request(repos_url)
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
