# 🔭 AI Cost Observatory

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Open-source observability layer for agentic systems**

Track LLM costs, optimize spending, and gain insights into your AI systems. Model-agnostic, provider-agnostic, and self-hostable.

> "Datadog + FinOps for LLMs"

## 🎯 Why AI Cost Observatory?

- **💰 Cost Attribution**: Track spending per agent, feature, user, or request
- **📊 Real-time Analytics**: Live dashboards showing usage patterns
- **🔮 Forecasting**: Project monthly costs based on trends
- **💡 Optimization**: Automatic suggestions to reduce costs
- **🔌 Drop-in Integration**: 2 lines of code to start tracking
- **🏢 Enterprise Ready**: Self-hostable, supports custom pricing, tagging system

## ✨ Features

- ✅ **Model Agnostic**: OpenAI, Anthropic, local models
- ✅ **Agent Aware**: Track costs by agent stages (planner, retriever, executor)
- ✅ **RAG Ready**: Separate tracking for retrieval and generation
- ✅ **Framework Support**: LangChain, LlamaIndex callbacks
- ✅ **Language Agnostic**: HTTP API for any language
- ✅ **Plugin System**: Extensible architecture

## 🚀 Quick Start

### 1. Start the Server

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-cost-observatory.git
cd ai-cost-observatory

# Start with Docker Compose (recommended)
docker-compose up -d

# Or manually:
# Start API server
cd server
pip install -r requirements.txt
python -m api.main

# Start dashboard (in another terminal)
cd ui
pip install -r requirements.txt
streamlit run dashboard.py
```

### 2. Install SDK

```bash
pip install ai-cost-observatory
```

### 3. Track Your First LLM Call

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

### 4. View Dashboard

Open http://localhost:8501 to see your costs!

## 📖 Documentation

### Basic Usage

```python
from ai_observer import observe, configure

# Configure once (optional - uses env vars by default)
configure(
    endpoint="http://localhost:8000",
    api_key="your-key",  # optional
)

# Track any LLM call
with observe(
    project="support-bot",
    agent="classifier",
    user_id="user_123",
    tags={"env": "prod", "feature": "intent"}
) as obs:
    response = client.chat.completions.create(...)
    obs.track_response(response)
```

### LangChain Integration

```python
from langchain_openai import ChatOpenAI
from ai_observer.langchain import CostCallback

# Add callback to any LangChain component
llm = ChatOpenAI(
    callbacks=[CostCallback(project="rag-app", agent="planner")]
)

# That's it! All calls are now tracked
```

### RAG Systems

```python
from ai_observer import track_retrieval

# Track retrieval separately
track_retrieval(
    chunks=5,
    context_tokens=1800,
    source="knowledge_base",
    project="rag-app"
)
```

### Multi-Agent Systems

```python
# Track each agent separately
with observe(project="research", agent="planner", step="planning"):
    plan = planner.run(query)

with observe(project="research", agent="retriever", step="search"):
    docs = retriever.search(plan)

with observe(project="research", agent="synthesizer", step="generation"):
    answer = synthesizer.generate(docs)
```

## 🎨 Dashboard Features

### 1. Overview
- Total costs (today, month)
- Token usage
- Active models
- Cost trends

### 2. Agent Breakdown
- Cost per agent
- Request distribution
- Performance metrics

### 3. Request Explorer
- Detailed event log
- Filtering by project/agent/model
- Cost and latency per request

### 4. Forecast
- Monthly projection
- Trend analysis
- Confidence levels

### 5. Optimization
- Cheaper model suggestions
- Prompt size recommendations
- Caching opportunities

## 🏗️ Architecture

```
Your App
    ↓
SDK (Context Manager)
    ↓
Event Collector API (FastAPI)
    ↓
Database (PostgreSQL/SQLite)
    ↓
Analytics Engine
    ↓
Dashboard (Streamlit)
```

## 🔌 Integrations

### Supported Providers
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Anthropic (Claude 3.5, Claude 3)
- Custom providers (via plugin system)

### Supported Frameworks
- LangChain
- LlamaIndex (coming soon)
- Direct SDK calls

### Language Support
- Python (native SDK)
- Any language (HTTP API)

## 📊 API Reference

### POST /events
```json
{
  "model": "gpt-4o",
  "prompt_tokens": 200,
  "completion_tokens": 90,
  "project": "chatbot",
  "agent": "assistant",
  "tags": {"env": "prod"}
}
```

### GET /dashboard/overview
Returns dashboard metrics

### GET /forecast
Returns cost forecast

### GET /optimize
Returns optimization suggestions

See [API Documentation](docs/api.md) for details.

## 🔧 Configuration

### Environment Variables

```bash
# SDK Configuration
AI_OBSERVER_ENDPOINT=http://localhost:8000
AI_OBSERVER_API_KEY=your-key
AI_OBSERVER_ENABLED=true

# Server Configuration
DATABASE_URL=postgresql://user:pass@localhost/ai_cost_observatory
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
```

### Custom Pricing

Create `config/pricing.yaml`:

```yaml
models:
  gpt-4o:
    input_price: 2.50  # per 1M tokens
    output_price: 10.00
  custom-model:
    input_price: 1.00
    output_price: 3.00
```

## 🧩 Plugin System

### Custom Provider

```python
from ai_observer.adapters import ProviderAdapter, get_adapter_registry

class MyCustomAdapter(ProviderAdapter):
    def extract_usage(self, response):
        return {
            "model": response.model,
            "prompt_tokens": response.usage.input,
            "completion_tokens": response.usage.output,
            "total_tokens": response.usage.total,
        }
    
    def extract_cost(self, usage, model):
        # Your pricing logic
        return {"total_cost": 0.01, "currency": "USD"}
    
    def can_handle(self, response):
        return hasattr(response, 'my_custom_field')

# Register
registry = get_adapter_registry()
registry.register_adapter(MyCustomAdapter())
```

## 🚢 Deployment

### Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

See [Deployment Guide](docs/deployment.md)

### Cloud Platforms
- AWS (ECS, RDS)
- GCP (Cloud Run, Cloud SQL)
- Azure (Container Instances, PostgreSQL)

## 📈 Roadmap

- [x] Phase 1: Core MVP
  - [x] SDK with context manager
  - [x] Provider adapters (OpenAI, Anthropic)
  - [x] FastAPI collector
  - [x] PostgreSQL/SQLite storage
  - [x] Streamlit dashboard

- [x] Phase 2: Intelligence
  - [x] Cost forecasting
  - [x] Anomaly detection (basic)
  - [x] Optimization suggestions

- [ ] Phase 3: Advanced Features
  - [ ] LlamaIndex integration
  - [ ] Prompt diff tool
  - [ ] Model benchmarking
  - [ ] Alert system
  - [ ] Custom dashboards (plugin)

- [ ] Phase 4: Enterprise
  - [ ] Role-based access
  - [ ] SSO integration
  - [ ] Advanced analytics
  - [ ] Export/reporting

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🌟 Star History

If this project helps you, please star it on GitHub!

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

Built for the AI community. Inspired by the need for better cost visibility in agentic systems.

---

**Made with ❤️ for AI Engineers**
