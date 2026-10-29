# Incident Intelligence Application

This project area contains a small FastAPI incident API and learning examples for diagnostics, evaluation, and agent tools. It demonstrates how application code can expose typed API contracts and deterministic Python functions without requiring an external model service.

## What is included

| Area | Files | Purpose |
| --- | --- | --- |
| Incident API | `main.py`, `schemas.py` | Health check and create/list/get endpoints with Pydantic request and response models. |
| Rule-based diagnostics | `diagnostics.py`, `evaluation.py` | A simple classifier interface and offline accuracy evaluation against labeled examples. |
| Mock AI provider | `ai_diagnostics.py` | Demonstrates a provider-shaped interface and structured diagnostic result without a paid API call. |
| Agent tool example | `agent_tools.py`, `tool_definitions.py`, `../practice_tool_call.py` | Counts synthetic incidents using a Python function and declares a tool schema; the practice script simulates tool arguments locally. |
| Tests | `../tests/` | Exercises API, schemas, diagnostics, evaluation, and tool behavior. |

## Run locally

From the repository root, install the packages used by the app and tests, then run:

```powershell
python -m uvicorn app.main:app --reload
python -m pytest
```

The API documentation is available at `http://127.0.0.1:8000/docs`. To run the local tool-call example:

```powershell
python practice_tool_call.py
```

## Design and current limitations

- The API stores incidents in process memory; data is lost when the process restarts and is not shared across worker processes.
- The diagnostic provider is a deterministic mock, not an OpenAI, Claude, or Azure AI integration.
- The tool example invokes an allowlisted Python function directly; it is not connected to an LLM. Model-generated arguments would need validation and authorization before dispatch.
- Evaluation data is for offline learning and should not be treated as evidence of real-world model performance.

These boundaries are intentional for a low-cost learning portfolio. Database persistence, authentication, deployment hardening, and a real model adapter are future extensions, not implemented features.
