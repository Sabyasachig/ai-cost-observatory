#!/bin/bash

# PyPI Publishing Quick Start Script
# This script helps you publish ai-cost-observatory to PyPI

set -e

echo "📦 AI Cost Observatory - PyPI Publishing Helper"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "sdk/setup.py" ]; then
    echo -e "${RED}Error: Must run from ai_cost_observatory root directory${NC}"
    exit 1
fi

echo "Select an option:"
echo "1. Test on TestPyPI (recommended first)"
echo "2. Publish to Production PyPI"
echo "3. Just build (no upload)"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}Publishing to TestPyPI...${NC}"
        echo ""
        
        # Check for build and twine
        if ! command -v python -m build &> /dev/null; then
            echo -e "${YELLOW}Installing build tools...${NC}"
            pip install --upgrade build twine
        fi
        
        cd sdk
        
        # Clean old builds
        echo -e "${BLUE}Cleaning old builds...${NC}"
        rm -rf build/ dist/ *.egg-info/
        
        # Build
        echo -e "${BLUE}Building package...${NC}"
        python -m build
        
        # Check
        echo -e "${BLUE}Checking package...${NC}"
        twine check dist/*
        
        # Upload
        echo -e "${BLUE}Uploading to TestPyPI...${NC}"
        echo ""
        echo -e "${YELLOW}You'll need your TestPyPI API token.${NC}"
        echo -e "${YELLOW}Get it from: https://test.pypi.org/manage/account/token/${NC}"
        echo ""
        twine upload --repository testpypi dist/*
        
        echo ""
        echo -e "${GREEN}✅ Published to TestPyPI!${NC}"
        echo ""
        echo "Test installation with:"
        echo -e "${GREEN}pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cost-observatory${NC}"
        echo ""
        echo "View at: https://test.pypi.org/project/ai-cost-observatory/"
        ;;
    
    2)
        echo -e "${YELLOW}⚠️  WARNING: Publishing to Production PyPI${NC}"
        echo ""
        echo "This will make the package publicly available."
        echo "Make sure you've:"
        echo "  - Tested on TestPyPI first"
        echo "  - Updated version number"
        echo "  - Committed all changes"
        echo "  - Created a git tag"
        echo ""
        read -p "Are you sure? (yes/no): " confirm
        
        if [ "$confirm" != "yes" ]; then
            echo "Aborted."
            exit 0
        fi
        
        echo -e "${BLUE}Publishing to PyPI...${NC}"
        echo ""
        
        # Check for build and twine
        if ! command -v python -m build &> /dev/null; then
            echo -e "${YELLOW}Installing build tools...${NC}"
            pip install --upgrade build twine
        fi
        
        cd sdk
        
        # Clean old builds
        echo -e "${BLUE}Cleaning old builds...${NC}"
        rm -rf build/ dist/ *.egg-info/
        
        # Build
        echo -e "${BLUE}Building package...${NC}"
        python -m build
        
        # Check
        echo -e "${BLUE}Checking package...${NC}"
        twine check dist/*
        
        # Upload
        echo -e "${BLUE}Uploading to PyPI...${NC}"
        echo ""
        echo -e "${YELLOW}You'll need your PyPI API token.${NC}"
        echo -e "${YELLOW}Get it from: https://pypi.org/manage/account/token/${NC}"
        echo ""
        twine upload dist/*
        
        echo ""
        echo -e "${GREEN}✅ Published to PyPI!${NC}"
        echo ""
        echo "Your package is now available:"
        echo -e "${GREEN}pip install ai-cost-observatory${NC}"
        echo ""
        echo "View at: https://pypi.org/project/ai-cost-observatory/"
        ;;
    
    3)
        echo -e "${BLUE}Building package...${NC}"
        echo ""
        
        # Check for build tools
        if ! command -v python -m build &> /dev/null; then
            echo -e "${YELLOW}Installing build tools...${NC}"
            pip install --upgrade build twine
        fi
        
        cd sdk
        
        # Clean old builds
        echo -e "${BLUE}Cleaning old builds...${NC}"
        rm -rf build/ dist/ *.egg-info/
        
        # Build
        python -m build
        
        # Check
        echo -e "${BLUE}Checking package...${NC}"
        twine check dist/*
        
        echo ""
        echo -e "${GREEN}✅ Package built successfully!${NC}"
        echo ""
        echo "Files created in sdk/dist/:"
        ls -lh dist/
        ;;
    
    4)
        echo "Exited."
        exit 0
        ;;
    
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Done!${NC}"
echo ""
echo "For detailed instructions, see:"
echo "  docs/PYPI_PUBLISHING.md"
