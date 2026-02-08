"""
Example: Manual Event Logging
For non-Python systems or custom integrations
"""

import requests

# API endpoint
API_URL = "http://localhost:8000"

# Log an event manually
event_data = {
    "model": "gpt-4o",
    "prompt_tokens": 320,
    "completion_tokens": 140,
    "latency_ms": 1250,
    "input_cost": 0.0008,
    "output_cost": 0.0014,
    "total_cost": 0.0022,
    "project": "customer-support",
    "agent": "classifier",
    "tags": {
        "env": "production",
        "feature": "intent_detection",
        "language": "en"
    }
}

response = requests.post(f"{API_URL}/events", json=event_data)

if response.status_code == 200:
    print("✅ Event logged successfully!")
    print(response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
