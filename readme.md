# Enterprise Incident Intelligence

A Python API built with FastAPI for creating and retrieving incidents.

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

## API endpoints

| Method | Path | Purpose | Expected response codes |
| --- | --- | --- | --- |
| `GET` | `/health` | Check that the API process is responding. | `200 OK` |
| `POST` | `/incidents` | Create an incident from a JSON request body. | `201 Created`, `422 Unprocessable Entity` for invalid input |
| `GET` | `/incidents` | List all incidents currently in memory. | `200 OK` |
| `GET` | `/incidents/{incident_id}` | Retrieve one incident by its integer ID. | `200 OK`, `404 Not Found` if no incident has that ID |

### Create an incident

Send JSON with all required `IncidentCreate` fields:

```bash
curl -X POST http://127.0.0.1:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fabric pipeline refresh failed",
    "description": "The pipeline stopped during data ingestion.",
    "severity": "High",
    "product": "Microsoft Fabric"
  }'
```

A successful request returns `201 Created` and an `IncidentResponse`, including the assigned ID and default status:

```json
{
  "title": "Fabric pipeline refresh failed",
  "description": "The pipeline stopped during data ingestion.",
  "severity": "High",
  "product": "Microsoft Fabric",
  "id": 1,
  "status": "Open"
}
```

If required fields are missing or values fail schema validation, FastAPI returns `422 Unprocessable Entity`.

### List and retrieve incidents

```bash
curl http://127.0.0.1:8000/incidents
curl http://127.0.0.1:8000/incidents/1
```

Both requests return `200 OK` when successful. The list endpoint returns an array (empty when there are no incidents). The detail endpoint returns `404 Not Found` with `{"detail":"Incident not found"}` if the ID is absent.

### Temporary storage limitation

Incidents are stored in a simple in-memory dictionary. They are lost when the application process restarts, and separate worker processes do not share the same data. This storage is suitable for development and learning, but not durable or consistent enough for production.

## Incident validation contract

The Pydantic models in `app/schemas.py` define the current incident data contract:

- `IncidentCreate` requires `title`, `description`, `severity`, and `product`.
- `title` must be 5–150 characters; `description` must contain at least 10 characters; `product` must contain at least 2 characters.
- `severity` must be exactly `Low`, `Medium`, `High`, or `Critical`.
- `IncidentResponse` includes the create fields, requires an integer `id`, and defaults `status` to `Open`. A supplied status must be exactly `Open`, `Investigating`, or `Resolved`.

Pydantic checks and constructs model instances at runtime. The create endpoint uses `IncidentCreate` to validate incoming request bodies, and incident responses use `IncidentResponse`.

By default, Pydantic may coerce compatible input values and ignore unknown fields. These models also do not trim whitespace, and `description` and `product` have no maximum length. Add stricter constraints if those behaviors do not fit the API's intended contract.

## PySpark incident data preparation notebook

The Databricks notebook source is [`pyspark/01_incident_data_preparation.py`](pyspark/01_incident_data_preparation.py). It uses six synthetic incidents, so it does not require or expose real incident data.

The notebook demonstrates how to:

- Create a Spark DataFrame with incident ID, product, category, and severity columns.
- Filter incidents by product or severity and select only the columns needed for an analysis.
- Group incidents by category or severity and count them; it also counts Critical incidents by product and category.
- Trim leading and trailing whitespace from product and category values.
- Separate rows with a missing or blank category from rows with a valid category.

To use it in Databricks, import the `.py` file as a notebook source and run its cells in order. Databricks provides the `spark` session used to create the DataFrame. In the category-quality section, `invalid` contains rows with null or blank categories, while `valid` contains rows with a non-null, non-blank category.

One learning note: the notebook's second filtering cell selects Critical incidents but assigns them to a variable named `fabric_incidents`; the variable name does not match the filter and would be clearer as `critical_incidents`.

## Run tests

```powershell
python -m pytest
```
