
import pytest
from pydantic import ValidationError

from app.schemas import IncidentCreate, IncidentResponse


def valid_incident():
    return {
        "title": "Fabric pipeline refresh failed",
        "description": "The pipeline stopped during data ingestion.",
        "severity": "High",
        "product": "Microsoft Fabric",
    }


def test_valid_incident():
    incident = IncidentCreate(**valid_incident())
    assert incident.severity == "High"


def test_title_too_short():
    data = valid_incident()
    data["title"] = "Oops"

    with pytest.raises(ValidationError):
        IncidentCreate(**data)


def test_invalid_severity():
    data = valid_incident()
    data["severity"] = "Emergency"

    with pytest.raises(ValidationError):
        IncidentCreate(**data)


def test_missing_product():
    data = valid_incident()
    del data["product"]

    with pytest.raises(ValidationError):
        IncidentCreate(**data)


def test_default_status():
    incident = IncidentResponse(
        **valid_incident(),
        id=1
    )

    assert incident.status == "Open"
