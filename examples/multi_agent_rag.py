"""
Example: Multi-Agent System with RAG
"""

from openai import OpenAI
from ai_observer import observe, track_retrieval

client = OpenAI()

def retrieve_context(query: str) -> str:
    """Simulate RAG retrieval"""
    # Track retrieval metrics
    track_retrieval(
        chunks=5,
        context_tokens=1500,
        source="knowledge_base",
        project="rag-agent",
        tags={"query_type": "semantic_search"}
    )
    
    # Simulate retrieval
    return "Context: Vector databases store embeddings for semantic search..."

def planner_agent(user_query: str) -> str:
    """Planning agent"""
    with observe(
        project="rag-agent",
        agent="planner",
        step="query_planning"
    ) as obs:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a query planner. Break down the user query."},
                {"role": "user", "content": user_query}
            ]
        )
        obs.track_response(response)
        return response.choices[0].message.content

def executor_agent(plan: str, context: str) -> str:
    """Execution agent"""
    with observe(
        project="rag-agent",
        agent="executor",
        step="answer_generation"
    ) as obs:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant. Use the context to answer."},
                {"role": "user", "content": f"Plan: {plan}\n\nContext: {context}\n\nProvide the final answer."}
            ]
        )
        obs.track_response(response)
        return response.choices[0].message.content

# Main workflow
user_query = "What are vector databases?"

print("Step 1: Planning...")
plan = planner_agent(user_query)
print(f"Plan: {plan}\n")

print("Step 2: Retrieving context...")
context = retrieve_context(user_query)
print(f"Context retrieved.\n")

print("Step 3: Generating answer...")
answer = executor_agent(plan, context)
print(f"Answer: {answer}")

print("\n✅ All steps tracked! Check the dashboard for cost breakdown by agent.")
