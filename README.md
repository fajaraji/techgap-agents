# TechGap AI: Skill Gap Analyzer

## Overview
TechGap AI is a multi-agent system designed to help tech job seekers identify their precise skill gaps. It analyzes job descriptions against their actual, verifiable skills on GitHub.

## Architecture (Production-Grade Agentic Engineering)
1. **Spec-Driven Development**: Uses YAML taxonomy (`specs/skill_taxonomy.yaml`) to prevent hallucination.
2. **Procedural Memory (Agent Skills)**: Split into modular skills (`job_parser`, `github_auditor`, `gap_analyzer`).
3. **MCP Server Integration**: Custom FastMCP server to securely fetch GitHub repos and READMEs.
4. **Zero-Trust Security**: Includes Context Hygiene (`security_middleware.py`) to mask PII from Job Descriptions.
5. **LLMOps**: Includes an LLM-as-judge evaluation script (`evaluation/llm_judge.py`).

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   Copy `.env.example` to `.env` and fill in:
   - `GEMINI_API_KEY`
   - `GITHUB_TOKEN` (optional but recommended for rate limits / private repos)
3. Run the Streamlit UI:
   ```bash
   streamlit run app.py
   ```

## Disclaimer
DO NOT commit your `.env` file containing real API keys.
