# 🐛 Docker Troubleshooting & Fix Guide

## Issue: "Failed to resolve 'api'" Error

**Error Message:**
```
Error fetching data: HTTPConnectionPool(host='api', port=8000): 
Max retries exceeded with url: /dashboard/overview 
(Caused by NameResolutionError("Failed to resolve 'api'"))
```

### ✅ **FIXED!**

This has been resolved by:
1. Adding proper Docker network configuration
2. Making API URL configurable via environment variable
3. Adding health checks to ensure services start in correct order

## How to Apply the Fix

### Option 1: Restart with New Configuration

```bash
# Stop existing containers
docker-compose down

# Rebuild with new configuration
docker-compose build --no-cache

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 2: Use Management Script

```bash
# Rebuild everything
./docker-manage.sh rebuild

# Check status
./docker-manage.sh status

# View logs
./docker-manage.sh logs
```

## Verify the Fix

1. **Check all services are running:**
   ```bash
   docker-compose ps
   ```
   
   You should see:
   - `ai_cost_observatory_db` (healthy)
   - `ai_cost_observatory_api` (healthy)
   - `ai_cost_observatory_ui` (running)

2. **Test API directly:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   Expected response: `{"status":"healthy"}`

3. **Open Dashboard:**
   ```bash
   open http://localhost:8501
   ```
   
   The dashboard should load without errors.

## What Changed

### 1. Docker Compose (`docker-compose.yml`)
- ✅ Added explicit Docker network (`ai_cost_network`)
- ✅ Added container names for easier management
- ✅ Added API healthcheck
- ✅ Made dashboard wait for API to be healthy
- ✅ Changed CORS to allow all origins in Docker

### 2. Dashboard (`ui/dashboard.py`)
- ✅ Added API connection info display
- ✅ Better error handling for API calls
- ✅ Shows which API endpoint it's connecting to

### 3. Docker Images
- ✅ Added curl to API image for healthcheck
- ✅ Added `.dockerignore` files to reduce image size

### 4. Management Script
- ✅ Created `docker-manage.sh` for easy Docker operations

## Common Issues & Solutions

### Issue: Port 8000 already in use
```bash
# Check what's using port 8000
lsof -i :8000

# Stop the process or change port in docker-compose.yml
```

### Issue: Port 8501 already in use
```bash
# Check what's using port 8501
lsof -i :8501

# Stop the process or change port in docker-compose.yml
```

### Issue: Database connection errors
```bash
# Check if PostgreSQL is healthy
docker-compose ps

# View database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Issue: API not responding
```bash
# Check API logs
docker-compose logs api

# Check if API is healthy
docker-compose exec api curl http://localhost:8000/health

# Restart API
docker-compose restart api
```

### Issue: Dashboard shows "No data available"
```bash
# Generate sample data
# First, install SDK locally
cd sdk && pip install -e . && cd ..

# Then generate data
python examples/generate_sample_data.py

# Or use Docker
docker-compose exec api python -c "
import requests
for i in range(10):
    requests.post('http://localhost:8000/events', json={
        'model': 'gpt-4o-mini',
        'prompt_tokens': 100,
        'completion_tokens': 50,
        'total_cost': 0.00001
    })
"
```

## Docker Commands Reference

### Basic Operations
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f api
docker-compose logs -f dashboard

# Restart a service
docker-compose restart api

# Check status
docker-compose ps
```

### Debugging
```bash
# Execute command in container
docker-compose exec api ls -la

# Open shell in API container
docker-compose exec api /bin/bash

# Open PostgreSQL shell
docker-compose exec postgres psql -U ai_observatory -d ai_cost_observatory

# Check container resource usage
docker stats
```

### Clean Up
```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (deletes database!)
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Complete cleanup
docker-compose down -v --rmi all
docker system prune -a
```

## Network Architecture

```
Host Machine (localhost)
│
├─ Port 8000 → API Container (api:8000)
│              │
│              └─ Connects to → PostgreSQL Container (postgres:5432)
│
└─ Port 8501 → Dashboard Container (dashboard:8501)
               │
               └─ Connects to → API Container (api:8000)
```

**Key Points:**
- From your browser: Use `http://localhost:8501` (Dashboard) and `http://localhost:8000` (API)
- Inside Docker network: Services use service names (`api`, `postgres`)
- Dashboard container connects to `http://api:8000` (internal network)

## Testing the Setup

### 1. Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### 2. Create Test Event
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_cost": 0.00001,
    "project": "test"
  }'
# Expected: {"status":"success","event_id":"..."}
```

### 3. Check Dashboard
```bash
open http://localhost:8501
# Should show the event you just created
```

## Performance Tips

1. **Use PostgreSQL volumes:** Data persists between restarts
2. **Build once:** Use `docker-compose build` then `docker-compose up -d`
3. **Monitor resources:** Use `docker stats` to check CPU/memory
4. **Clean old images:** Run `docker system prune` periodically

## Getting Help

If issues persist:

1. Check logs: `docker-compose logs -f`
2. Verify network: `docker network inspect ai_cost_observatory_ai_cost_network`
3. Check services: `docker-compose ps`
4. Review this guide
5. Open an issue on GitHub with logs

## Success Checklist

- ✅ All 3 containers running (db, api, dashboard)
- ✅ API health check returns `{"status":"healthy"}`
- ✅ Dashboard loads at http://localhost:8501
- ✅ No connection errors in dashboard
- ✅ Can create events via API
- ✅ Dashboard shows data

---

**Last Updated:** February 9, 2026  
**Status:** ✅ Fixed and Tested
