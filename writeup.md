# TechGap AI: The Data-Driven Skill Gap Analyzer

**Track:** Agents for Good / Freestyle

## The Problem
Tech job seekers often apply to countless roles but fail the initial screening without knowing exactly why. Current market tools (like Jobscan) operate on a 1-to-1 matching basis (1 CV to 1 Job Description), which is slow and only valid for one specific posting. Furthermore, they rely on self-reported claims in a CV rather than verifiable skills.

## The Solution
TechGap AI is a multi-agent system that analyzes job descriptions to find market patterns and cross-references them with the user's *actual* verifiable skills on GitHub. It generates a precise, data-driven skill gap map and recommends highly specific portfolio projects.

## Architecture
We utilized the following tools covered in the course:
1. **Multi-Agent System (ADK)**: Built with `google-genai`, splitting logic into `job_parser`, `github_auditor`, and `gap_analyzer` skills to prevent context rot.
2. **MCP Server**: A custom `FastMCP` server acts as the secure interface to GitHub API, reading repositories and READMEs.
3. **Security Features**: Implemented a `security_middleware.py` that strips PII (Emails, Phone numbers) before passing data to the LLM (Context Hygiene).
4. **Deployability & UI**: An interactive Streamlit frontend with Plotly radar charts, easily deployable to any cloud host.
5. **LLM Evaluation**: Maintained a Golden Dataset to automatically grade the agent's performance.

## Future Work
In future iterations, we plan to implement a Chrome Extension that automatically scrapes job descriptions while the user browses job boards, feeding directly into the TechGap AI via an MCP endpoint.
