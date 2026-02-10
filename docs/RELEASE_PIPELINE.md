# 🚀 GitHub Release Pipeline - Automated PyPI Publishing

This document explains the automated release and publishing workflow for AI Cost Observatory.

## 📋 Overview

When you create a GitHub release, the pipeline automatically:

1. ✅ **Builds** the Python package (wheel + source distribution)
2. ✅ **Validates** the package with twine
3. ✅ **Publishes to TestPyPI** (for verification)
4. ✅ **Publishes to PyPI** (production)
5. ✅ **Uploads assets** to GitHub release
6. ✅ **Notifies** on success with installation instructions

---

## 🔧 One-Time Setup

### Step 1: Create PyPI Accounts

If you haven't already:

**Production PyPI**:
- Visit: https://pypi.org/account/register/
- Verify email
- Enable 2FA

**TestPyPI** (optional but recommended):
- Visit: https://test.pypi.org/account/register/
- Verify email

---

### Step 2: Generate API Tokens

**For Production PyPI**:
1. Go to: https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `ai-cost-observatory-github`
4. Scope: "Entire account" (or project-specific after first upload)
5. **Copy the token** (starts with `pypi-`)

**For TestPyPI** (optional):
1. Go to: https://test.pypi.org/manage/account/token/
2. Follow same steps
3. Token name: `ai-cost-observatory-github-test`
4. **Copy the token**

⚠️ **Save these securely!** You'll only see them once.

---

### Step 3: Add GitHub Secrets

Add the API tokens to your GitHub repository:

1. Go to: https://github.com/Sabyasachig/ai-cost-observatory/settings/secrets/actions

2. Click **"New repository secret"**

3. Add **PYPI_API_TOKEN**:
   - Name: `PYPI_API_TOKEN`
   - Value: Your production PyPI token (starts with `pypi-`)
   - Click "Add secret"

4. Add **TEST_PYPI_API_TOKEN** (optional):
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: Your TestPyPI token
   - Click "Add secret"

---

## 🎯 How to Create a Release

### Method 1: Using GitHub CLI (Recommended)

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory

# Update version number first!
# Edit sdk/setup.py and sdk/pyproject.toml

# Commit changes
git add sdk/setup.py sdk/pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.0.0"
git push origin main

# Create tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Create GitHub release
gh release create v1.0.0 \
  --title "v1.0.0 - Initial Release" \
  --notes "## 🎉 First Official Release

### Installation
\`\`\`bash
pip install ai-cost-observatory
\`\`\`

### Features
- ✅ Real-time LLM cost tracking
- ✅ Multi-agent system monitoring
- ✅ Cost forecasting and optimization
- ✅ Beautiful Streamlit dashboard
- ✅ FastAPI backend with PostgreSQL
- ✅ Docker deployment ready
- ✅ LangChain integration

### Quick Start
\`\`\`python
from ai_observer import observe

with observe(project=\"my-app\"):
    # Your LLM calls here
    pass
\`\`\`

### Documentation
- [Getting Started](docs/GETTING_STARTED.md)
- [PyPI Package](https://pypi.org/project/ai-cost-observatory/)
- [GitHub Repository](https://github.com/Sabyasachig/ai-cost-observatory)
"
```

### Method 2: Using GitHub Web Interface

1. **Update Version** (locally):
   ```bash
   # Edit sdk/setup.py: version="1.0.0"
   # Edit sdk/pyproject.toml: version = "1.0.0"
   # Update CHANGELOG.md
   
   git add sdk/ CHANGELOG.md
   git commit -m "Bump version to 1.0.0"
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin main
   git push origin v1.0.0
   ```

2. **Create Release** (on GitHub):
   - Go to: https://github.com/Sabyasachig/ai-cost-observatory/releases/new
   - Choose tag: `v1.0.0`
   - Release title: `v1.0.0 - Initial Release`
   - Add release notes (see template above)
   - Check "Set as the latest release"
   - Click **"Publish release"**

---

## ⚙️ What Happens After Publishing

### Automatic Pipeline Execution

1. **Build Job** (1-2 minutes):
   - Checks out code
   - Sets up Python 3.11
   - Installs build tools
   - Builds wheel and source distribution
   - Validates with twine
   - Uploads artifacts

2. **TestPyPI Job** (1 minute):
   - Downloads build artifacts
   - Publishes to test.pypi.org
   - Available at: https://test.pypi.org/project/ai-cost-observatory/

3. **PyPI Job** (1 minute):
   - Waits for TestPyPI success
   - Downloads build artifacts
   - Publishes to pypi.org
   - Available at: https://pypi.org/project/ai-cost-observatory/

4. **Release Assets Job** (30 seconds):
   - Uploads `.whl` file to GitHub release
   - Uploads `.tar.gz` file to GitHub release
   - Users can download directly from release page

5. **Notification Job** (10 seconds):
   - Posts success comment
   - Includes installation instructions
   - Links to PyPI and TestPyPI

**Total Time**: ~4-5 minutes

---

## 📊 Monitoring the Pipeline

### Check Workflow Status

1. Go to: https://github.com/Sabyasachig/ai-cost-observatory/actions

2. Look for "Release & Publish to PyPI" workflow

3. Click on the running/completed workflow to see:
   - ✅ Build status
   - ✅ TestPyPI publish status
   - ✅ PyPI publish status
   - ✅ Release assets upload
   - ✅ Notification status

### View Logs

Click on any job to see detailed logs:
- Build output
- Package validation
- Upload progress
- Any errors

---

## ✅ Verification After Release

### 1. Check PyPI

Visit: https://pypi.org/project/ai-cost-observatory/

Verify:
- ✅ Correct version number
- ✅ README renders correctly
- ✅ Project links work
- ✅ Installation command shown

### 2. Test Installation

```bash
# Create test environment
python3 -m venv test_release
source test_release/bin/activate

# Install from PyPI
pip install ai-cost-observatory

# Test import
python -c "from ai_observer import observe; print('✅ Release successful!')"

# Check version
python -c "import ai_observer; print(f'Version: {ai_observer.__version__}')"

# Cleanup
deactivate
rm -rf test_release
```

### 3. Check GitHub Release

Visit: https://github.com/Sabyasachig/ai-cost-observatory/releases

Verify:
- ✅ Release shows up
- ✅ Assets attached (wheel + tar.gz)
- ✅ Release notes display correctly
- ✅ Tagged correctly

---

## 🔄 Updating to a New Version

### Patch Release (1.0.0 → 1.0.1)

For bug fixes:

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory

# 1. Update version numbers
sed -i '' 's/version="1.0.0"/version="1.0.1"/' sdk/setup.py
sed -i '' 's/version = "1.0.0"/version = "1.0.1"/' sdk/pyproject.toml

# 2. Update CHANGELOG.md
cat >> CHANGELOG.md << 'EOF'

## [1.0.1] - 2026-02-11

### Fixed
- Bug fix description here

EOF

# 3. Commit and tag
git add sdk/setup.py sdk/pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.0.1"
git push origin main

git tag -a v1.0.1 -m "Release v1.0.1 - Bug fixes"
git push origin v1.0.1

# 4. Create release
gh release create v1.0.1 \
  --title "v1.0.1 - Bug Fixes" \
  --notes "## 🐛 Bug Fix Release

### Fixed
- Bug fix description

### Installation
\`\`\`bash
pip install --upgrade ai-cost-observatory
\`\`\`
"
```

### Minor Release (1.0.0 → 1.1.0)

For new features:

```bash
# Update to version 1.1.0
sed -i '' 's/version="1.0.0"/version="1.1.0"/' sdk/setup.py
sed -i '' 's/version = "1.0.0"/version = "1.1.0"/' sdk/pyproject.toml

# Rest of the process is the same
```

### Major Release (1.0.0 → 2.0.0)

For breaking changes:

```bash
# Update to version 2.0.0
sed -i '' 's/version="1.0.0"/version="2.0.0"/' sdk/setup.py
sed -i '' 's/version = "1.0.0"/version = "2.0.0"/' sdk/pyproject.toml

# Include migration guide in release notes
```

---

## 🛠️ Troubleshooting

### Pipeline Fails at Build

**Check**:
- `sdk/setup.py` has valid Python syntax
- `pyproject.toml` has valid TOML syntax
- All required files exist (README.md, LICENSE)

**Fix**:
```bash
cd sdk
python -m build  # Test locally
twine check dist/*  # Validate
```

### Pipeline Fails at TestPyPI Upload

**Error: "403 Forbidden"**
- Check `TEST_PYPI_API_TOKEN` secret is set correctly
- Verify token hasn't expired
- Try regenerating token

**Error: "File already exists"**
- Version already published to TestPyPI
- Increment version number and try again

### Pipeline Fails at PyPI Upload

**Error: "403 Forbidden"**
- Check `PYPI_API_TOKEN` secret is set correctly
- Verify token has correct permissions
- For first upload, token must have "Entire account" scope

**Error: "File already exists"**
- Version already published to PyPI
- **Cannot overwrite!** Must increment version

### Release Assets Not Uploading

**Check**:
- Repository has `contents: write` permission
- `GITHUB_TOKEN` is available (automatic in GitHub Actions)
- Files exist in dist/ directory

---

## 🔐 Security Best Practices

### API Token Management

1. **Use Separate Tokens**:
   - Different token for GitHub Actions vs local development
   - Easier to rotate without breaking workflows

2. **Minimum Permissions**:
   - After first upload, create project-specific tokens
   - Change scope from "Entire account" to specific project

3. **Token Rotation**:
   - Rotate tokens every 6-12 months
   - Update GitHub secrets when rotating

4. **Never Commit Tokens**:
   - Always use GitHub Secrets
   - Don't hardcode in workflow files

### GitHub Secrets

- Only accessible to workflows
- Masked in logs (shown as ***)
- Encrypted at rest

---

## 📈 Best Practices

### Before Every Release

- [ ] Update version in `setup.py` and `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run tests locally: `cd tests && pytest -v`
- [ ] Test package build: `cd sdk && python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] All changes committed and pushed
- [ ] Create git tag with version

### Release Notes Template

Use this template for consistent release notes:

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

### Deprecated
- Features that will be removed

### Removed
- Features that were removed

### Security
- Security updates

### Installation
\`\`\`bash
pip install ai-cost-observatory
\`\`\`

### Upgrade
\`\`\`bash
pip install --upgrade ai-cost-observatory
\`\`\`
```

---

## 🎯 Quick Reference

### Common Commands

```bash
# Update version
sed -i '' 's/version="1.0.0"/version="1.0.1"/' sdk/setup.py
sed -i '' 's/version = "1.0.0"/version = "1.0.1"/' sdk/pyproject.toml

# Create and push tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1

# Create release with gh CLI
gh release create v1.0.1 --title "v1.0.1" --notes "Release notes"

# Check workflow status
gh run list --workflow=release-publish.yml

# View workflow logs
gh run view [run-id] --log
```

### Useful Links

- **Actions**: https://github.com/Sabyasachig/ai-cost-observatory/actions
- **Releases**: https://github.com/Sabyasachig/ai-cost-observatory/releases
- **Secrets**: https://github.com/Sabyasachig/ai-cost-observatory/settings/secrets/actions
- **PyPI**: https://pypi.org/project/ai-cost-observatory/
- **TestPyPI**: https://test.pypi.org/project/ai-cost-observatory/

---

## 📊 Success Metrics

After setting up automated releases:

### Workflow Metrics
- ⏱️ Average release time: ~4-5 minutes
- ✅ Success rate: Target 95%+
- 🔄 Releases per month: Track growth

### Package Metrics
- 📥 PyPI downloads: https://pepy.tech/project/ai-cost-observatory
- ⭐ GitHub stars: Track community interest
- 🐛 Issues/PRs: Community engagement

---

## 🎓 What This Demonstrates

**Professional DevOps Skills**:

✅ Automated release management  
✅ CI/CD pipeline design  
✅ Package distribution automation  
✅ GitHub Actions expertise  
✅ Security best practices (secrets management)  
✅ Version management  
✅ Release documentation  

**This is production-grade automation!** 🚀

---

## ✅ Final Checklist

### Setup (One-Time)
- [ ] Created PyPI account and verified email
- [ ] Created TestPyPI account (optional)
- [ ] Generated PyPI API token
- [ ] Generated TestPyPI API token (optional)
- [ ] Added `PYPI_API_TOKEN` to GitHub secrets
- [ ] Added `TEST_PYPI_API_TOKEN` to GitHub secrets (optional)
- [ ] Workflow file committed and pushed

### Each Release
- [ ] Updated version numbers
- [ ] Updated CHANGELOG.md
- [ ] Committed all changes
- [ ] Created and pushed git tag
- [ ] Created GitHub release
- [ ] Monitored pipeline execution
- [ ] Verified on PyPI
- [ ] Tested installation
- [ ] Announced release (optional)

---

**Ready to automate your releases? Create your first one with the commands above!** 🎉
