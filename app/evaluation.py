
from collections.abc import Mapping, Sequence

from app.diagnostics import (
    EvaluationResult,
    RuleBasedClassifier,
    evaluate_classifier,
)


def evaluate_diagnostics(
    cases: Sequence[Mapping[str, str]],
) -> EvaluationResult:
    examples = [
        (case["description"], case["expected"])
        for case in cases
    ]

    return evaluate_classifier(RuleBasedClassifier(), examples)
