# 🚀 Quick Start Commands

## Apply the Docker Fix

```bash
cd /Users/sabyasachighosh/Projects/ai_cost_observatory

# Stop existing containers
docker-compose down

# Rebuild images with new configuration
docker-compose build --no-cache

# Start all services
docker-compose up -d

# Check status (wait for all to be healthy)
docker-compose ps

# Follow logs
docker-compose logs -f
```

## Or Use the Management Script

```bash
# One command to rebuild everything
./docker-manage.sh rebuild

# Check status
./docker-manage.sh status

# View logs
./docker-manage.sh logs
```

## Verify Everything Works

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. Check API docs
open http://localhost:8000/docs

# 3. Open dashboard
open http://localhost:8501

# 4. Create a test event
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "latency_ms": 500,
    "input_cost": 0.000015,
    "output_cost": 0.000030,
    "total_cost": 0.000045,
    "project": "test-project",
    "agent": "test-agent"
  }'
```

## Generate Sample Data

```bash
# Option 1: Install SDK and run script
cd sdk && pip install -e . && cd ..
python examples/generate_sample_data.py

# Option 2: Use Python directly (if SDK installed)
python3 -c "
import requests
import random

for i in range(20):
    response = requests.post('http://localhost:8000/events', json={
        'model': random.choice(['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']),
        'prompt_tokens': random.randint(50, 500),
        'completion_tokens': random.randint(20, 200),
        'total_cost': random.uniform(0.0001, 0.01),
        'project': random.choice(['chatbot', 'rag-system', 'research']),
        'agent': random.choice(['planner', 'executor', 'retriever'])
    })
    print(f'Event {i+1}: {response.status_code}')
"
```

## Useful Docker Commands

```bash
# View all container logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f dashboard
docker-compose logs -f postgres

# Check container status
docker-compose ps

# Restart a service
docker-compose restart api
docker-compose restart dashboard

# Stop all services
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v

# Shell into API container
docker-compose exec api /bin/bash

# Shell into database
docker-compose exec postgres psql -U ai_observatory -d ai_cost_observatory
```

## URLs

- 📊 **Dashboard**: http://localhost:8501
- 🔌 **API**: http://localhost:8000
- 📖 **API Docs**: http://localhost:8000/docs
- 🗄️ **Database**: localhost:5432 (user: ai_observatory, db: ai_cost_observatory)

## If Something Goes Wrong

```bash
# Complete reset
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Or use the script
./docker-manage.sh clean
./docker-manage.sh rebuild
```

## Expected Output

When everything is working:

```bash
$ docker-compose ps
NAME                        STATUS                   PORTS
ai_cost_observatory_db      Up (healthy)            0.0.0.0:5432->5432/tcp
ai_cost_observatory_api     Up (healthy)            0.0.0.0:8000->8000/tcp
ai_cost_observatory_ui      Up                      0.0.0.0:8501->8501/tcp
```

## Next Steps

1. ✅ Start services
2. ✅ Verify health checks
3. ✅ Generate sample data
4. ✅ Open dashboard at http://localhost:8501
5. ✅ Explore the features!

---

For detailed troubleshooting, see: `docs/DOCKER_TROUBLESHOOTING.md`
