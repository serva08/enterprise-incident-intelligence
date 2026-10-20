
from typing import Protocol


class DiagnosticProvider(Protocol):
    def diagnose(self, description: str) -> dict:
        ...


class MockAIProvider:
    def diagnose(self, description: str) -> dict:
        text = description.lower()

        if "permission" in text:
            category = "Authentication issue"
            explanation = "The error is related to authentication or permission issues."
        elif "timeout" in text:
            category = "Connectivity issue"
            explanation = "There is an error related to connectivity or network timeout."
        elif "memory" in text or "disk full" in text or "disk is full" in text:
            category = "Resource exhaustion"
            explanation = "The error is related to resource exhaustion. There could be a memory leak or the disk is full."
        else:
            category = "Unknown issue"
            explanation = "The error category could not be determined."

        return {
            "category": category,
            "provider": "mock",
            "requires_human_review": True,
            "explanation": explanation,
        }


def run_diagnosis(
    description: str,
    provider: DiagnosticProvider,
) -> dict:
    return provider.diagnose(description)
