from app.repositories.incident_repository import InMemoryIncidentRepository
from app.schemas import IncidentCreate


def valid_incident() -> IncidentCreate:
    return IncidentCreate(
        title="Fabric pipeline refresh failed",
        description="The pipeline stopped during data ingestion.",
        severity="High",
        product="Microsoft Fabric",
    )


def test_create_assigns_ids_and_stores_incidents():
    repository = InMemoryIncidentRepository()

    first = repository.create(valid_incident())
    second = repository.create(valid_incident())

    assert first.id == 1
    assert second.id == 2
    assert repository.list_all() == [first, second]


def test_new_repository_starts_empty_and_returns_none_for_missing_incident():
    repository = InMemoryIncidentRepository()

    assert repository.list_all() == []
    assert repository.get(1) is None
