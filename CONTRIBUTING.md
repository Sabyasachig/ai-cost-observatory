# Contributing to AI Cost Observatory

First off, thank you for considering contributing to AI Cost Observatory! 🎉

It's people like you that make AI Cost Observatory such a great tool for the community.

## 🤝 Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and encourage diverse contributions
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. macOS, Ubuntu]
 - Docker version: [e.g. 24.0.0]
 - Python version: [e.g. 3.11]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear and descriptive title**
- **Detailed description** of the proposed functionality
- **Use cases** showing why this would be useful
- **Possible implementation** if you have ideas

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, concise commits
3. **Test your changes** thoroughly
4. **Update documentation** as needed
5. **Submit a pull request**

## 🛠️ Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Local Development

1. **Clone your fork:**
```bash
git clone https://github.com/YOUR_USERNAME/ai-cost-observatory.git
cd ai-cost-observatory
```

2. **Start the development environment:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

3. **Access the services:**
- Dashboard: http://localhost:8501
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

4. **Make your changes:**
```bash
# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Test thoroughly

# Commit your changes
git add .
git commit -m "Add amazing feature"

# Push to your fork
git push origin feature/amazing-feature
```

5. **Open a Pull Request** on GitHub

### Testing

Before submitting a PR, please ensure:

```bash
# All containers build successfully
docker-compose build

# All services start without errors
docker-compose up -d
docker-compose ps

# API health check passes
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Dashboard is accessible
curl -I http://localhost:8501
# Expected: HTTP/1.1 200 OK
```

### Code Style

- **Python**: Follow PEP 8
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Add type hints where applicable
- **Comments**: Write clear, concise comments

Example:
```python
def track_llm_call(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
    cost: float,
) -> dict:
    """
    Track an LLM API call.
    
    Args:
        model: The model name (e.g., "gpt-4")
        prompt_tokens: Number of tokens in the prompt
        completion_tokens: Number of tokens in the completion
        cost: Total cost in USD
        
    Returns:
        dict: Response with event_id and status
    """
    # Implementation
    pass
```

## 📁 Project Structure

```
ai_cost_observatory/
├── server/          # FastAPI backend
│   ├── api/         # API endpoints
│   ├── models/      # Database models
│   └── services/    # Business logic
├── ui/              # Streamlit dashboard
├── sdk/             # Python SDK
├── examples/        # Usage examples
├── docs/            # Documentation
└── tests/           # Tests
```

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Additional provider integrations (Cohere, Mistral, etc.)
- [ ] More optimization suggestions
- [ ] Better forecasting algorithms
- [ ] Cost allocation rules engine
- [ ] Export functionality (CSV, JSON, Parquet)

### Medium Priority
- [ ] More dashboard visualizations
- [ ] Alert system (Slack, email, webhook)
- [ ] Budget management and limits
- [ ] Team collaboration features
- [ ] API rate limiting

### Nice to Have
- [ ] Mobile-responsive dashboard
- [ ] Dark mode for UI
- [ ] More example integrations
- [ ] Video tutorials
- [ ] Integration tests

## 🔍 Code Review Process

1. At least one maintainer review is required
2. All CI checks must pass
3. Documentation must be updated
4. Breaking changes require discussion

## 📝 Commit Message Guidelines

Use clear and meaningful commit messages:

```
feat: Add support for Anthropic Claude models
fix: Resolve timeout error in dashboard
docs: Update installation instructions
refactor: Simplify cost calculation logic
test: Add tests for analytics service
chore: Update dependencies
```

## 🏷️ Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

- Open a [Discussion](https://github.com/Sabyasachig/ai-cost-observatory/discussions)
- Create an [Issue](https://github.com/Sabyasachig/ai-cost-observatory/issues)
- Check existing documentation in `/docs`

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort! 🚀

---

**Happy Contributing!** 🎊
