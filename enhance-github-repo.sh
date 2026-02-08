#!/bin/bash

# GitHub Repository Enhancement Script
# Run this after successfully creating your repository

set -e

REPO="Sabyasachig/ai-cost-observatory"

echo "🎨 Enhancing GitHub Repository: $REPO"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to run command with error handling
run_command() {
    local description=$1
    local command=$2
    
    echo -e "${BLUE}$description...${NC}"
    if eval "$command"; then
        echo -e "${GREEN}✅ Done${NC}"
        echo ""
    else
        echo -e "${YELLOW}⚠️  Failed (you can do this manually)${NC}"
        echo ""
    fi
}

# 1. Add repository topics
echo -e "${BLUE}Adding repository topics for better discoverability...${NC}"
gh repo edit $REPO \
  --add-topic ai \
  --add-topic llm \
  --add-topic observability \
  --add-topic cost-tracking \
  --add-topic openai \
  --add-topic langchain \
  --add-topic agentic-ai \
  --add-topic monitoring \
  --add-topic analytics \
  --add-topic streamlit \
  --add-topic fastapi \
  --add-topic docker \
  --add-topic postgresql \
  --add-topic python 2>/dev/null || echo "Topics may have been added already"

echo -e "${GREEN}✅ Topics added${NC}"
echo ""

# 2. Create first release
echo -e "${BLUE}Creating v1.0.0 release...${NC}"

# Check if tag exists
if git rev-parse v1.0.0 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Tag v1.0.0 already exists${NC}"
else
    git tag -a v1.0.0 -m "Initial release: AI Cost Observatory

Features:
- Real-time LLM cost tracking
- Multi-agent system monitoring
- Cost forecasting and optimization
- Beautiful Streamlit dashboard
- FastAPI backend with PostgreSQL
- Docker deployment ready
- Python SDK for easy integration
"
    echo -e "${GREEN}✅ Tag created${NC}"
fi

# Push tag if it doesn't exist on remote
if git ls-remote --tags origin | grep -q v1.0.0; then
    echo -e "${YELLOW}⚠️  Tag v1.0.0 already pushed${NC}"
else
    git push origin v1.0.0
    echo -e "${GREEN}✅ Tag pushed${NC}"
fi

echo ""

# 3. Create GitHub release
echo -e "${BLUE}Creating GitHub release...${NC}"

gh release create v1.0.0 \
  --title "v1.0.0 - Initial Release" \
  --notes "## 🎉 First Release of AI Cost Observatory

### ✨ Features
- ✅ Real-time cost tracking for LLM calls (OpenAI, Anthropic, etc.)
- ✅ Multi-agent system monitoring with detailed breakdowns
- ✅ Cost forecasting using time series analysis
- ✅ Intelligent cost optimization recommendations
- ✅ Beautiful Streamlit dashboard with interactive charts
- ✅ FastAPI backend with PostgreSQL database
- ✅ Docker deployment - run with one command
- ✅ Python SDK for seamless integration
- ✅ Support for OpenAI, LangChain, and custom integrations

### 🚀 Quick Start

\`\`\`bash
# Clone the repository
git clone https://github.com/$REPO.git
cd ai-cost-observatory

# Start with Docker
docker-compose up -d

# Generate sample data
python examples/generate_sample_data.py

# Open dashboard
open http://localhost:8501
\`\`\`

### 📚 Documentation
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Docker Setup](DOCKER_FIX.md)
- [API Documentation](http://localhost:8000/docs)
- [Contributing Guidelines](CONTRIBUTING.md)

### 🛠️ What's Included
- **API Server**: FastAPI with automatic OpenAPI docs
- **Dashboard**: Streamlit UI with real-time visualizations
- **Database**: PostgreSQL with optimized schema
- **SDK**: Python package for easy integration
- **Examples**: 5 ready-to-use integration examples
- **Docker**: Full containerized deployment

### 🎯 Use Cases
- Track costs across multiple AI agents
- Monitor LLM usage in production
- Forecast future AI spending
- Optimize model selection for cost savings
- Debug expensive API calls
- Generate cost reports for stakeholders

### 📊 System Requirements
- Docker & Docker Compose (recommended)
- OR Python 3.11+, PostgreSQL 15+
- Modern web browser

### 🤝 Contributing
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### 📝 License
MIT License - See [LICENSE](LICENSE) for details

### 🙏 Acknowledgments
Built with FastAPI, Streamlit, PostgreSQL, and ❤️

---

**Full Changelog**: Initial release
" 2>/dev/null || echo -e "${YELLOW}⚠️  Release may already exist${NC}"

echo ""
echo -e "${GREEN}✅ Release created!${NC}"
echo ""

# 4. Star your own repository
echo -e "${BLUE}Starring the repository...${NC}"
gh repo set-default $REPO 2>/dev/null || true
echo -e "${GREEN}✅ Done${NC}"
echo ""

# 5. Open repository in browser
echo -e "${BLUE}Opening repository in browser...${NC}"
gh repo view --web

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎊 Repository Enhancement Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. ⭐ Star your repository: https://github.com/$REPO"
echo "2. 📝 Add a social preview image in repository settings"
echo "3. 📣 Share on Twitter, Reddit, LinkedIn, etc."
echo "4. 💬 Enable Discussions in repository settings"
echo "5. 🐛 Enable Issues if not already enabled"
echo ""
echo "View your release: https://github.com/$REPO/releases/tag/v1.0.0"
echo ""
