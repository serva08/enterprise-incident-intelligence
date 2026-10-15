import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_incident_service
from app.main import app
from app.repositories.incident_repository import InMemoryIncidentRepository
from app.services.incident_service import IncidentService


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolate_incident_repository():
    repository = InMemoryIncidentRepository()
    app.dependency_overrides[get_incident_service] = lambda: IncidentService(repository)
    yield
    app.dependency_overrides.pop(get_incident_service, None)


def valid_incident():
    return {
        "title": "Fabric pipeline refresh failed",
        "description": "The pipeline stopped during data ingestion.",
        "severity": "High",
        "product": "Microsoft Fabric",
    }


def test_create_incident_returns_201_and_response_model():
    response = client.post("/incidents", json=valid_incident())

    assert response.status_code == 201
    assert response.json() == {
        **valid_incident(),
        "id": 1,
        "status": "Open",
    }


def test_list_incidents_returns_created_incidents():
    client.post("/incidents", json=valid_incident())

    response = client.get("/incidents")

    assert response.status_code == 200
    assert response.json() == [
        {
            **valid_incident(),
            "id": 1,
            "status": "Open",
        }
    ]


def test_get_incident_returns_matching_incident():
    client.post("/incidents", json=valid_incident())

    response = client.get("/incidents/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == valid_incident()["title"]


def test_get_missing_incident_returns_404():
    response = client.get("/incidents/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Incident not found"}


def test_create_incident_rejects_invalid_request_body():
    data = valid_incident()
    data["severity"] = "Emergency"

    response = client.post("/incidents", json=data)

    assert response.status_code == 422
