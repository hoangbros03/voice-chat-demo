.PHONY: help build up down logs clean test shell env

help:
	@echo "Voice Chat Demo - Docker Commands"
	@echo "=================================="
	@echo ""
	@echo "make env              - Create .env.dev from .env.example"
	@echo "make build            - Build Docker images"
	@echo "make up               - Start all services in foreground"
	@echo "make up-d             - Start all services in background"
	@echo "make down             - Stop all services"
	@echo "make clean            - Remove containers, images, and volumes"
	@echo "make logs             - View logs from all services"
	@echo "make logs-core        - View logs from fastrtc-core service"
	@echo "make logs-mcp         - View logs from mcp-server service"
	@echo "make logs-search      - View logs from vector-search service"
	@echo "make ps               - Show running container status"
	@echo "make shell-core       - Open shell in fastrtc-core container"
	@echo "make shell-mcp        - Open shell in mcp-server container"
	@echo "make shell-search     - Open shell in vector-search container"
	@echo "make test             - Run tests in containers"
	@echo "make health           - Check health of all services"
	@echo "make rebuild          - Rebuild images without cache"
	@echo "make prune            - Remove stopped containers and dangling images"
	@echo ""

env:
	@if [ ! -f .env.dev ]; then \
		cp .env.example .env.dev; \
		echo "Created .env.dev - please update with your credentials"; \
	else \
		echo ".env.dev already exists"; \
	fi

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

up:
	docker-compose up

up-d:
	docker-compose up -d
	@echo "Services started in background. Check status with 'make ps'"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-core:
	docker-compose logs -f fastrtc-core

logs-mcp:
	docker-compose logs -f mcp-server

logs-search:
	docker-compose logs -f vector-search

ps:
	docker-compose ps

shell-core:
	docker-compose exec fastrtc-core /bin/bash

shell-mcp:
	docker-compose exec mcp-server /bin/bash

shell-search:
	docker-compose exec vector-search /bin/bash

health:
	@echo "Checking FastRTC Core..."
	@curl -f http://localhost:8000/health 2>/dev/null && echo "✓ FastRTC Core is healthy" || echo "✗ FastRTC Core is down"
	@echo ""
	@echo "Checking Vector Search..."
	@curl -f http://localhost:8002/health 2>/dev/null && echo "✓ Vector Search is healthy" || echo "✗ Vector Search is down"
	@echo ""
	@echo "Checking MCP Server..."
	@curl -f http://localhost:8001/health 2>/dev/null && echo "✓ MCP Server is healthy" || echo "✗ MCP Server is down (may not have health endpoint)"

test:
	docker-compose exec fastrtc-core python -m pytest services/fastrtc_core/test/ -v
	docker-compose exec mcp-server python -m pytest services/mcp_server/test/ -v

clean: down
	docker-compose rm -f
	docker rmi $$(docker images -f "reference=*voice*" -q) 2>/dev/null || true
	@echo "Cleaned up Docker resources"

prune:
	docker system prune -f
	@echo "Docker system pruned"

restart:
	make down
	make up-d
	@echo "Services restarted"

restart-core:
	docker-compose restart fastrtc-core

restart-mcp:
	docker-compose restart mcp-server

restart-search:
	docker-compose restart vector-search
