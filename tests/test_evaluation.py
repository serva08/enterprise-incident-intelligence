import pytest

from app.evaluation import evaluate_diagnostics


def test_evaluate_diagnostics_with_all_correct_predictions():
    cases = [
        {
            "description": "SQL connection timeout",
            "expected": "Connectivity issue",
        },
        {
            "description": "Pipeline memory exceeded",
            "expected": "Resource exhaustion",
        },
    ]

    result = evaluate_diagnostics(cases)

    assert result.total == 2
    assert result.correct == 2
    assert result.incorrect == 0
    assert result.accuracy == 1.0


def test_evaluate_diagnostics_counts_incorrect_predictions():
    cases = [
        {
            "description": "SQL connection timeout",
            "expected": "Connectivity issue",
        },
        {
            "description": "Unexpected failure",
            "expected": "Connectivity issue",
        },
    ]

    result = evaluate_diagnostics(cases)

    assert result.total == 2
    assert result.correct == 1
    assert result.incorrect == 1
    assert result.accuracy == 0.5


def test_evaluate_diagnostics_rejects_empty_dataset():
    with pytest.raises(ValueError, match="At least one labeled incident"):
        evaluate_diagnostics([])
