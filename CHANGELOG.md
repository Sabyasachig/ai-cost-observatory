# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-09

### Added
- 🎉 Initial release of AI Cost Observatory
- FastAPI backend with PostgreSQL database
- Streamlit dashboard with real-time cost tracking
- Python SDK for easy integration
- Support for OpenAI, Anthropic Claude models
- Docker deployment with docker-compose
- Agent-aware cost tracking (planner, retriever, executor, etc.)
- Cost forecasting and optimization suggestions
- Multi-project support with tagging system
- Request explorer with filtering
- Sample data generator for testing
- Comprehensive documentation

### Features
- **Dashboard UI**: Beautiful Streamlit interface with:
  - Overview page with key metrics
  - Agent breakdown analysis
  - Request explorer with search and filters
  - Cost forecasting charts
  - Optimization recommendations

- **API Endpoints**:
  - `/events` - Track LLM calls
  - `/dashboard/overview` - Get overview metrics
  - `/stats/agents` - Agent statistics
  - `/forecast` - Cost predictions
  - `/optimize` - Optimization suggestions

- **SDK Integration**:
  - Drop-in replacement for OpenAI
  - LangChain callbacks
  - Manual logging support
  - Automatic cost calculation

- **Docker Deployment**:
  - Full docker-compose setup
  - Health checks
  - Persistent data volumes
  - Management scripts

### Documentation
- README with quick start guide
- Getting started guide
- Docker troubleshooting guide
- API documentation
- Examples for OpenAI, LangChain, multi-agent systems
- Contributing guidelines

### Fixed
- Docker network configuration for container communication
- Python import paths (relative to absolute)
- Dashboard timeout errors with proper datetime formatting
- Health check dependencies between containers

### Known Issues
- None at this time

---

## Future Releases

### [1.1.0] - Planned
- Additional provider support (Cohere, Mistral)
- Alert system (Slack, email, webhooks)
- Export functionality (CSV, JSON, Parquet)
- Budget management and limits
- Enhanced forecasting algorithms

### [2.0.0] - Planned
- Team collaboration features
- Role-based access control
- Multi-tenant support
- Advanced cost allocation rules
- Integration with cloud billing APIs

---

## Release Notes Format

### Added
New features and capabilities

### Changed
Changes to existing functionality

### Deprecated
Features that will be removed in future releases

### Removed
Features that have been removed

### Fixed
Bug fixes

### Security
Security vulnerability fixes

---

For a detailed view of changes, see the [commit history](https://github.com/Sabyasachig/ai-cost-observatory/commits/main).
