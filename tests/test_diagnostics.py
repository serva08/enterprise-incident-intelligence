import pytest

from app.diagnostics import (
    EvaluationResult,
    RuleBasedClassifier,
    diagnose_incident,
    evaluate_classifier,
)


@pytest.mark.parametrize(
    "description, expected",
    [
        ("SQL connection timeout", "Connectivity issue"),
        ("User permission denied", "Authentication issue"),
        ("Pipeline memory exceeded", "Resource exhaustion"),
        ("Unknown exception", "Unknown issue"),
        ("Disk full error", "Resource exhaustion")
    ],
)
def test_diagnosis(description, expected):
    assert diagnose_incident(description) == expected


def test_rule_based_classifier_matches_diagnosis_function():
    classifier = RuleBasedClassifier()

    assert classifier.classify("SQL connection timeout") == diagnose_incident(
        "SQL connection timeout"
    )


def test_evaluate_classifier_reports_accuracy():
    classifier = RuleBasedClassifier()
    examples = [
        ("SQL connection timeout", "Connectivity issue"),
        ("User permission denied", "Authentication issue"),
        ("Disk full error", "Resource exhaustion"),
        ("Unknown exception", "Authentication issue"),
    ]

    result = evaluate_classifier(classifier, examples)

    assert result == EvaluationResult(correct=3, total=4, accuracy=0.75)


def test_evaluate_classifier_rejects_empty_examples():
    with pytest.raises(ValueError, match="At least one labeled incident"):
        evaluate_classifier(RuleBasedClassifier(), [])
