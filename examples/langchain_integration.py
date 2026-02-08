"""
Example: LangChain Integration
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from ai_observer.langchain import CostCallback

# Create the cost callback
callback = CostCallback(
    project="rag-system",
    agent="retriever",
    tags={"env": "production"}
)

# Create LangChain components with callback
llm = ChatOpenAI(
    model="gpt-4o-mini",
    callbacks=[callback]
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("user", "{question}")
])

# Create chain
chain = prompt | llm

# Use the chain - costs are automatically tracked
response = chain.invoke({"question": "Explain vector databases in one sentence."})

print(response.content)
