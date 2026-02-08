#!/bin/bash

# AI Cost Observatory - Docker Management Script

set -e

COMPOSE_FILE="docker-compose.yml"

echo "🔭 AI Cost Observatory - Docker Manager"
echo "========================================"
echo ""

case "${1:-}" in
    start)
        echo "🚀 Starting services..."
        docker-compose up -d
        echo ""
        echo "✅ Services started!"
        echo ""
        echo "📊 Dashboard: http://localhost:8501"
        echo "🔌 API: http://localhost:8000"
        echo "📖 API Docs: http://localhost:8000/docs"
        echo ""
        echo "View logs: ./docker-manage.sh logs"
        ;;
    
    stop)
        echo "🛑 Stopping services..."
        docker-compose down
        echo "✅ Services stopped!"
        ;;
    
    restart)
        echo "🔄 Restarting services..."
        docker-compose restart
        echo "✅ Services restarted!"
        ;;
    
    logs)
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    
    build)
        echo "🔨 Building images..."
        docker-compose build --no-cache
        echo "✅ Build complete!"
        ;;
    
    rebuild)
        echo "🔨 Rebuilding and restarting..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        echo "✅ Rebuild complete!"
        echo ""
        echo "📊 Dashboard: http://localhost:8501"
        echo "🔌 API: http://localhost:8000"
        ;;
    
    status)
        echo "📊 Service Status:"
        docker-compose ps
        ;;
    
    clean)
        echo "🧹 Cleaning up..."
        docker-compose down -v
        echo "✅ Cleanup complete (volumes removed)!"
        ;;
    
    shell-api)
        echo "🐚 Opening shell in API container..."
        docker-compose exec api /bin/bash
        ;;
    
    shell-db)
        echo "🐚 Opening PostgreSQL shell..."
        docker-compose exec postgres psql -U ai_observatory -d ai_cost_observatory
        ;;
    
    *)
        echo "Usage: $0 {start|stop|restart|logs|build|rebuild|status|clean|shell-api|shell-db}"
        echo ""
        echo "Commands:"
        echo "  start      - Start all services"
        echo "  stop       - Stop all services"
        echo "  restart    - Restart all services"
        echo "  logs       - View logs (follow mode)"
        echo "  build      - Build Docker images"
        echo "  rebuild    - Rebuild and restart"
        echo "  status     - Show service status"
        echo "  clean      - Stop and remove all volumes"
        echo "  shell-api  - Open shell in API container"
        echo "  shell-db   - Open PostgreSQL shell"
        exit 1
        ;;
esac
