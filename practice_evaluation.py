
from app.evaluation import evaluate_diagnostics

cases = [
    {
        "description": "SQL connection timeout",
        "expected": "Connectivity issue",
    },
    {
        "description": "User permission denied",
        "expected": "Authentication issue",
    },
    {
        "description": "Pipeline memory exceeded",
        "expected": "Resource exhaustion",
    },
    {
        "description": "Unexpected failure",
        "expected": "Connectivity issue",
    },
]

result = evaluate_diagnostics(cases)

print(f"Total evaluated: {result.total}")
print(f"Correct predictions: {result.correct}")
print(f"Incorrect predictions: {result.incorrect}")
print(f"Accuracy: {result.accuracy:.0%}")
