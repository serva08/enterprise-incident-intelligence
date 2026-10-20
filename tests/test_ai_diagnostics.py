from app.ai_diagnostics import MockAIProvider


def test_mock_provider_explains_timeout_classification():
    result = MockAIProvider().diagnose("SQL connection timeout")

    assert result["category"] == "Connectivity issue"
    assert "timeout" in result["explanation"].lower()

def test_mock_provider_explains_permission_classification():
    result = MockAIProvider().diagnose("User permission denied")

    assert result["category"] == "Authentication issue"
    assert "permission" in result["explanation"].lower()

def test_mock_provider_explains_resource_exhaustion_classification():
    result = MockAIProvider().diagnose("Disk is full")

    assert result["category"] == "Resource exhaustion"
    assert "memory" in result["explanation"].lower() or "disk full" in result["explanation"].lower()

def test_mock_provider_explains_unknown_issue_classification():
    result = MockAIProvider().diagnose("Some other error")

    assert result["category"] == "Unknown issue"
    assert "could not be determined" in result["explanation"].lower()