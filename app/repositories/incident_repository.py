from app.schemas import IncidentCreate, IncidentResponse


class InMemoryIncidentRepository:
    def __init__(self) -> None:
        self._incidents: dict[int, IncidentResponse] = {}
        self._next_incident_id = 1

    def create(self, incident: IncidentCreate) -> IncidentResponse:
        saved_incident = IncidentResponse(
            id=self._next_incident_id,
            **incident.model_dump(),
        )
        self._incidents[saved_incident.id] = saved_incident
        self._next_incident_id += 1
        return saved_incident

    def list_all(self) -> list[IncidentResponse]:
        return list(self._incidents.values())

    def get(self, incident_id: int) -> IncidentResponse | None:
        return self._incidents.get(incident_id)
