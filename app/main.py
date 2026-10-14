from fastapi import FastAPI, HTTPException, Request

from app.schemas import IncidentCreate, IncidentResponse

app = FastAPI(
    title="Enterprise Incident Intelligence",
    version="0.1.0"
)
app.state.incidents = {}
app.state.next_incident_id = 1

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/incidents", response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate, request: Request) -> IncidentResponse:
    incident_id = request.app.state.next_incident_id
    saved_incident = IncidentResponse(id=incident_id, **incident.model_dump())

    request.app.state.incidents[incident_id] = saved_incident
    request.app.state.next_incident_id += 1
    return saved_incident


@app.get("/incidents", response_model=list[IncidentResponse])
def list_incidents(request: Request) -> list[IncidentResponse]:
    return list(request.app.state.incidents.values())


@app.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, request: Request) -> IncidentResponse:
    incident = request.app.state.incidents.get(incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident