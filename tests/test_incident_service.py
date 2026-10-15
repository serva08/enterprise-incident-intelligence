import pytest

from app.repositories.incident_repository import InMemoryIncidentRepository
from app.schemas import IncidentCreate
from app.services.incident_service import IncidentNotFoundError, IncidentService


def valid_incident() -> IncidentCreate:
    return IncidentCreate(
        title="Fabric pipeline refresh failed",
        description="The pipeline stopped during data ingestion.",
        severity="High",
        product="Microsoft Fabric",
    )


def test_create_and_list_incidents():
    service = IncidentService(InMemoryIncidentRepository())

    created = service.create_incident(valid_incident())

    assert service.list_incidents() == [created]


def test_get_incident_returns_created_incident():
    service = IncidentService(InMemoryIncidentRepository())
    created = service.create_incident(valid_incident())

    assert service.get_incident(created.id) == created


def test_get_missing_incident_raises_not_found_error():
    service = IncidentService(InMemoryIncidentRepository())

    with pytest.raises(IncidentNotFoundError):
        service.get_incident(999)
