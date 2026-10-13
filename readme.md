# Enterprise Incident Intelligence

A Python API built with FastAPI. The current starter application exposes a health-check endpoint.

## Requirements

- Python 3.10 or newer

## Setup

Create and activate a virtual environment, then install the application and test dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pytest httpx
```

## Run the API

From the project root, start the development server:

```powershell
python -m uvicorn app.main:app --reload
```

The health endpoint is available at `http://127.0.0.1:8000/health` and returns:

```json
{"status": "healthy"}
```

FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Incident validation contract

The Pydantic models in `app/schemas.py` define the current incident data contract:

- `IncidentCreate` requires `title`, `description`, `severity`, and `product`.
- `title` must be 5–150 characters; `description` must contain at least 10 characters; `product` must contain at least 2 characters.
- `severity` must be exactly `Low`, `Medium`, `High`, or `Critical`.
- `IncidentResponse` includes the create fields, requires an integer `id`, and defaults `status` to `Open`. A supplied status must be exactly `Open`, `Investigating`, or `Resolved`.

Pydantic checks and constructs model instances at runtime. Invalid or missing required data raises a `ValidationError`. If an API endpoint uses one of these models as its request body, FastAPI performs that validation for incoming requests and reports invalid input as a client error. The current application only exposes `/health`; it does not yet have incident endpoints.

By default, Pydantic may coerce compatible input values and ignore unknown fields. These models also do not trim whitespace, and `description` and `product` have no maximum length. Add stricter constraints if those behaviors do not fit the API's intended contract.

## Run tests

```powershell
python -m pytest
```
