
INCIDENT_STATS_TOOL = {
    "type": "function",
    "name": "get_incident_stats",
    "description": (
        "Get incident counts for a product, "
        "optionally filtered by severity."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
                "enum": ["FABRIC", "DATABRICKS"],
            },
            "severity": {
                "type": ["string", "null"],
                "enum": [
                    "Low", "Medium", "High",
                    "Critical", None
                ],
            },
        },
        "required": ["product", "severity"],
        "additionalProperties": False,
    },
    "strict": True,
}
