# TechGap AI: Skill Gap Analyzer (Indonesian Tech Market Focus)

Streamlit prototype that compares Indonesian tech job requirements with GitHub repository tree evidence and generates a learning plan using Gemini.

**Live Demo:** [techgap.streamlit.app](https://techgap.streamlit.app/)

---

## Explore the implementation

The auditor uses file paths as signals when matching a job requirement. Read its prompt alongside the evaluation dataset to understand how tentative a recommendation can be.

- [Extract job requirements](skills/job_parser.py)
- [Match requirements to repository paths](skills/github_auditor.py)
- [Evaluation examples](evaluation/golden_dataset.json)

## Try a comparison

1. Open the Streamlit app and paste a job description or search for a role in the Indonesian market.
2. Enter a GitHub username. The auditor fetches public repository trees and compares their paths with the extracted requirements.
3. Inspect the cited paths before using the suggested learning plan. A SQL file is a lead for a code review. Its filename alone cannot establish the complexity of the work or who wrote it.

## Run locally

Install the dependencies and set `GEMINI_API_KEY` in a local `.env`. An optional `GITHUB_TOKEN` raises the authenticated API allowance. The auditor lists up to 100 public repositories per user request.

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Evaluate changes

Inspect the [golden dataset](evaluation/golden_dataset.json) and [judge implementation](evaluation/llm_judge.py) alongside the [skill taxonomy](specs/skill_taxonomy.yaml) when changing the matching rules.
