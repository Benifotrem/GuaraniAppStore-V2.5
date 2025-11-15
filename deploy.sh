#!/bin/bash

###############################################################################
# SCRIPT DE DEPLOYMENT - GuaraniAppStore V2.5
# Uso: ./deploy.sh [production|staging|local]
###############################################################################

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logs
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo "╔══════════════════════════════════════════════════════════╗"
echo "║     GuaraniAppStore V2.5 - Script de Deployment         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Verificar entorno
ENVIRONMENT=${1:-production}
log_info "Entorno de deployment: $ENVIRONMENT"
echo ""

# Cambiar al directorio webapp
cd "$(dirname "$0")/webapp" || exit 1

###############################################################################
# PASO 1: VERIFICACIONES PREVIAS
###############################################################################
echo "═══════════════════════════════════════════════════════════"
echo "PASO 1: Verificaciones Previas"
echo "═══════════════════════════════════════════════════════════"

# Verificar PHP
log_info "Verificando PHP..."
if ! command -v php &> /dev/null; then
    log_error "PHP no está instalado"
    exit 1
fi

PHP_VERSION=$(php -r 'echo PHP_VERSION;')
log_success "PHP $PHP_VERSION detectado"

# Verificar Composer
log_info "Verificando Composer..."
if ! command -v composer &> /dev/null; then
    log_error "Composer no está instalado"
    exit 1
fi
log_success "Composer instalado"

echo ""

###############################################################################
# PASO 2: INSTALACIÓN DE DEPENDENCIAS
###############################################################################
echo "═══════════════════════════════════════════════════════════"
echo "PASO 2: Instalación de Dependencias"
echo "═══════════════════════════════════════════════════════════"

log_info "Instalando dependencias de Composer..."
if [ "$ENVIRONMENT" = "production" ]; then
    composer install --optimize-autoloader --no-dev --no-interaction
else
    composer install --optimize-autoloader
fi
log_success "Dependencias de Composer instaladas"

if command -v npm &> /dev/null; then
    log_info "Instalando dependencias de NPM..."
    npm install
    log_success "Dependencias de NPM instaladas"

    log_info "Compilando assets..."
    npm run build
    log_success "Assets compilados"
fi

echo ""

###############################################################################
# PASO 3: CONFIGURACIÓN DEL ENTORNO
###############################################################################
echo "═══════════════════════════════════════════════════════════"
echo "PASO 3: Configuración del Entorno"
echo "═══════════════════════════════════════════════════════════"

# Verificar .env
if [ ! -f .env ]; then
    log_warning ".env no existe. Copiando desde .env.example..."
    cp .env.example .env
    log_success ".env creado"

    # Generar APP_KEY
    log_info "Generando APP_KEY..."
    php artisan key:generate --force
    log_success "APP_KEY generada"
else
    log_success ".env ya existe"
fi

echo ""

###############################################################################
# PASO 4: PERMISOS DE DIRECTORIOS
###############################################################################
echo "═══════════════════════════════════════════════════════════"
echo "PASO 4: Configuración de Permisos"
echo "═══════════════════════════════════════════════════════════"

log_info "Configurando permisos de storage y cache..."
chmod -R 755 storage bootstrap/cache
chmod -R 775 storage/logs

log_success "Permisos configurados"

# Storage link
if [ ! -L public/storage ]; then
    log_info "Creando symlink de storage..."
    php artisan storage:link
    log_success "Symlink creado"
else
    log_success "Symlink de storage ya existe"
fi

echo ""

###############################################################################
# RESUMEN FINAL
###############################################################################
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                  DEPLOYMENT BÁSICO COMPLETADO            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

log_success "Aplicación preparada en modo: $ENVIRONMENT"
echo ""

echo "Próximos pasos:"
echo "1. Configura tu .env con las credenciales de BD"
echo "2. Ejecuta: php artisan migrate --seed"
echo "3. Ejecuta: php artisan telegram:setup-webhooks"
echo ""

log_success "¡Listo para continuar! 🎉"
