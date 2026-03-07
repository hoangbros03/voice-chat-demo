#!/bin/bash

# Voice Chat Demo - Docker Quick Start Script
# This script helps you set up and run the Docker containers

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Voice Chat Demo - Docker Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker Compose is installed${NC}"
echo ""

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon is not running. Please start Docker.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker daemon is running${NC}"
echo ""

# Create .env.dev if it doesn't exist
if [ ! -f .env.dev ]; then
    echo -e "${YELLOW}Creating .env.dev from .env.example...${NC}"
    cp .env.example .env.dev
    echo -e "${YELLOW}⚠️  Please edit .env.dev and add your API keys:${NC}"
    echo "   - OPENAI_API__KEY"
    echo "   - SEARCH__API_KEY"
    echo ""
    read -p "Do you want to edit .env.dev now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env.dev
    fi
fi

echo ""
echo -e "${YELLOW}Available commands:${NC}"
echo "  make up         - Start all services in foreground"
echo "  make up-d       - Start all services in background"
echo "  make down       - Stop all services"
echo "  make logs       - View service logs"
echo "  make health     - Check service health"
echo "  make help       - Show all available commands"
echo ""

# Ask if user wants to build and start services
read -p "Do you want to build and start the services now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}Building Docker images...${NC}"
    docker-compose build
    
    echo ""
    echo -e "${BLUE}Starting services...${NC}"
    docker-compose up -d
    
    echo ""
    echo -e "${GREEN}✓ Services are starting${NC}"
    echo ""
    echo -e "${YELLOW}Waiting for services to be ready...${NC}"
    sleep 10
    
    # Check health
    echo ""
    echo -e "${BLUE}Checking service health...${NC}"
    
    echo -n "  FastRTC Core... "
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(still starting)${NC}"
    fi
    
    echo -n "  Vector Search... "
    if curl -sf http://localhost:8002/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}(still starting)${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Services are running at:"
    echo "  • FastRTC Core API: http://localhost:8000/docs"
    echo "  • Vector Search API: http://localhost:8002/docs"
    echo "  • MCP Server: http://localhost:8001"
    echo ""
    echo "View logs with: docker-compose logs -f"
    echo "Stop services with: docker-compose down"
    echo ""
else
    echo ""
    echo -e "${YELLOW}Skipped starting services${NC}"
    echo "To start later, run:"
    echo "  make up-d       (start in background)"
    echo "  make up         (start in foreground)"
    echo ""
fi
