# 🔄 Setting Up CI/CD with GitHub Actions

This guide explains how to set up Continuous Integration and Continuous Deployment for AI Cost Observatory.

## What Our CI/CD Pipeline Does

Our GitHub Actions workflow automatically:

1. **Tests** - Runs tests on Python 3.8-3.12
2. **Lints** - Checks code quality (Black, flake8, isort)
3. **Docker** - Builds and tests Docker containers
4. **Builds** - Creates Python package
5. **Publishes** - Deploys to PyPI on release (optional)

## Setup Instructions

### Step 1: Enable GitHub Actions

1. Go to your repository: https://github.com/Sabyasachig/ai-cost-observatory
2. Click **Settings** → **Actions** → **General**
3. Under "Actions permissions", select **"Allow all actions and reusable workflows"**
4. Click **Save**

### Step 2: Add PyPI API Token (For Auto-Publishing)

**Only needed if you want automatic PyPI publishing on releases.**

1. Get your PyPI API token from: https://pypi.org/manage/account/token/
2. In your GitHub repo, go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token (starts with `pypi-`)
6. Click **Add secret**

### Step 3: Push the Workflow File

The workflow file is already created at `.github/workflows/ci-cd.yml`. Just commit and push:

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD pipeline with GitHub Actions"
git push origin main
```

### Step 4: Verify Workflow Runs

1. Go to your repository on GitHub
2. Click **Actions** tab
3. You should see a workflow run triggered by your push
4. Click on the run to see details
5. Wait for all jobs to complete (green checkmarks)

## Workflow Triggers

The CI/CD pipeline runs on:

- **Push to main/develop** - Runs tests, linting, and Docker builds
- **Pull Requests to main** - Validates changes before merging
- **New Releases** - Runs full pipeline + publishes to PyPI

## Understanding the Jobs

### Job 1: Test (Matrix Build)

```yaml
test:
  strategy:
    matrix:
      python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
```

- Runs tests on 5 Python versions
- Generates code coverage reports
- Uploads coverage to Codecov (if configured)

**Status**: ✅ Required to pass

### Job 2: Lint (Code Quality)

```yaml
lint:
  - Black (code formatting)
  - flake8 (style guide enforcement)
  - isort (import sorting)
```

- Ensures code follows Python best practices
- Catches common errors
- Maintains consistent style

**Status**: ✅ Required to pass

### Job 3: Docker (Container Build)

```yaml
docker:
  - Builds API container
  - Builds Dashboard container
  - Starts services with docker-compose
  - Tests health endpoints
```

- Validates Docker deployment works
- Catches container configuration issues
- Tests service communication

**Status**: ✅ Required to pass

### Job 4: Build (Package Creation)

```yaml
build:
  - Builds Python package (wheel + sdist)
  - Validates with twine check
  - Uploads artifacts
```

- Creates distributable package
- Validates package structure
- Stores artifacts for download

**Status**: ✅ Required to pass

### Job 5: Publish (PyPI Deployment)

```yaml
publish:
  if: github.event_name == 'release'
  - Builds package
  - Publishes to PyPI
```

- Only runs on GitHub releases
- Requires `PYPI_API_TOKEN` secret
- Automatically publishes to PyPI

**Status**: 🔄 Optional (only on releases)

## Adding Status Badges to README

After your first successful workflow run, add these badges to your README.md:

```markdown
[![CI/CD Pipeline](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/Sabyasachig/ai-cost-observatory/ci-cd.yml?label=tests)](https://github.com/Sabyasachig/ai-cost-observatory/actions)
[![Python Versions](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://github.com/Sabyasachig/ai-cost-observatory)
```

Add near the top of your README, after the title:

```markdown
# 🔭 AI Cost Observatory

[![CI/CD Pipeline](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Sabyasachig/ai-cost-observatory/actions/workflows/ci-cd.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
```

## Optional Enhancements

### Add Codecov Integration

1. Sign up at: https://codecov.io/
2. Connect your GitHub repository
3. Add `CODECOV_TOKEN` to GitHub secrets
4. Badge will automatically appear in PR comments

### Add Dependabot

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/sdk"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "pip"
    directory: "/server"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "pip"
    directory: "/ui"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "docker"
    directory: "/server"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "docker"
    directory: "/ui"
    schedule:
      interval: "weekly"
  
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

This automatically creates PRs to update dependencies.

### Add Release Drafter

Automatically generate release notes from PRs.

Create `.github/release-drafter.yml`:

```yaml
name-template: 'v$RESOLVED_VERSION'
tag-template: 'v$RESOLVED_VERSION'
categories:
  - title: '🚀 Features'
    labels:
      - 'feature'
      - 'enhancement'
  - title: '🐛 Bug Fixes'
    labels:
      - 'fix'
      - 'bugfix'
      - 'bug'
  - title: '📚 Documentation'
    labels:
      - 'documentation'
  - title: '🔧 Maintenance'
    labels:
      - 'chore'
      - 'maintenance'
version-resolver:
  major:
    labels:
      - 'breaking'
  minor:
    labels:
      - 'feature'
  patch:
    labels:
      - 'fix'
      - 'bugfix'
  default: patch
template: |
  ## What's Changed
  
  $CHANGES
  
  ## Contributors
  
  $CONTRIBUTORS
```

And `.github/workflows/release-drafter.yml`:

```yaml
name: Release Drafter

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, reopened, synchronize]

permissions:
  contents: read

jobs:
  update_release_draft:
    permissions:
      contents: write
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - uses: release-drafter/release-drafter@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

### Workflow Not Running

**Check**:
1. GitHub Actions enabled in Settings
2. Workflow file in `.github/workflows/` directory
3. Valid YAML syntax (use online validator)

### Tests Failing

**Check**:
1. Tests pass locally: `cd tests && pytest -v`
2. All dependencies listed in `requirements.txt`
3. Python version compatibility

### Docker Build Failing

**Check**:
1. Dockerfiles are valid
2. `docker-compose.yml` is valid
3. Local build works: `docker-compose up`

### Publish Job Not Running

**Check**:
1. `PYPI_API_TOKEN` secret is set
2. Triggered by a release (not just a tag)
3. Previous jobs passed

### PyPI Upload Fails

**Error**: "403 Forbidden"
- Invalid or expired token
- Token doesn't have permission for package

**Error**: "File already exists"
- Version number already published
- Increment version in `setup.py` and `pyproject.toml`

## Manual Publishing (Without CI/CD)

If you prefer manual publishing:

1. Remove or comment out the `publish` job in `.github/workflows/ci-cd.yml`
2. Follow the [PyPI Publishing Guide](PYPI_PUBLISHING.md) for manual steps
3. CI will still run tests and builds, just not auto-publish

## Workflow Commands

### View Workflow Runs

```bash
# Using GitHub CLI
gh run list

# View specific run
gh run view RUN_ID

# Watch live run
gh run watch
```

### Manually Trigger Workflow

```bash
# Trigger via GitHub CLI
gh workflow run ci-cd.yml

# Or via GitHub UI
# Actions tab → Select workflow → Run workflow button
```

### Cancel Running Workflow

```bash
# Cancel via GitHub CLI
gh run cancel RUN_ID

# Or via GitHub UI
# Actions tab → Click on run → Cancel workflow
```

## Best Practices

1. **Always run tests locally first**
   ```bash
   cd tests && pytest -v
   ```

2. **Use branches for features**
   ```bash
   git checkout -b feature/new-feature
   git push -u origin feature/new-feature
   # Create PR when ready
   ```

3. **Review CI failures immediately**
   - Don't merge if CI fails
   - Fix issues in the same PR

4. **Keep workflows fast**
   - Use caching for dependencies
   - Run expensive tests only on main branch

5. **Secure secrets properly**
   - Never commit tokens/passwords
   - Use GitHub secrets for sensitive data
   - Rotate tokens regularly

## Next Steps

After setting up CI/CD:

1. ✅ Commit and push the workflow file
2. ✅ Verify workflow runs successfully
3. ✅ Add status badges to README
4. ✅ Configure PyPI token for auto-publishing
5. ✅ Create your first release to test publishing

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Publishing to PyPI](https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)

---

**Your CI/CD pipeline is ready to go!** 🚀
