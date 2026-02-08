"""
Example: Basic OpenAI Integration
"""

from openai import OpenAI
from ai_observer import observe, configure

# Configure the observer (optional, uses environment variables by default)
configure(
    endpoint="http://localhost:8000",
    enabled=True,
)

# Initialize OpenAI client
client = OpenAI()

# Track a simple completion
with observe(
    project="chatbot",
    agent="assistant",
    user_id="user_123",
    tags={"env": "production", "feature": "customer_support"}
) as obs:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    
    # Track the response
    obs.track_response(response)
    
    print(response.choices[0].message.content)
