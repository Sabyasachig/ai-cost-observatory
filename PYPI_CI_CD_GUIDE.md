# 🚀 PyPI & CI/CD Setup Guide - Quick Reference

This document provides a quick overview of publishing to PyPI and setting up CI/CD.

## 📦 Part 1: Publishing to PyPI

### Quick Steps

1. **Create PyPI Accounts**
   - Production: https://pypi.org/account/register/
   - Testing: https://test.pypi.org/account/register/

2. **Get API Tokens**
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

3. **Run the Helper Script**
   ```bash
   ./publish-to-pypi.sh
   ```
   
   Choose option 1 (TestPyPI) first, then option 2 (Production PyPI)

4. **Manual Method** (if you prefer):
   ```bash
   cd sdk
   pip install --upgrade build twine
   python -m build
   twine upload --repository testpypi dist/*  # Test first
   twine upload dist/*                         # Then production
   ```

### After Publishing

Add to README.md:
```markdown
[![PyPI version](https://badge.fury.io/py/ai-cost-observatory.svg)](https://badge.fury.io/py/ai-cost-observatory)
[![Python Versions](https://img.shields.io/pypi/pyversions/ai-cost-observatory.svg)](https://pypi.org/project/ai-cost-observatory/)
```

Users can now install with:
```bash
pip install ai-cost-observatory
```

**Detailed Guide**: [docs/PYPI_PUBLISHING.md](docs/PYPI_PUBLISHING.md)

---

## 🔄 Part 2: Setting Up CI/CD

### Quick Steps

1. **Enable GitHub Actions**
   - Go to: https://github.com/Sabyasachig/ai-cost-observatory/settings/actions
   - Enable "Allow all actions"

2. **Add PyPI Token to GitHub Secrets** (optional, for auto-publishing)
   - Go to: https://github.com/Sabyasachig/ai-cost-observatory/settings/secrets/actions
   - Add secret: `PYPI_API_TOKEN` = your PyPI token

3. **Push the Workflow**
   ```bash
   git add .github/workflows/ci-cd.yml
   git commit -m "Add CI/CD pipeline"
   git push origin main
   ```

4. **Verify It Works**
   - Go to: https://github.com/Sabyasachig/ai-cost-observatory/actions
   - Watch the workflow run
   - All jobs should pass ✅

### CI/CD Pipeline Jobs

Our pipeline runs 5 jobs:

1. **Test** - Runs on Python 3.8-3.12
2. **Lint** - Checks code quality (Black, flake8, isort)
3. **Docker** - Builds and tests containers
4. **Build** - Creates Python package
5. **Publish** - Deploys to PyPI (only on releases)

### Add Status Badge

After first successful run, add to README.md:
```markdown
[![CI/CD Pipeline](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml)
```

**Detailed Guide**: [docs/CI_CD_SETUP.md](docs/CI_CD_SETUP.md)

---

## 📋 Complete Checklist

### Before Publishing to PyPI

- [ ] Create PyPI and TestPyPI accounts
- [ ] Get API tokens
- [ ] Update version in `sdk/setup.py` and `sdk/pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Test locally: `cd tests && pytest -v`
- [ ] Commit all changes
- [ ] Create git tag: `git tag v1.0.0`

### Publishing Process

- [ ] Test on TestPyPI first: `./publish-to-pypi.sh` → option 1
- [ ] Install and test from TestPyPI
- [ ] Publish to production PyPI: `./publish-to-pypi.sh` → option 2
- [ ] Verify package appears: https://pypi.org/project/ai-cost-observatory/
- [ ] Test installation: `pip install ai-cost-observatory`
- [ ] Push git tag: `git push origin v1.0.0`

### Setting Up CI/CD

- [ ] Enable GitHub Actions in repository settings
- [ ] Push workflow file: `.github/workflows/ci-cd.yml`
- [ ] Verify workflow runs successfully
- [ ] Add `PYPI_API_TOKEN` secret (for auto-publishing)
- [ ] Add status badges to README
- [ ] Test by creating a pull request

### Post-Setup

- [ ] Update README with PyPI installation instructions
- [ ] Update README with status badges
- [ ] Create GitHub release
- [ ] Announce on social media
- [ ] Update documentation to reference PyPI package

---

## 🎯 What This Achieves

### Before
```bash
# Users had to:
git clone https://github.com/Sabyasachig/ai-cost-observatory.git
cd ai-cost-observatory/sdk
pip install -e .
```

### After PyPI
```bash
# Users can simply:
pip install ai-cost-observatory
```

### Before CI/CD
- Manual testing on every push
- No automated quality checks
- Manual deployments
- No visibility into build status

### After CI/CD
- ✅ Automatic tests on every push/PR
- ✅ Code quality checks enforced
- ✅ Docker builds validated
- ✅ Automated PyPI publishing on releases
- ✅ Status badges show build health
- ✅ Pull requests show test results

---

## 📁 Files Created

```
ai_cost_observatory/
├── .github/
│   └── workflows/
│       └── ci-cd.yml              # ✅ GitHub Actions workflow
│
├── sdk/
│   ├── setup.py                   # ✅ Updated with metadata
│   ├── pyproject.toml             # ✅ Modern Python packaging
│   └── MANIFEST.in                # ✅ Package file inclusion
│
├── docs/
│   ├── PYPI_PUBLISHING.md         # ✅ Detailed PyPI guide
│   └── CI_CD_SETUP.md             # ✅ Detailed CI/CD guide
│
└── publish-to-pypi.sh             # ✅ Helper script
```

---

## 🆘 Quick Troubleshooting

### PyPI Upload Fails

**Error**: "403 Forbidden"
```bash
# Check token in ~/.pypirc or use explicit token:
twine upload -u __token__ -p pypi-YOUR_TOKEN dist/*
```

**Error**: "Package already exists"
```bash
# Increment version in sdk/setup.py and sdk/pyproject.toml
# Then rebuild and upload
```

### CI/CD Fails

**Tests fail**
```bash
# Run locally first:
cd tests && pytest -v
```

**Docker build fails**
```bash
# Test locally:
docker-compose up
```

**Linting fails**
```bash
# Fix code style:
cd sdk && black ai_observer/
cd ../server && black .
```

---

## 📚 Resources

- **PyPI Guide**: [docs/PYPI_PUBLISHING.md](docs/PYPI_PUBLISHING.md)
- **CI/CD Guide**: [docs/CI_CD_SETUP.md](docs/CI_CD_SETUP.md)
- **Helper Script**: `./publish-to-pypi.sh`
- **Workflow File**: `.github/workflows/ci-cd.yml`

---

## 🎬 Quick Start Commands

```bash
# 1. Publish to PyPI (test first, then production)
./publish-to-pypi.sh

# 2. Set up CI/CD
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD pipeline"
git push origin main

# 3. Add PyPI token to GitHub
# Visit: https://github.com/Sabyasachig/ai-cost-observatory/settings/secrets/actions
# Add: PYPI_API_TOKEN

# 4. Watch your first CI run
# Visit: https://github.com/Sabyasachig/ai-cost-observatory/actions

# 5. Create a release (triggers auto-publishing to PyPI)
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0 - Initial PyPI Release"
```

---

**You're ready to make your package professionally available!** 🚀

For detailed step-by-step instructions, see:
- [PyPI Publishing Guide](docs/PYPI_PUBLISHING.md)
- [CI/CD Setup Guide](docs/CI_CD_SETUP.md)
