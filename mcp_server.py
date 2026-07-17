import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from github_api import get_user_repos_raw, get_repo_readme_raw

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("TechGap_GitHub_MCP")

@mcp.tool()
def get_user_repos(username: str, limit: int = 5) -> str:
    """Fetch the top updated repositories for a given GitHub username."""
    return get_user_repos_raw(username, limit)

@mcp.tool()
def get_repo_readme(username: str, repo_name: str) -> str:
    """Fetch the contents of the README.md file for a specific repository."""
    return get_repo_readme_raw(username, repo_name)

if __name__ == "__main__":
    # Start the standard input/output server loop
    mcp.run()
