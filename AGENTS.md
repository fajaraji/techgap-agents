# Project DNA: TechGap AI
This is the core instruction guide that applies to all agents (Parser, Auditor, and Analyzer) to prevent hallucinations and ensure safe Agentic Engineering behavior.

## 1. Anti-Hallucination Policy (Strict Evidence-Based)
- **DO NOT** conclude that a user has a specific skill (e.g., "Proficient in Python") ONLY from their profile bio or brief repository description.
- Agents (specifically `skill-github-auditor`) **MUST** look into file structures, read `requirements.txt`, `package.json`, or relevant actual code content to validate the existence of that skill.
- If there is no verifiable evidence in the repository, the agent MUST honestly mark that skill as `[NOT ACQUIRED]`.

## 2. Memory & Specification Usage (Spec-Driven)
- Agents must always refer to the `specs/skill_taxonomy.yaml` file when attempting to categorize skills from a Job Description (JD).
- If a skill in the JD does not exactly exist in the YAML, the agent must map it to the closest technical category.

## 3. Context Hygiene & Privacy
- Never leak `GITHUB_TOKEN` or `GEMINI_API_KEY` to console output or logs.
- Before processing a user's GitHub profile or CV (if applicable), mask PII such as user emails, phone numbers, or API tokens that were accidentally committed in the repo.

## 4. Objective Reporting
- Portfolio project recommendations at the end of the process MUST be specific and directly target the identified gaps.
- *Bad Example*: "Build a project using Python."
- *Good Example*: "Based on the gap we found (lack of API Design experience), build a simple RESTful API project using FastAPI (Python) that performs CRUD operations on a SQLite database."
