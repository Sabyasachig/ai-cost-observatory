# 📜 Scripts Reference

This repository includes several helper scripts to make your life easier.

## 🚀 Repository Management

### `enhance-github-repo.sh`
**Purpose**: Enhance your GitHub repository with topics, releases, and more

**What it does**:
- ✅ Adds repository topics (ai, llm, observability, etc.)
- ✅ Creates v1.0.0 release with release notes
- ✅ Creates git tag
- ✅ Opens repository in browser

**Usage**:
```bash
./enhance-github-repo.sh
```

**When to use**: After forking or cloning to set up your own repository

---

### `create-github-repo.sh`
**Purpose**: Create a new GitHub repository and push code

**What it does**:
- ✅ Checks if GitHub CLI is installed
- ✅ Authenticates with GitHub
- ✅ Creates public repository
- ✅ Pushes code to GitHub

**Usage**:
```bash
./create-github-repo.sh
```

**When to use**: First time setting up the repository (already done for this project)

---

## 🐳 Docker Management

### `docker-manage.sh`
**Purpose**: Manage Docker containers with easy commands

**Available commands**:

```bash
./docker-manage.sh start     # Start all services
./docker-manage.sh stop      # Stop all services
./docker-manage.sh restart   # Restart all services
./docker-manage.sh status    # Check container status
./docker-manage.sh logs      # View all logs
./docker-manage.sh build     # Build containers
./docker-manage.sh rebuild   # Rebuild from scratch
./docker-manage.sh clean     # Stop and remove everything
./docker-manage.sh shell-api # Open shell in API container
./docker-manage.sh shell-db  # Open shell in database container
```

**Examples**:
```bash
# Check if everything is running
./docker-manage.sh status

# View real-time logs
./docker-manage.sh logs

# Restart after code changes
./docker-manage.sh restart

# Complete cleanup and fresh start
./docker-manage.sh clean
./docker-manage.sh start
```

---

## ⚡ Quick Start

### `quickstart.sh`
**Purpose**: One-command setup and start

**What it does**:
- ✅ Checks prerequisites (Docker, Python)
- ✅ Creates environment file from template
- ✅ Starts all Docker containers
- ✅ Waits for services to be healthy
- ✅ Opens dashboard in browser

**Usage**:
```bash
./quickstart.sh
```

**When to use**: First time setup or when introducing someone to the project

---

## 📊 Making Scripts Executable

If you get "permission denied" errors, make scripts executable:

```bash
chmod +x docker-manage.sh
chmod +x quickstart.sh
chmod +x enhance-github-repo.sh
chmod +x create-github-repo.sh
```

Or make all scripts executable at once:

```bash
chmod +x *.sh
```

---

## 🔧 Script Locations

```
ai_cost_observatory/
├── docker-manage.sh          # Docker operations
├── quickstart.sh             # Quick setup
├── enhance-github-repo.sh    # Repository enhancement
└── create-github-repo.sh     # Repository creation
```

---

## 💡 Pro Tips

### Chain Commands
```bash
# Rebuild and check logs
./docker-manage.sh rebuild && ./docker-manage.sh logs

# Stop, clean, and restart fresh
./docker-manage.sh stop && ./docker-manage.sh clean && ./docker-manage.sh start
```

### Debug Issues
```bash
# Check container status
./docker-manage.sh status

# View logs for specific service
docker-compose logs -f api
docker-compose logs -f dashboard

# Open shell to debug
./docker-manage.sh shell-api
```

### Development Workflow
```bash
# 1. Make code changes
vim server/api/main.py

# 2. Rebuild affected service
docker-compose up -d --build api

# 3. Check logs
./docker-manage.sh logs

# 4. Test
curl http://localhost:8000/health
```

---

## 📝 Adding Your Own Scripts

Want to add custom scripts? Follow this pattern:

```bash
#!/bin/bash
# Your script description

set -e  # Exit on error

echo "🚀 Your Script Name"
echo "==================="
echo ""

# Your commands here

echo "✅ Done!"
```

Make it executable:
```bash
chmod +x your-script.sh
```

Add to this documentation!

---

## 🆘 Getting Help

If a script isn't working:

1. **Check Prerequisites**
   ```bash
   which docker
   which docker-compose
   which python3
   ```

2. **View Script Contents**
   ```bash
   cat docker-manage.sh
   ```

3. **Run with Debug Mode**
   ```bash
   bash -x ./docker-manage.sh status
   ```

4. **Check Logs**
   ```bash
   ./docker-manage.sh logs
   ```

---

## 📚 Related Documentation

- `QUICK_COMMANDS.md` - Quick command reference
- `DOCKER_TROUBLESHOOTING.md` - Docker help
- `GETTING_STARTED.md` - Setup guide
- `README.md` - Main documentation

---

**Last Updated**: February 9, 2026  
**Status**: ✅ All scripts tested and working
