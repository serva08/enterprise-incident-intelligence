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

## Run tests

```powershell
python -m pytest
```
