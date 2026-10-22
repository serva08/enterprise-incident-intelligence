
from app.agent_tools import get_incident_stats


def test_critical_fabric_incidents():
    result = get_incident_stats("Fabric", "Critical")

    assert result["count"] == 1
    assert result["product"] == "FABRIC"


def test_all_fabric_incidents():
    result = get_incident_stats("Fabric")

    assert result["count"] == 3


def test_severity_matching():
    result = get_incident_stats("Fabric", "critical")

    assert result["count"] == 1
    assert result["product"] == "FABRIC"


def test_severity_none():
    result = get_incident_stats("Databricks", None)

    assert result["count"] == 2
    assert result["product"] == "DATABRICKS"


def test_product_matching_trims_whitespace():
    result = get_incident_stats(" Fabric ")

    assert result["count"] == 3
    assert result["product"] == "FABRIC"