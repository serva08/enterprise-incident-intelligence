from app.repositories.incident_repository import InMemoryIncidentRepository
from app.schemas import IncidentCreate, IncidentResponse


class IncidentNotFoundError(LookupError):
    pass


class IncidentService:
    def __init__(self, repository: InMemoryIncidentRepository) -> None:
        self._repository = repository

    def create_incident(self, incident: IncidentCreate) -> IncidentResponse:
        return self._repository.create(incident)

    def list_incidents(self) -> list[IncidentResponse]:
        return self._repository.list_all()

    def get_incident(self, incident_id: int) -> IncidentResponse:
        incident = self._repository.get(incident_id)
        if incident is None:
            raise IncidentNotFoundError(incident_id)
        return incident
