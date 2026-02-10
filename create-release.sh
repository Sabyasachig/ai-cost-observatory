#!/bin/bash

# AI Cost Observatory - Release Helper Script
# Automates the release process

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}║       🚀 AI Cost Observatory - Release Helper             ║${NC}"
echo -e "${BLUE}║                                                           ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed.${NC}"
    echo ""
    echo "Install with:"
    echo "  brew install gh"
    echo ""
    echo "Or visit: https://cli.github.com/"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "sdk/setup.py" ]; then
    echo -e "${RED}❌ Please run this script from the project root directory${NC}"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(grep -E 'version="[0-9]+\.[0-9]+\.[0-9]+"' sdk/setup.py | sed -E 's/.*version="([0-9]+\.[0-9]+\.[0-9]+)".*/\1/')
echo -e "${GREEN}Current version: ${CURRENT_VERSION}${NC}"
echo ""

# Ask for new version
echo -e "${YELLOW}What type of release?${NC}"
echo "  1) Patch (bug fixes):    ${CURRENT_VERSION} → $(echo $CURRENT_VERSION | awk -F. '{print $1"."$2"."$3+1}')"
echo "  2) Minor (new features): ${CURRENT_VERSION} → $(echo $CURRENT_VERSION | awk -F. '{print $1"."$2+1".0"}')"
echo "  3) Major (breaking):     ${CURRENT_VERSION} → $(echo $CURRENT_VERSION | awk -F. '{print $1+1".0.0"}')"
echo "  4) Custom version"
echo "  5) Cancel"
echo ""
read -p "Enter choice (1-5): " CHOICE

case $CHOICE in
    1)
        NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."$2"."$3+1}')
        RELEASE_TYPE="Patch Release"
        ;;
    2)
        NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1"."$2+1".0"}')
        RELEASE_TYPE="Minor Release"
        ;;
    3)
        NEW_VERSION=$(echo $CURRENT_VERSION | awk -F. '{print $1+1".0.0"}')
        RELEASE_TYPE="Major Release"
        ;;
    4)
        read -p "Enter new version (e.g., 1.2.3): " NEW_VERSION
        RELEASE_TYPE="Custom Release"
        ;;
    5)
        echo "Cancelled."
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}New version will be: ${NEW_VERSION}${NC}"
echo ""

# Confirm
read -p "Continue with release v${NEW_VERSION}? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Starting Release Process${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Step 1: Update version in setup.py
echo -e "${YELLOW}[1/7] Updating version in sdk/setup.py...${NC}"
sed -i '' "s/version=\"$CURRENT_VERSION\"/version=\"$NEW_VERSION\"/" sdk/setup.py
echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 2: Update version in pyproject.toml
echo -e "${YELLOW}[2/7] Updating version in sdk/pyproject.toml...${NC}"
sed -i '' "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" sdk/pyproject.toml
echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 3: Update CHANGELOG
echo -e "${YELLOW}[3/7] Updating CHANGELOG.md...${NC}"
DATE=$(date +%Y-%m-%d)

# Ask for changelog entry
echo ""
echo "Enter changes for this release (one per line, empty line to finish):"
echo "Example:"
echo "  - Added new feature X"
echo "  - Fixed bug Y"
echo "  - Improved performance Z"
echo ""

CHANGES=""
while true; do
    read -p "> " LINE
    if [ -z "$LINE" ]; then
        break
    fi
    CHANGES="${CHANGES}${LINE}\n"
done

# Create changelog entry
cat > /tmp/changelog_entry.txt << EOF

## [${NEW_VERSION}] - ${DATE}

${CHANGES}
EOF

# Prepend to CHANGELOG.md
cat /tmp/changelog_entry.txt CHANGELOG.md > /tmp/CHANGELOG_new.md
mv /tmp/CHANGELOG_new.md CHANGELOG.md
rm /tmp/changelog_entry.txt

echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 4: Commit changes
echo -e "${YELLOW}[4/7] Committing changes...${NC}"
git add sdk/setup.py sdk/pyproject.toml CHANGELOG.md
git commit -m "Bump version to ${NEW_VERSION}"
echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 5: Create tag
echo -e "${YELLOW}[5/7] Creating git tag v${NEW_VERSION}...${NC}"
git tag -a "v${NEW_VERSION}" -m "Release v${NEW_VERSION}"
echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 6: Push
echo -e "${YELLOW}[6/7] Pushing to GitHub...${NC}"
git push origin main
git push origin "v${NEW_VERSION}"
echo -e "${GREEN}✅ Done${NC}"
echo ""

# Step 7: Create GitHub release
echo -e "${YELLOW}[7/7] Creating GitHub release...${NC}"

# Create release notes
RELEASE_NOTES="## ${RELEASE_TYPE}

${CHANGES}

### Installation
\`\`\`bash
pip install ai-cost-observatory
\`\`\`

### Upgrade
\`\`\`bash
pip install --upgrade ai-cost-observatory
\`\`\`

### Quick Start
\`\`\`python
from ai_observer import observe

with observe(project=\"my-app\"):
    # Your LLM calls here
    pass
\`\`\`

### Links
- **PyPI**: https://pypi.org/project/ai-cost-observatory/
- **Documentation**: https://github.com/Sabyasachig/ai-cost-observatory#readme
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
"

gh release create "v${NEW_VERSION}" \
  --title "v${NEW_VERSION}" \
  --notes "$RELEASE_NOTES"

echo -e "${GREEN}✅ Done${NC}"
echo ""

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}🎉 Release Created Successfully!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

echo -e "${GREEN}Version: v${NEW_VERSION}${NC}"
echo -e "${GREEN}Release: https://github.com/Sabyasachig/ai-cost-observatory/releases/tag/v${NEW_VERSION}${NC}"
echo ""

echo -e "${YELLOW}The automated pipeline will now:${NC}"
echo "  1. Build the package"
echo "  2. Publish to TestPyPI"
echo "  3. Publish to PyPI"
echo "  4. Upload release assets"
echo ""

echo "Monitor progress at:"
echo -e "${BLUE}https://github.com/Sabyasachig/ai-cost-observatory/actions${NC}"
echo ""

echo -e "${YELLOW}In ~5 minutes, your package will be available:${NC}"
echo -e "${GREEN}pip install ai-cost-observatory${NC}"
echo ""

echo "✨ Happy releasing! ✨"
