#!/bin/bash

# GitHub Repository Creation Helper Script
# This script will help you create and push to a GitHub repository

set -e

echo "🚀 GitHub Repository Setup for AI Cost Observatory"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✅ GitHub CLI (gh) is installed${NC}"
    echo ""
    
    # Check if authenticated
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✅ You are authenticated with GitHub${NC}"
        echo ""
        
        echo -e "${BLUE}Creating public repository 'ai-cost-observatory'...${NC}"
        
        # Create repository
        gh repo create ai-cost-observatory \
            --public \
            --source=. \
            --remote=origin \
            --description="Open-source observability layer for AI agents - Track, analyze, and optimize LLM costs in real-time" \
            --push
        
        echo ""
        echo -e "${GREEN}✅ Repository created and code pushed!${NC}"
        echo ""
        echo "🌐 View your repository at:"
        gh repo view --web
        
    else
        echo -e "${YELLOW}⚠️  You need to authenticate with GitHub${NC}"
        echo ""
        echo "Run: gh auth login"
        echo ""
        echo "Then run this script again."
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) is not installed${NC}"
    echo ""
    echo "Would you like to:"
    echo "1. Install GitHub CLI (recommended)"
    echo "2. Get manual instructions"
    echo ""
    read -p "Enter your choice (1 or 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo -e "${BLUE}Installing GitHub CLI...${NC}"
        brew install gh
        
        echo ""
        echo -e "${GREEN}✅ GitHub CLI installed!${NC}"
        echo ""
        echo "Now authenticate with GitHub:"
        echo "  gh auth login"
        echo ""
        echo "Then run this script again to create the repository."
    else
        echo ""
        echo -e "${BLUE}📋 Manual Instructions:${NC}"
        echo ""
        echo "1. Go to: https://github.com/new"
        echo ""
        echo "2. Fill in:"
        echo "   - Repository name: ai-cost-observatory"
        echo "   - Description: Open-source observability layer for AI agents"
        echo "   - Visibility: Public"
        echo "   - DO NOT initialize with README, .gitignore, or license"
        echo ""
        echo "3. After creating, run these commands:"
        echo ""
        echo -e "${GREEN}git remote add origin https://github.com/YOUR_USERNAME/ai-cost-observatory.git${NC}"
        echo -e "${GREEN}git push -u origin main${NC}"
        echo ""
        echo "Replace YOUR_USERNAME with your GitHub username"
        echo ""
        echo "For detailed instructions, see: GITHUB_SETUP.md"
    fi
fi
