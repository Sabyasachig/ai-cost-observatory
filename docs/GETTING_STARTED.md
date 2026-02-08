# Getting Started with AI Cost Observatory

This guide will walk you through setting up and using AI Cost Observatory.

## Prerequisites

- Python 3.8 or higher
- pip
- OpenAI API key (for examples)
- Docker (optional, for production deployment)

## Installation Methods

### Method 1: Quick Start (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-cost-observatory.git
cd ai-cost-observatory

# Run the quickstart script
./quickstart.sh
```

### Method 2: Manual Installation

#### Step 1: Set up the SDK

```bash
cd sdk
pip install -e .
cd ..
```

#### Step 2: Set up the Server

```bash
cd server
pip install -r requirements.txt

# Initialize the database
python -c "from database import init_db; init_db()"

# Start the server
python -m api.main
```

The API will be available at `http://localhost:8000`.

#### Step 3: Set up the Dashboard

In a new terminal:

```bash
cd ui
pip install -r requirements.txt

# Start the dashboard
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`.

### Method 3: Docker Compose (Production)

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# SDK Configuration
AI_OBSERVER_ENDPOINT=http://localhost:8000
AI_OBSERVER_API_KEY=
AI_OBSERVER_ENABLED=true

# Server Configuration
DATABASE_URL=sqlite:///./ai_cost_observatory.db

# OpenAI (for examples)
OPENAI_API_KEY=your-openai-api-key
```

For PostgreSQL (production):

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/ai_cost_observatory
```

## First Steps

### 1. Verify Installation

Check that the API is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Run Your First Example

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# Run the basic example
python examples/basic_openai.py
```

### 3. View the Dashboard

Open your browser and go to: `http://localhost:8501`

You should see:
- Today's cost
- Month's cost
- Total tokens
- Cost trends

## Usage Examples

### Basic Tracking

```python
from openai import OpenAI
from ai_observer import observe

client = OpenAI()

with observe(project="chatbot", agent="assistant") as obs:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    obs.track_response(response)
```

### LangChain Integration

```python
from langchain_openai import ChatOpenAI
from ai_observer.langchain import CostCallback

llm = ChatOpenAI(
    model="gpt-4o-mini",
    callbacks=[CostCallback(project="rag-app")]
)

result = llm.invoke("What are vector databases?")
```

### Multi-Agent System

```python
# Track different agents separately
with observe(project="research", agent="planner"):
    plan = create_plan(query)

with observe(project="research", agent="retriever"):
    docs = retrieve_documents(plan)

with observe(project="research", agent="synthesizer"):
    answer = generate_answer(docs)
```

### RAG System with Retrieval Tracking

```python
from ai_observer import observe, track_retrieval

# Track retrieval
track_retrieval(
    chunks=5,
    context_tokens=1500,
    source="knowledge_base",
    project="rag-system"
)

# Track generation
with observe(project="rag-system", agent="generator") as obs:
    response = client.chat.completions.create(...)
    obs.track_response(response)
```

## Dashboard Overview

### Page 1: Overview
- **Key Metrics**: Today's cost, month's cost, total tokens
- **Cost Over Time**: Line chart showing daily costs
- **Top Models**: Bar chart of most used models
- **Top Agents**: Bar chart of agent costs

### Page 2: Agent Breakdown
- Agent-by-agent cost analysis
- Request counts and token usage
- Performance metrics

### Page 3: Request Explorer
- Detailed event log
- Filter by project, agent, model, date
- View individual request details

### Page 4: Forecast
- Monthly cost projection
- Trend analysis (increasing/decreasing/stable)
- Confidence levels

### Page 5: Optimization
- Cost-saving suggestions
- Model alternatives
- Prompt optimization tips
- Caching opportunities

## Advanced Configuration

### Custom Model Pricing

Create `server/config/pricing.yaml`:

```yaml
models:
  my-custom-model:
    input_price: 1.00   # per 1M tokens
    output_price: 3.00  # per 1M tokens
    currency: USD
```

### Custom Provider Adapter

```python
from ai_observer.adapters import ProviderAdapter, get_adapter_registry

class MyAdapter(ProviderAdapter):
    def extract_usage(self, response):
        return {
            "model": response.model,
            "prompt_tokens": response.usage.input,
            "completion_tokens": response.usage.output,
            "total_tokens": response.usage.total,
        }
    
    def extract_cost(self, usage, model):
        # Your pricing logic
        cost = usage["prompt_tokens"] * 0.001 / 1000
        return {
            "input_cost": cost,
            "output_cost": 0.0,
            "total_cost": cost,
            "currency": "USD"
        }
    
    def can_handle(self, response):
        return hasattr(response, 'my_field')

# Register
get_adapter_registry().register_adapter(MyAdapter())
```

### Using with Anthropic

```python
from anthropic import Anthropic
from ai_observer import observe

client = Anthropic()

with observe(project="chatbot", agent="claude") as obs:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    obs.track_response(response)
```

## API Reference

### SDK Methods

#### `observe()`
Context manager for tracking LLM calls.

**Parameters:**
- `project` (str): Project name
- `agent` (str, optional): Agent name
- `step` (str, optional): Step name
- `user_id` (str, optional): User ID
- `tags` (dict, optional): Custom tags
- `endpoint` (str, optional): Custom API endpoint

#### `log_event()`
Manually log an event.

**Parameters:**
- `model` (str): Model name
- `prompt_tokens` (int): Prompt tokens
- `completion_tokens` (int): Completion tokens
- Other optional parameters

#### `track_retrieval()`
Track RAG retrieval metrics.

**Parameters:**
- `chunks` (int): Number of chunks
- `context_tokens` (int): Context size
- `source` (str, optional): Source name
- `project` (str, optional): Project name

### REST API Endpoints

#### `POST /events`
Create a new event.

#### `GET /events`
List events with filtering.

#### `GET /dashboard/overview`
Get dashboard overview data.

#### `GET /stats/costs`
Get cost statistics.

#### `GET /forecast`
Get cost forecast.

#### `GET /optimize`
Get optimization suggestions.

## Troubleshooting

### Issue: "Connection refused" error

**Solution:** Make sure the API server is running:
```bash
cd server
python -m api.main
```

### Issue: "Module not found" error

**Solution:** Install the SDK in development mode:
```bash
cd sdk
pip install -e .
```

### Issue: Dashboard shows no data

**Solution:** 
1. Check that you've run some tracked LLM calls
2. Verify API connection in dashboard sidebar
3. Check server logs for errors

### Issue: Database errors

**Solution:** Reinitialize the database:
```bash
cd server
rm ai_cost_observatory.db  # if using SQLite
python -c "from database import init_db; init_db()"
```

## Best Practices

1. **Tagging Strategy**: Use consistent tags for better analytics
   ```python
   tags={"env": "prod", "feature": "search", "version": "v1"}
   ```

2. **Project Organization**: Use meaningful project names
   ```python
   project="customer-support"  # Good
   project="test"              # Bad
   ```

3. **Agent Naming**: Use descriptive agent names
   ```python
   agent="planner"     # Good
   agent="agent1"      # Bad
   ```

4. **Cost Monitoring**: Set up regular reviews of optimization suggestions

5. **Database**: Use PostgreSQL for production deployments

## Next Steps

- Explore all examples in the `examples/` directory
- Read the [API Documentation](api.md)
- Check out [Advanced Features](advanced.md)
- Join the community discussions

## Support

- GitHub Issues: https://github.com/yourusername/ai-cost-observatory/issues
- Documentation: https://github.com/yourusername/ai-cost-observatory/docs
- Email: your.email@example.com
