# TechGap AI: Skill Gap Analyzer (Indonesian Tech Market Focus)

TechGap AI is a production-grade, multi-agent AI system designed to help tech professionals identify and close their precise skill gaps. By analyzing live market demands in Indonesia and cross-referencing them against actual, verifiable code structures on GitHub, TechGap AI provides objective, data-driven career development roadmaps and tailored project recommendations.

---

## 🌟 Key Features

### 1. Live Indonesian Tech Market Research (Search-Grounded Agent)
* Bypasses outdated or limited job APIs by utilizing **Gemini with Google Search Grounding**.
* Dynamically retrieves current, real-time job vacancies and requirements in Indonesia for any tech role typed by the user.
* Consolidation and synthesis of actual requirements without scraping violations.

### 2. Zero-Trust Security (PII Sanitization)
* Includes a robust security middleware ([security_middleware.py](file:///c:/kaggle-vibecoding-aiagents-2026/security_middleware.py)) that automatically masks Personally Identifiable Information (PII) like emails, phone numbers, and API tokens from job descriptions before sending them to the LLM.

### 3. Scalable Git Tree API Auditing
* **Real-time & Reliable**: Bypasses the delayed GitHub Code Search indexing by reading repository file structures directly using the Git Tree API.
* **Concurrency (Multithreading)**: Uses `ThreadPoolExecutor` to scan the file trees of up to 100+ repositories concurrently in seconds.
* **Verifiable Evidence**: Demands hard code proof (e.g., finding `.sql` files for SQL, `terraform-gcp` directories for GCP) to prevent bio-based or README-based skill hallucinations.

### 4. Interactive Gap Analysis & Visualization
* Compares parsed job requirements against verified GitHub evidence.
* Renders an interactive bar chart of acquired vs. missing skills.
* Suggests custom, highly specific portfolio projects on missing skills to help users bridge the gap.

---

## 📁 Repository Structure

```text
├── app.py                      # Streamlit UI & Orchestration controller
├── agents.py                   # Master multi-agent pipeline orchestrator
├── github_api.py               # GitHub REST & Tree API concurrent wrapper
├── security_middleware.py      # PII masking & sanitization utility
├── specs/
│   └── skill_taxonomy.yaml     # Spec-driven taxonomy mapping (Anti-Hallucination)
│   └── indonesia_tech_jobs.json# Fallback curated Indonesian tech jobs dataset
└── skills/
    ├── market_researcher.py    # Google Search Grounded Agent
    ├── job_parser.py           # Taxonomy-driven JD parsing agent
    ├── github_auditor.py       # Git Tree structural auditing agent
    └── gap_analyzer.py         # Objective match & portfolio recommender agent
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

---

## 🛡️ DNA Proyek (Core Constraints)
* **Evidence-Based only**: Skills are marked as `[Acquired]` ONLY if there is folder/file structural evidence in the repository. BIO descriptions are ignored to prevent skill inflation.
* **O(1) Repository Scalability**: Avoids fetching entire repository contents or sequential file downloads by performing concurrent REST API Tree scans globally.
* **Context Hygiene**: Absolute masking of API keys and PII to prevent context leaks.
