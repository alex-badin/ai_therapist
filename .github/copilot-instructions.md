# Copilot Instructions

These notes summarize the AI Therapist project so that future contributors (human or AI) can work efficiently and safely.

## Project Overview
- **Purpose:** Educational demo of a multi-agent therapeutic assistant in Russian, not for real clinical use.
- **Core Tech:** LangGraph workflow orchestrating LiteLLM-backed LangChain agents, Streamlit UI, Rich-based CLI, SQLite persistence.
- **Therapeutic Modes:** Router selects between DBT, IFS, TRE specialists; Memory agent extracts insights. Prompts are written in Russian and must remain unchanged unless explicitly requested.

## Processing Flow
```
User Input → Router Agent → [DBT Specialist | IFS Specialist | TRE Specialist] → Memory Agent → Response + Insights
```
The router interprets each turn, forwards it to the chosen specialist, and the memory agent appends insights before the reply is sent back.

## Repository Structure
```
ai_therapist/
├── agents/
│   ├── prompts.py        # All static prompt strings (Russian)
│   ├── base.py           # TypedDict `TherapyState`
│   └── specialists.py    # Router, DBT, IFS, TRE, Memory agents
├── core/
│   ├── graph.py          # LangGraph `TherapyGraph`
│   ├── orchestrator.py   # Session management facade
│   └── storage.py        # SQLite `MemoryStorage`
├── app.py                # Streamlit UX (chat-style)
├── main.py               # Rich CLI experience
├── config.py             # Loads `.env`, defines `LITELLM_CONFIG`, DB path
├── requirements.txt      # Runtime dependencies
├── .env.example          # Provider-specific env vars
└── therapy-agents-python.py  # Original monolithic reference file
```

## Core Components
- `agents/specialists.py:RouterAgent` — Parses the latest user turn, calls the LLM router prompt, and stamps `current_approach`, confidence, and reasoning.
- `agents/specialists.py:{DBTAgent, IFSAgent, TREAgent}` — Deliver short therapeutic replies tailored to their modality while persisting the response in state.
- `agents/specialists.py:MemoryAgent` — Summarizes the exchange into structured insights (patterns, triggers, resources) for persistence.
- `agents/prompts.py` — Houses all Russian-language system prompts; treat them as canonical.
- `core/graph.py:TherapyGraph` — Builds the LangGraph workflow, links router → specialists → memory, and manages message history updates.
- `core/orchestrator.py:TherapyOrchestrator` — Session facade used by CLI/Streamlit; coordinates state, storage, and graph execution.
- `core/storage.py:MemoryStorage` — Lightweight SQLite layer for sessions, transcripts, and insights.
- `main.py` — Rich-driven CLI, including insight table rendering.
- `app.py` — Streamlit chat UI with stats, insight refresh, and export button.

## Routing Heuristics
- **DBT** when the user references intense emotions, distress tolerance, crisis language, or interpersonal conflicts.
- **IFS** for inner-part narratives ("часть меня..."), self-criticism, protective mechanisms, or childhood patterns.
- **TRE** when bodily sensations, muscle tension, somatic stress, or physical grounding requests dominate the message.

## Environment & Tooling
- Preferred Python version: **3.12** (virtual environment in `.venv/` created via `uv venv`).
- Install deps inside the venv with `uv pip install -r requirements.txt` (already run once).
- Activate venv before running scripts: `source .venv/bin/activate`.
- No linters/tests are configured yet; add them if needed (e.g., Ruff, Pytest).

## Running the Project
```bash
# CLI (uses Rich)
uv run main.py

# Streamlit app (local web UI)
uv run streamlit run app.py
```
Both interfaces use `TherapyOrchestrator` for routing, memory persistence, and insight extraction.

## Configuration & Secrets
- Copy `.env.example` to `.env`; supply the appropriate API key(s) for the chosen model/provider.
- `config.py` reads `MODEL` and other provider keys via `python-dotenv` and sets LiteLLM defaults (`temperature=0.7`, `max_tokens=500`).
- SQLite DB file (`therapy_sessions.db`) stores session transcripts & insights; it’s ignored by Git.

## Coding Guidelines
- **Prompts are canonical:** avoid editing texts in `agents/prompts.py` unless the change is explicitly requested.
- Maintain Russian language for user-facing strings and prompts.
- Respect the `TherapyState` schema; when extending it, update all nodes that depend on new keys.
- If modifying conversation flows, ensure `TherapyGraph.route_to_specialist` returns valid node names and that each specialist pushes `specialist_response` into the state.
- Add database migrations carefully—`MemoryStorage` currently initializes schemas automatically.
- Keep Streamlit session state keys stable (`orchestrator`, `session_id`, `messages`).

## Extending the System
- **New specialists:** create prompt + subclass in `agents/specialists.py`, add node & routing in `core/graph.py`.
- **Additional memory insights:** adjust `MemoryAgent.extract` and storage insert loops in `core/storage.py`.
- **Alternate persistence:** replace or extend `MemoryStorage`; ensure orchestrator gracefully handles missing storage.
- **Analytics/UI tweaks:** update Streamlit columns or CLI panels; ensure metadata (approach, confidence, reasoning) remains synchronized with state.

## Known Limitations / TODOs
- No automated tests—consider adding unit tests around `TherapyGraph` and storage layer.
- Error handling is minimal; LLM failures print to stdout and return fallback messages.
- Session replay/export uses simple JSON download; extend for paginated history if needed.
- UV-created environment is not committed; contributors must recreate it locally.

## Safety Reminder
This project is a demonstration only. Do not deploy as medical/therapeutic software without professional oversight and appropriate safeguards.
