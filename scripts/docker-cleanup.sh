#!/bin/bash
# Script de limpieza Docker para GuaraniAppStore

echo "🧹 Docker Cleanup - GuaraniAppStore"
echo "===================================="
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Este script limpiará:"
echo "  - Contenedores parados"
echo "  - Imágenes no utilizadas"
echo "  - Volúmenes no utilizados (opcional)"
echo "  - Redes no utilizadas"
echo "  - Build cache"
echo ""

read -p "¿Continuar? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelado"
    exit 0
fi

echo ""
echo "1. Parando servicios de GuaraniAppStore..."
docker compose down

echo ""
echo "2. Removiendo contenedores parados..."
docker container prune -f

echo ""
echo "3. Removiendo imágenes no utilizadas..."
docker image prune -a -f

echo ""
echo "4. Removiendo redes no utilizadas..."
docker network prune -f

echo ""
read -p "⚠️  ¿Remover volúmenes NO utilizados? Esto NO afectará volúmenes activos (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker volume prune -f
    echo -e "${GREEN}✓${NC} Volúmenes limpiados"
fi

echo ""
echo "5. Removiendo build cache..."
docker builder prune -f

echo ""
echo "Espacio liberado:"
docker system df

echo ""
echo -e "${GREEN}✓ Limpieza completada${NC}"
echo ""
echo "Para ver espacio usado: docker system df"
