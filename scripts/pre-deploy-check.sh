#!/bin/bash
# Pre-deployment verification script

echo "🔍 Pre-Deployment Checklist"
echo "============================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✓${NC} Docker installed: $DOCKER_VERSION"
else
    echo -e "${RED}✗${NC} Docker not found. Install from: https://get.docker.com"
    ERRORS=$((ERRORS + 1))
fi

# Check Docker Compose
echo ""
echo "2. Checking Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version)
    echo -e "${GREEN}✓${NC} Docker Compose installed: $COMPOSE_VERSION"
else
    echo -e "${RED}✗${NC} Docker Compose not found"
    ERRORS=$((ERRORS + 1))
fi

# Check .env files
echo ""
echo "3. Checking environment files..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env exists"
else
    echo -e "${YELLOW}⚠${NC} .env not found. Copy from .env.docker"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} backend/.env exists"
else
    echo -e "${YELLOW}⚠${NC} backend/.env not found. Copy from backend/.env.example"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "frontend/.env" ]; then
    echo -e "${GREEN}✓${NC} frontend/.env exists"
else
    echo -e "${YELLOW}⚠${NC} frontend/.env not found. Copy from frontend/.env.example"
    ERRORS=$((ERRORS + 1))
fi

# Check critical variables in backend/.env
echo ""
echo "4. Checking critical environment variables..."
if [ -f "backend/.env" ]; then
    REQUIRED_VARS=("POSTGRES_URL" "JWT_SECRET" "SECRET_KEY")
    for VAR in "${REQUIRED_VARS[@]}"; do
        if grep -q "^${VAR}=" backend/.env && ! grep -q "^${VAR}=your" backend/.env; then
            echo -e "${GREEN}✓${NC} $VAR is set"
        else
            echo -e "${YELLOW}⚠${NC} $VAR not configured in backend/.env"
        fi
    done
fi

# Check if ports are available
echo ""
echo "5. Checking ports..."
PORTS=(80 443 3000 8001 5432)
for PORT in "${PORTS[@]}"; do
    if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Port $PORT is available"
    else
        echo -e "${YELLOW}⚠${NC} Port $PORT is already in use"
    fi
done

# Summary
echo ""
echo "============================"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Ready to deploy!${NC}"
    echo ""
    echo "Run: ./scripts/deploy.sh"
    exit 0
else
    echo -e "${YELLOW}⚠ Found $ERRORS issues. Please fix them before deploying.${NC}"
    echo ""
    echo "Quick fixes:"
    echo "  cp .env.docker .env"
    echo "  cp backend/.env.example backend/.env"
    echo "  cp frontend/.env.example frontend/.env"
    echo "  nano .env  # Configure your values"
    exit 1
fi
