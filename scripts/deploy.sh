#!/bin/bash
# Deploy script for GuaraniAppStore V2.5 Pro

set -e

echo "🚀 GuaraniAppStore V2.5 Pro - Deploy Script"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please copy .env.docker to .env and configure it"
    exit 1
fi

# Check if backend/.env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}Error: backend/.env file not found${NC}"
    echo "Please copy backend/.env.example to backend/.env and configure it"
    exit 1
fi

# Check if frontend/.env exists
if [ ! -f "frontend/.env" ]; then
    echo -e "${RED}Error: frontend/.env file not found${NC}"
    echo "Please copy frontend/.env.example to frontend/.env and configure it"
    exit 1
fi

echo -e "${GREEN}✓ Environment files found${NC}"
echo ""

# Pull latest changes (optional)
read -p "Pull latest changes from Git? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pulling latest changes..."
    git pull
    echo -e "${GREEN}✓ Updated from Git${NC}"
fi

# Build and start containers
echo ""
echo "Building Docker containers..."
docker-compose build --no-cache

echo ""
echo "Starting services..."
docker-compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check service status
echo ""
echo "Service Status:"
docker-compose ps

echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo ""
echo "Services:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8001"
echo "  - Nginx Proxy: http://localhost:80"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
echo "  - View backend logs: docker-compose logs -f backend"
echo "  - View frontend logs: docker-compose logs -f frontend"
echo ""