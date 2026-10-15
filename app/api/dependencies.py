from app.repositories.incident_repository import InMemoryIncidentRepository
from app.services.incident_service import IncidentService

_shared_repository = InMemoryIncidentRepository()


def get_incident_service() -> IncidentService:
    return IncidentService(_shared_repository)
