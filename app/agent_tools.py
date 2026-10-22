
INCIDENTS = [
    {"id": 1, "product": "FABRIC",
     "category": "timeout", "severity": "High"},
    {"id": 2, "product": "FABRIC",
     "category": "permission", "severity": "Medium"},
    {"id": 3, "product": "DATABRICKS",
     "category": "memory", "severity": "Critical"},
    {"id": 4, "product": "FABRIC",
     "category": "timeout", "severity": "Critical"},
    {"id": 5, "product": "DATABRICKS",
     "category": "memory", "severity": "High"},
]


def get_incident_stats(
    product: str,
    severity: str | None = None,
) -> dict:

    product = product.strip().upper()
    if not product:
        raise ValueError("Product cannot be empty")
    if severity is not None:
        severity = severity.strip()
        if not severity:
            raise ValueError("Severity cannot be empty")

    matches = [
        incident
        for incident in INCIDENTS
        if incident["product"].strip().upper() == product
        and (severity is None or incident["severity"].lower() == severity.lower())
    ]

    return {
        "product": product,
        "severity": severity,
        "count": len(matches),
    }
