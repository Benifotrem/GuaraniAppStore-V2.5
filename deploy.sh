#!/bin/bash

# ============================================
# GuaraniAppStore - Deployment Script
# ============================================

set -e

echo "🚀 Iniciando deployment de GuaraniAppStore..."

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}❌ No ejecutar como root. Usa un usuario con sudo.${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Archivo .env no encontrado en la raíz del proyecto${NC}"
    echo "Copia .env.example a .env y configura las variables"
    exit 1
fi

if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Archivo backend/.env no encontrado${NC}"
    echo "Copia .env.example a backend/.env y configura las variables"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Verificaciones iniciales completadas${NC}"

# Stop existing containers
echo -e "${YELLOW}🛑 Deteniendo contenedores existentes...${NC}"
docker-compose down || true

# Pull latest images (if using pre-built images)
# docker-compose pull

# Build images
echo -e "${YELLOW}🏗️  Construyendo imágenes Docker...${NC}"
docker-compose build --no-cache

# Start services
echo -e "${YELLOW}▶️  Iniciando servicios...${NC}"
docker-compose up -d

# Wait for services to be healthy
echo -e "${YELLOW}⏳ Esperando que los servicios estén listos...${NC}"
sleep 10

# Check services status
echo -e "${YELLOW}🔍 Verificando estado de servicios...${NC}"
docker-compose ps

# Check MongoDB
echo -e "${YELLOW}🔍 Verificando MongoDB...${NC}"
if docker exec guarani_mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MongoDB está funcionando${NC}"
else
    echo -e "${RED}❌ MongoDB no responde${NC}"
    exit 1
fi

# Check Backend
echo -e "${YELLOW}🔍 Verificando Backend...${NC}"
sleep 5
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend está funcionando${NC}"
else
    echo -e "${RED}❌ Backend no responde${NC}"
    echo "Logs del backend:"
    docker-compose logs --tail=50 backend
    exit 1
fi

# Check Frontend
echo -e "${YELLOW}🔍 Verificando Frontend...${NC}"
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend está funcionando${NC}"
else
    echo -e "${RED}❌ Frontend no responde${NC}"
    docker-compose logs --tail=50 frontend
    exit 1
fi

# Initialize database (optional - uncomment if needed)
# echo -e "${YELLOW}🗄️  Inicializando base de datos...${NC}"
# docker exec -it guarani_backend python init_services_mongo_v2.py

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Deployment completado exitosamente!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📊 URLs de acceso:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8001"
echo "  - Health Check: http://localhost:8001/health"
echo ""
echo "📝 Ver logs:"
echo "  docker-compose logs -f"
echo ""
echo "🔄 Reiniciar servicios:"
echo "  docker-compose restart"
echo ""
echo "🛑 Detener servicios:"
echo "  docker-compose down"
echo ""
