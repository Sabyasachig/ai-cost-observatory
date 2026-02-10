# 📦 Publishing to PyPI - Complete Guide

This guide will walk you through publishing `ai-cost-observatory` to PyPI so users can install it with:

```bash
pip install ai-cost-observatory
```

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Testing on TestPyPI](#testing-on-testpypi)
4. [Publishing to PyPI](#publishing-to-pypi)
5. [Post-Publication](#post-publication)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Create PyPI Accounts

**Main PyPI** (production):
- Visit: https://pypi.org/account/register/
- Verify your email
- Enable 2FA (recommended)

**TestPyPI** (testing):
- Visit: https://test.pypi.org/account/register/
- Verify your email

### 2. Generate API Tokens

**For PyPI**:
1. Go to: https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `ai-cost-observatory`
4. Scope: "Entire account" (or specific project after first upload)
5. Copy and save the token (starts with `pypi-`)

**For TestPyPI**:
1. Go to: https://test.pypi.org/manage/account/token/
2. Follow same steps as above
3. Save this token separately

⚠️ **Important**: Save these tokens securely! You won't be able to see them again.

### 3. Install Required Tools

```bash
# Install build and upload tools
pip install --upgrade pip
pip install --upgrade build twine
```

---

## Setup

### 1. Configure PyPI Credentials

Create `~/.pypirc` file with your tokens:

```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
EOF

# Secure the file
chmod 600 ~/.pypirc
```

Replace `pypi-YOUR_PYPI_TOKEN_HERE` and `pypi-YOUR_TESTPYPI_TOKEN_HERE` with your actual tokens.

### 2. Navigate to SDK Directory

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory/sdk
```

---

## Testing on TestPyPI

**Always test on TestPyPI first!**

### Step 1: Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### Step 2: Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates:
- `dist/ai_cost_observatory-1.0.0.tar.gz` (source distribution)
- `dist/ai_cost_observatory-1.0.0-py3-none-any.whl` (wheel)

### Step 3: Check the Package

```bash
# Verify package metadata and structure
twine check dist/*
```

You should see:
```
Checking dist/ai_cost_observatory-1.0.0-py3-none-any.whl: PASSED
Checking dist/ai_cost_observatory-1.0.0.tar.gz: PASSED
```

### Step 4: Upload to TestPyPI

```bash
# Upload to test.pypi.org
twine upload --repository testpypi dist/*
```

Output should show:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading ai_cost_observatory-1.0.0-py3-none-any.whl
Uploading ai_cost_observatory-1.0.0.tar.gz
```

### Step 5: Test Installation from TestPyPI

```bash
# Create a test virtual environment
cd /tmp
python -m venv test_pypi_install
source test_pypi_install/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ ai-cost-observatory

# Test import
python -c "from ai_observer import observe; print('✅ Import successful!')"

# Deactivate and cleanup
deactivate
rm -rf test_pypi_install
```

✅ If this works, you're ready for production PyPI!

---

## Publishing to PyPI

### Step 1: Ensure Everything is Committed

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory
git status
git add sdk/
git commit -m "Prepare SDK for PyPI publication"
git push origin main
```

### Step 2: Create a Git Tag

```bash
# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0 - PyPI publication"
git push origin v1.0.0
```

### Step 3: Build for Production

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory/sdk

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build fresh
python -m build

# Verify
twine check dist/*
```

### Step 4: Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

You'll see:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading ai_cost_observatory-1.0.0-py3-none-any.whl
Uploading ai_cost_observatory-1.0.0.tar.gz

View at:
https://pypi.org/project/ai-cost-observatory/1.0.0/
```

### Step 5: Verify on PyPI

Visit: https://pypi.org/project/ai-cost-observatory/

You should see your package with:
- ✅ Description
- ✅ Installation command
- ✅ Project links
- ✅ Classifiers

### Step 6: Test Production Installation

```bash
# Create fresh venv
cd /tmp
python -m venv test_prod_install
source test_prod_install/bin/activate

# Install from PyPI
pip install ai-cost-observatory

# Test
python -c "from ai_observer import observe; print('✅ Production install works!')"

# Cleanup
deactivate
rm -rf test_prod_install
```

---

## Post-Publication

### 1. Update README

Add installation badge to your README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/ai-cost-observatory.svg)](https://badge.fury.io/py/ai-cost-observatory)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-cost-observatory.svg)](https://pypi.org/project/ai-cost-observatory/)
[![Downloads](https://pepy.tech/badge/ai-cost-observatory)](https://pepy.tech/project/ai-cost-observatory)
```

### 2. Update Documentation

Update all documentation to use the new install command:

```bash
pip install ai-cost-observatory
```

Instead of:
```bash
cd sdk && pip install -e .
```

### 3. Create GitHub Release

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory

gh release create v1.0.0 \
  --title "v1.0.0 - PyPI Release" \
  --notes "## 🎉 Now Available on PyPI!

Install with:
\`\`\`bash
pip install ai-cost-observatory
\`\`\`

### What's New
- 📦 Published to PyPI for easy installation
- 🔧 Improved package metadata
- 📚 Enhanced documentation
- ✅ Tested on Python 3.8-3.12

### PyPI Package
https://pypi.org/project/ai-cost-observatory/

### Quick Start
\`\`\`python
from ai_observer import observe

with observe(project=\"my-app\"):
    # Your LLM calls here
    pass
\`\`\`
"
```

### 4. Announce on Social Media

Share on:
- Twitter/X: "🎉 ai-cost-observatory is now on PyPI! `pip install ai-cost-observatory`"
- Reddit: r/Python, r/MachineLearning
- LinkedIn
- Hacker News (if appropriate)

---

## Updating the Package (Future Releases)

### For Bug Fixes (Patch Release: 1.0.0 → 1.0.1)

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory/sdk

# 1. Update version in setup.py and pyproject.toml
sed -i '' 's/version="1.0.0"/version="1.0.1"/' setup.py
sed -i '' 's/version = "1.0.0"/version = "1.0.1"/' pyproject.toml

# 2. Update CHANGELOG.md

# 3. Build and upload
rm -rf build/ dist/ *.egg-info/
python -m build
twine check dist/*
twine upload dist/*

# 4. Git tag
cd ..
git add .
git commit -m "Release v1.0.1 - Bug fixes"
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main v1.0.1
```

### For New Features (Minor Release: 1.0.0 → 1.1.0)

Same process, but update version to `1.1.0`

### For Breaking Changes (Major Release: 1.0.0 → 2.0.0)

Same process, but update version to `2.0.0`

---

## Troubleshooting

### Error: "403 Forbidden"

**Cause**: Incorrect API token or permissions

**Fix**:
1. Verify token in `~/.pypirc`
2. Ensure token has correct scope
3. Try uploading with explicit token:
   ```bash
   twine upload -u __token__ -p pypi-YOUR_TOKEN dist/*
   ```

### Error: "Package already exists"

**Cause**: Version number already uploaded

**Fix**:
1. You cannot re-upload the same version
2. Increment version number in `setup.py` and `pyproject.toml`
3. Rebuild and upload

### Error: "Invalid distribution"

**Cause**: Package structure issues

**Fix**:
1. Run `twine check dist/*` to see specific errors
2. Ensure `__init__.py` exists in all package directories
3. Check `MANIFEST.in` includes all necessary files

### Error: "README rendering failed"

**Cause**: Invalid Markdown in README.md

**Fix**:
1. Test README rendering: https://github.com/pypa/readme_renderer
2. Install: `pip install readme-renderer`
3. Check: `python -m readme_renderer README.md`

### Package Not Found After Upload

**Wait**: It can take 1-5 minutes for PyPI to index new packages

**Check**:
1. Visit: https://pypi.org/project/ai-cost-observatory/
2. Search: https://pypi.org/search/?q=ai-cost-observatory

---

## Security Best Practices

1. **Never commit tokens to git**
   - Add `~/.pypirc` to global `.gitignore`
   - Use environment variables in CI/CD

2. **Use scoped tokens**
   - Create project-specific tokens after first upload
   - Limit scope to specific project

3. **Enable 2FA**
   - PyPI requires 2FA for new projects
   - Use authenticator app (not SMS)

4. **Rotate tokens regularly**
   - Change tokens every 6-12 months
   - Revoke old tokens

---

## Checklist

Before publishing:
- [ ] Updated version number in `setup.py` and `pyproject.toml`
- [ ] Updated `CHANGELOG.md`
- [ ] All tests passing
- [ ] README.md is up to date
- [ ] LICENSE file included
- [ ] Git committed and tagged
- [ ] Tested on TestPyPI
- [ ] `twine check` passes

After publishing:
- [ ] Package appears on PyPI
- [ ] Can install: `pip install ai-cost-observatory`
- [ ] Import works: `from ai_observer import observe`
- [ ] Updated GitHub README with PyPI badge
- [ ] Created GitHub release
- [ ] Announced on social media

---

## Useful Commands

```bash
# Check package info
pip show ai-cost-observatory

# View package files
pip show --files ai-cost-observatory

# Check latest version on PyPI
pip index versions ai-cost-observatory

# Uninstall
pip uninstall ai-cost-observatory

# Install specific version
pip install ai-cost-observatory==1.0.0

# Install with extras
pip install ai-cost-observatory[langchain]
pip install ai-cost-observatory[dev]
```

---

## Resources

- **PyPI Help**: https://pypi.org/help/
- **Packaging Tutorial**: https://packaging.python.org/tutorials/packaging-projects/
- **Twine Documentation**: https://twine.readthedocs.io/
- **setuptools Documentation**: https://setuptools.pypa.io/

---

**Ready to publish? Start with [Testing on TestPyPI](#testing-on-testpypi)!** 🚀
