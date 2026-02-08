"""
Generate sample data for AI Cost Observatory
Useful for testing and demos without real LLM API calls
"""

import requests
import random
from datetime import datetime, timedelta
import time

API_URL = "http://localhost:8000"

# Sample configurations
PROJECTS = ["customer-support", "rag-system", "chatbot", "research-agent"]
AGENTS = ["planner", "retriever", "executor", "synthesizer", "classifier"]
MODELS = [
    "gpt-4o",
    "gpt-4o-mini", 
    "gpt-3.5-turbo",
    "claude-3-5-sonnet",
    "claude-3-haiku"
]

# Model pricing (per 1M tokens)
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
}


def calculate_cost(model, prompt_tokens, completion_tokens):
    """Calculate cost for a model"""
    pricing = PRICING.get(model, {"input": 0.0, "output": 0.0})
    input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing["output"]
    return round(input_cost, 6), round(output_cost, 6), round(input_cost + output_cost, 6)


def generate_event():
    """Generate a random event"""
    project = random.choice(PROJECTS)
    agent = random.choice(AGENTS) if random.random() > 0.2 else None
    model = random.choice(MODELS)
    
    # Generate realistic token counts
    prompt_tokens = random.randint(50, 2000)
    completion_tokens = random.randint(20, 500)
    
    # Calculate costs
    input_cost, output_cost, total_cost = calculate_cost(
        model, prompt_tokens, completion_tokens
    )
    
    # Random latency
    latency_ms = random.randint(200, 3000)
    
    return {
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "latency_ms": latency_ms,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
        "currency": "USD",
        "project": project,
        "agent": agent,
        "user_id": f"user_{random.randint(1, 100)}",
        "tags": {
            "env": random.choice(["production", "staging", "development"]),
            "feature": random.choice(["search", "chat", "analysis", "summary"]),
        }
    }


def send_event(event, timestamp=None):
    """Send event to API"""
    if timestamp:
        event["timestamp"] = timestamp.isoformat()
    
    try:
        response = requests.post(f"{API_URL}/events", json=event, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending event: {e}")
        return False


def generate_historical_data(days=30):
    """Generate historical data for the past N days"""
    print(f"🎲 Generating {days} days of historical data...")
    
    end_date = datetime.utcnow()
    total_events = 0
    
    for day in range(days):
        date = end_date - timedelta(days=days - day)
        
        # Generate 50-200 events per day with some variation
        num_events = random.randint(50, 200)
        
        for _ in range(num_events):
            # Random time during the day
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            timestamp = date.replace(hour=hour, minute=minute, second=second)
            
            event = generate_event()
            if send_event(event, timestamp):
                total_events += 1
        
        print(f"  Day {day + 1}/{days}: {num_events} events generated")
    
    print(f"\n✅ Generated {total_events} events over {days} days")
    return total_events


def generate_realtime_data(duration_seconds=60):
    """Generate real-time data for testing"""
    print(f"🔄 Generating real-time data for {duration_seconds} seconds...")
    
    start_time = time.time()
    event_count = 0
    
    while time.time() - start_time < duration_seconds:
        event = generate_event()
        if send_event(event):
            event_count += 1
            print(f"  Event {event_count}: {event['model']} - ${event['total_cost']:.6f}")
        
        # Random delay between events (1-5 seconds)
        time.sleep(random.uniform(1, 5))
    
    print(f"\n✅ Generated {event_count} real-time events")
    return event_count


def main():
    """Main function"""
    print("🔭 AI Cost Observatory - Sample Data Generator")
    print("=" * 50)
    print()
    
    # Check if API is available
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding correctly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API at {API_URL}")
        print(f"   Error: {e}")
        print("\n💡 Make sure the server is running:")
        print("   cd server && python -m api.main")
        return
    
    print("✅ API is available\n")
    
    # Menu
    print("Select an option:")
    print("1. Generate 30 days of historical data")
    print("2. Generate 7 days of historical data")
    print("3. Generate real-time data (60 seconds)")
    print("4. Generate both historical and real-time data")
    print("5. Exit")
    
    choice = input("\nYour choice (1-5): ").strip()
    
    if choice == "1":
        generate_historical_data(30)
    elif choice == "2":
        generate_historical_data(7)
    elif choice == "3":
        generate_realtime_data(60)
    elif choice == "4":
        generate_historical_data(30)
        print("\nNow generating real-time data...")
        generate_realtime_data(60)
    elif choice == "5":
        print("Goodbye!")
        return
    else:
        print("Invalid choice")
        return
    
    print("\n🎉 Done! Open the dashboard to see the data:")
    print("   http://localhost:8501")


if __name__ == "__main__":
    main()
