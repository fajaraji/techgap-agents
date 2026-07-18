# TechGap AI: Skill Gap Analyzer (Indonesian Tech Market Focus)

TechGap AI is a production-grade, multi-agent AI system designed to help tech professionals identify and close their precise skill gaps. By analyzing live market demands in Indonesia and cross-referencing them against actual, verifiable code structures on GitHub, TechGap AI provides objective, data-driven career development roadmaps and tailored project recommendations.

**Live Demo:** [techgap.streamlit.app](https://techgap.streamlit.app/)

---

## 🔬 Framework & Theoretical Foundation: `Agent = Model + Harness`

This project is built strictly upon the **Agentic Engineering** principles, realizing the industry-standard formula:
$$\text{Agent} = \text{Model} + \text{Harness}$$

Where the **Model** acts as the reasoning engine (Gemini), and the **Harness** represents the surrounding infrastructure (memory, tools, guardrails, and orchestration) that makes the agent safe, scalable, and predictable in production.

Here is how TechGap AI maps directly to the 5-step production-grade Agentic Harness framework:

### 1. Spec-Driven Development (SDD) & BDD
* **Spec Gating**: Built with a strict taxonomy file ([specs/skill_taxonomy.yaml](file:///c:/kaggle-vibecoding-aiagents-2026/specs/skill_taxonomy.yaml)) to prevent model hallucination. The parser maps unstructured job descriptions only to predefined, validated tech categories.
* **Project DNA**: Controlled by global and workspace project rules (`AGENTS.md`) ensuring that the agent remains strict, objective, and evidence-based.

### 2. Procedural Memory via Agent Skills
* Instead of stuffing all logic into a single context-rot prompt, the system's memory is divided into modular, decoupled **Agent Skills** under the `skills/` directory:
  * `job_parser.py`: Spec-driven mapping of roles and required skills.
  * `market_researcher.py`: Search-grounded live market research agent.
  * `github_auditor.py`: Git Tree structural auditing agent.
  * `gap_analyzer.py`: Objective match & personalized project recommendation generator.

### 3. Tool Interoperability & MCP
* The Harness integrates tools using the **Model Context Protocol (MCP)**, connecting the reasoning model securely to the GitHub REST API and Google Search Grounding services.

### 4. Zero-Trust Security & Policy Gating
* **Context Hygiene**: Employs a security middleware ([security_middleware.py](file:///c:/kaggle-vibecoding-aiagents-2026/security_middleware.py)) that acts as a structural policy gate. It filters and masks PII (Personally Identifiable Information) and sensitive API keys *before* the context is passed to the LLM.

### 5. Evaluation-Driven Development (EDD)
* Utilizes LLM-as-a-judge trajectory testing (`evaluation/`) to trace and measure the agent's reasoning path, self-repair behavior, and output consistency against test cases.

---

## 🌟 Key Features

### 1. Live Indonesian Tech Market Research (Search-Grounded Agent)
* Bypasses outdated or limited job APIs by utilizing **Gemini with Google Search Grounding**.
* Dynamically retrieves current, real-time job vacancies and requirements in Indonesia for any tech role typed by the user.

### 2. Scalable Git Tree API Auditing (O(1) Scalability)
* **Real-time & Reliable**: Bypasses the delayed GitHub Code Search indexing by reading repository file structures directly using the Git Tree API.
* **Concurrency (Multithreading)**: Uses `ThreadPoolExecutor` to scan the file trees of up to 100+ repositories concurrently in seconds.
* **Verifiable Evidence**: Demands hard code proof (e.g., finding `.sql` files for SQL, `terraform-gcp` directories for GCP) to prevent bio-based or README-based skill hallucinations.

---

## 📁 Repository Structure

```text
├── app.py                      # Streamlit UI & Orchestration controller
├── agents.py                   # Master multi-agent pipeline orchestrator
├── github_api.py               # GitHub REST & Tree API concurrent wrapper (with rate-limit handling)
├── mcp_server.py               # FastMCP server exposing GitHub API tools
├── security_middleware.py      # PII masking & sanitization utility
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── AGENTS.md                   # Project DNA — core constraints for all agents
├── writeup.md                  # Submission writeup / project overview
├── specs/
│   ├── skill_taxonomy.yaml     # Spec-driven taxonomy mapping (Anti-Hallucination)
│   └── indonesia_tech_jobs.json# Fallback curated Indonesian tech jobs dataset
├── skills/
│   ├── __init__.py             # Python package marker
│   ├── market_researcher.py    # Google Search Grounded Agent (with fallback)
│   ├── job_parser.py           # Taxonomy-driven JD parsing agent
│   ├── github_auditor.py       # Git Tree structural auditing agent
│   └── gap_analyzer.py         # Objective match & portfolio recommender agent
└── evaluation/
    ├── llm_judge.py            # LLM-as-a-Judge trajectory evaluator
    └── golden_dataset.json     # 5 test cases for regression testing
```

---

## 🚀 Setup & Execution

### 1. Installation
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here (Optional: Required for private repos & rate-limits)
```

### 3. Run the Application
Start the Streamlit dashboard:
```bash
streamlit run app.py
```
