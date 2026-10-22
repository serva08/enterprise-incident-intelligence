
from app.agent_tools import get_incident_stats

# Simulated arguments from an AI agent
tool_arguments = {
    "product": "DATABRICKS",
    "severity": "High",
}

result = get_incident_stats(**tool_arguments)

print("Tool result:", result)
