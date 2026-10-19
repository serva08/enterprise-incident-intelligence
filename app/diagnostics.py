from dataclasses import dataclass
from typing import Protocol, Sequence

LabeledIncident = tuple[str, str]


@dataclass(frozen=True)
class EvaluationResult:
    correct: int
    total: int
    accuracy: float

    @property
    def incorrect(self) -> int:
        return self.total - self.correct


class IncidentClassifier(Protocol):
    def classify(self, description: str) -> str:
        ...


class RuleBasedClassifier:
    def classify(self, description: str) -> str:
        description = description.lower()

        if "timeout" in description:
            return "Connectivity issue"

        if "permission" in description:
            return "Authentication issue"

        if "memory" in description or "disk full" in description:
            return "Resource exhaustion"

        return "Unknown issue"


def diagnose_incident(description: str) -> str:
    return RuleBasedClassifier().classify(description)


def evaluate_classifier(
    classifier: IncidentClassifier,
    examples: Sequence[LabeledIncident],
) -> EvaluationResult:
    if not examples:
        raise ValueError("At least one labeled incident is required")

    correct = sum(
        classifier.classify(description) == expected
        for description, expected in examples
    )
    total = len(examples)

    return EvaluationResult(
        correct=correct,
        total=total,
        accuracy=correct / total,
    )
