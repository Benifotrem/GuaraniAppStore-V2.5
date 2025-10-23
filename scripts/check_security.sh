#!/bin/bash
# Script de verificación de seguridad para GuaraniAppStore

echo "🔍 Verificación de Seguridad - GuaraniAppStore V2.5 Pro"
echo "========================================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de issues
ISSUES=0

# 1. Verificar que .env está en .gitignore
echo "1. Verificando .gitignore..."
if grep -q "*.env" .gitignore && grep -q "*.env.*" .gitignore; then
    echo -e "${GREEN}✓${NC} Archivos .env están en .gitignore"
else
    echo -e "${RED}✗${NC} ALERTA: Archivos .env NO están en .gitignore"
    ISSUES=$((ISSUES + 1))
fi

# 2. Verificar que existen los archivos .env.example
echo ""
echo "2. Verificando archivos .env.example..."
if [ -f "backend/.env.example" ]; then
    echo -e "${GREEN}✓${NC} backend/.env.example existe"
else
    echo -e "${RED}✗${NC} FALTA: backend/.env.example"
    ISSUES=$((ISSUES + 1))
fi

if [ -f "frontend/.env.example" ]; then
    echo -e "${GREEN}✓${NC} frontend/.env.example existe"
else
    echo -e "${RED}✗${NC} FALTA: frontend/.env.example"
    ISSUES=$((ISSUES + 1))
fi

# 3. Buscar claves potencialmente hardcodeadas
echo ""
echo "3. Buscando claves hardcodeadas en el código..."
PATTERNS=(
    "sk-[a-zA-Z0-9]{20,}"
    "api_key.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
    "secret.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
)

FOUND=0
for pattern in "${PATTERNS[@]}"; do
    if grep -rE "$pattern" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" backend/ frontend/ 2>/dev/null | grep -v ".env" | grep -v "node_modules" | grep -v "# " > /dev/null; then
        echo -e "${YELLOW}⚠${NC} Posible clave hardcodeada encontrada (patrón: $pattern)"
        FOUND=1
    fi
done

if [ $FOUND -eq 0 ]; then
    echo -e "${GREEN}✓${NC} No se encontraron claves hardcodeadas obvias"
else
    echo -e "${YELLOW}⚠${NC} Revisa manualmente las coincidencias encontradas"
fi

# 4. Verificar que archivos .env no están trackeados
echo ""
echo "4. Verificando que .env no está en Git..."
if git ls-files | grep -q ".env$"; then
    echo -e "${RED}✗${NC} PELIGRO: Archivo .env está siendo trackeado por Git"
    echo "   Ejecuta: git rm --cached backend/.env frontend/.env"
    ISSUES=$((ISSUES + 1))
else
    echo -e "${GREEN}✓${NC} Archivos .env no están en Git"
fi

# 5. Verificar que las variables de entorno están siendo usadas
echo ""
echo "5. Verificando uso de variables de entorno..."
if grep -r "process.env" frontend/src/ > /dev/null; then
    echo -e "${GREEN}✓${NC} Frontend usa process.env correctamente"
else
    echo -e "${YELLOW}⚠${NC} Frontend no parece usar variables de entorno"
fi

if grep -r "os.environ" backend/*.py > /dev/null; then
    echo -e "${GREEN}✓${NC} Backend usa os.environ correctamente"
else
    echo -e "${YELLOW}⚠${NC} Backend no parece usar variables de entorno"
fi

# Resumen
echo ""
echo "========================================================"
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ Verificación completada: No se encontraron problemas críticos${NC}"
else
    echo -e "${RED}✗ Se encontraron $ISSUES problemas críticos de seguridad${NC}"
    echo "Por favor, revisa y corrige los issues antes de hacer deploy."
    exit 1
fi

echo ""
echo "📚 Para más información, consulta: SECURITY.md"
