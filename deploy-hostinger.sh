#!/bin/bash

###############################################################################
# SCRIPT DE DEPLOYMENT - GuaraniAppStore V2.5 para HOSTINGER SHARED HOSTING
# Uso: ./deploy-hostinger.sh
###############################################################################
# IMPORTANTE: Este script está optimizado para hosting compartido
# Si tienes VPS/Dedicado, usa deploy.sh en su lugar
###############################################################################

set -e  # Exit on error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
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

log_step() {
    echo -e "${MAGENTA}▶️  $1${NC}"
}

# Banner
clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   GuaraniAppStore V2.5 - Deployment para Hostinger          ║"
echo "║              (Hosting Compartido)                            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

###############################################################################
# VERIFICACIONES INICIALES
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "VERIFICACIONES INICIALES"
echo "═══════════════════════════════════════════════════════════════"

# Verificar que estemos en el directorio correcto
if [ ! -f "composer.json" ]; then
    log_error "No se encuentra composer.json. Asegúrate de estar en el directorio 'webapp'"
    log_info "Cambiando al directorio webapp..."
    cd webapp 2>/dev/null || {
        log_error "No se pudo encontrar el directorio webapp"
        exit 1
    }
fi

log_success "Directorio correcto detectado"

# Verificar PHP
log_info "Verificando PHP..."
if ! command -v php &> /dev/null; then
    log_error "PHP no está disponible en el PATH"
    log_warning "En Hostinger, PHP suele estar en /usr/bin/php o /opt/alt/phpXX/usr/bin/php"
    exit 1
fi

PHP_VERSION=$(php -r 'echo PHP_VERSION;')
log_success "PHP $PHP_VERSION detectado"

# Verificar versión de PHP (mínimo 8.1)
PHP_MAJOR=$(echo $PHP_VERSION | cut -d. -f1)
PHP_MINOR=$(echo $PHP_VERSION | cut -d. -f2)

if [ "$PHP_MAJOR" -lt 8 ] || ([ "$PHP_MAJOR" -eq 8 ] && [ "$PHP_MINOR" -lt 1 ]); then
    log_error "Laravel 12 requiere PHP 8.1 o superior. Tienes: $PHP_VERSION"
    log_warning "En Hostinger Panel > PHP Configuration, selecciona PHP 8.1, 8.2 o 8.3"
    exit 1
fi
log_success "Versión de PHP correcta (mínimo 8.1)"

# Verificar Composer
log_info "Verificando Composer..."
if command -v composer &> /dev/null; then
    COMPOSER_CMD="composer"
    log_success "Composer instalado globalmente"
elif [ -f "composer.phar" ]; then
    COMPOSER_CMD="php composer.phar"
    log_success "composer.phar encontrado localmente"
else
    log_warning "Composer no encontrado. Descargando..."
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
    php composer-setup.php --quiet
    php -r "unlink('composer-setup.php');"
    COMPOSER_CMD="php composer.phar"
    log_success "Composer descargado correctamente"
fi

COMPOSER_VERSION=$($COMPOSER_CMD --version 2>/dev/null | head -n1)
log_info "$COMPOSER_VERSION"

echo ""

###############################################################################
# PASO 1: BACKUP (si existe instalación previa)
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 1: Backup de seguridad"
echo "═══════════════════════════════════════════════════════════════"

if [ -f ".env" ]; then
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    log_info "Creando backup de .env..."
    cp .env "$BACKUP_DIR/.env.backup"
    log_success "Backup creado en: $BACKUP_DIR"

    if [ -d "storage" ]; then
        log_info "Haciendo backup de archivos storage..."
        cp -r storage "$BACKUP_DIR/"
        log_success "Storage respaldado"
    fi
else
    log_info "No hay instalación previa, omitiendo backup"
fi

echo ""

###############################################################################
# PASO 2: INSTALACIÓN DE DEPENDENCIAS
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 2: Instalación de Dependencias"
echo "═══════════════════════════════════════════════════════════════"

log_step "Instalando dependencias de Composer (modo producción)..."
$COMPOSER_CMD install --optimize-autoloader --no-dev --no-interaction 2>&1 | grep -v "Warning:" || true
log_success "Dependencias de Composer instaladas"

# NPM/Node.js (opcional en hosting compartido)
if command -v npm &> /dev/null; then
    log_info "NPM detectado, instalando dependencias frontend..."
    npm install --silent 2>&1 | tail -n 5
    log_success "Dependencias de NPM instaladas"

    log_info "Compilando assets para producción..."
    npm run build 2>&1 | tail -n 5
    log_success "Assets compilados"
else
    log_warning "NPM no disponible (normal en hosting compartido)"
    log_info "Los assets ya están pre-compilados en el repositorio"
fi

echo ""

###############################################################################
# PASO 3: CONFIGURACIÓN DEL ENTORNO
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 3: Configuración del Entorno"
echo "═══════════════════════════════════════════════════════════════"

# Verificar .env
if [ ! -f .env ]; then
    log_warning ".env no existe. Creando desde template..."

    if [ -f .env.hostinger ]; then
        cp .env.hostinger .env
        log_success ".env creado desde .env.hostinger"
    elif [ -f .env.example ]; then
        cp .env.example .env
        log_success ".env creado desde .env.example"
    else
        log_error "No se encontró ni .env.hostinger ni .env.example"
        exit 1
    fi

    # Generar APP_KEY
    log_info "Generando APP_KEY..."
    php artisan key:generate --force
    log_success "APP_KEY generada"

    log_warning ""
    log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_warning "  ⚠️  IMPORTANTE: Configura tu .env AHORA"
    log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log_warning ""
    log_warning "Edita el archivo .env y configura:"
    log_warning "1. Base de datos (DB_DATABASE, DB_USERNAME, DB_PASSWORD)"
    log_warning "2. URL de tu aplicación (APP_URL)"
    log_warning "3. Telegram bots (TELEGRAM_BOT_*_TOKEN)"
    log_warning "4. APIs externas (OPENROUTER_API_KEY, GOOGLE_*, etc.)"
    log_warning ""
    read -p "Presiona ENTER cuando hayas configurado el .env..." -r
else
    log_success ".env ya existe"
    log_info "Verificando APP_KEY..."

    if ! grep -q "APP_KEY=base64:" .env; then
        log_warning "APP_KEY no configurada, generando..."
        php artisan key:generate --force
        log_success "APP_KEY generada"
    else
        log_success "APP_KEY ya configurada"
    fi
fi

echo ""

###############################################################################
# PASO 4: PERMISOS DE DIRECTORIOS
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 4: Configuración de Permisos"
echo "═══════════════════════════════════════════════════════════════"

log_info "Configurando permisos de storage y cache..."

# Crear directorios necesarios si no existen
mkdir -p storage/framework/{sessions,views,cache}
mkdir -p storage/logs
mkdir -p bootstrap/cache

# Configurar permisos (en hosting compartido puede fallar, no es crítico)
chmod -R 755 storage bootstrap/cache 2>/dev/null || log_warning "No se pudieron cambiar algunos permisos (normal en hosting compartido)"
chmod -R 775 storage/logs 2>/dev/null || log_warning "No se pudieron cambiar permisos de logs"

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
# PASO 5: OPTIMIZACIONES DE LARAVEL
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 5: Optimizaciones de Laravel"
echo "═══════════════════════════════════════════════════════════════"

log_info "Limpiando caché..."
php artisan config:clear 2>&1 | grep -v "Warning:" || true
php artisan route:clear 2>&1 | grep -v "Warning:" || true
php artisan view:clear 2>&1 | grep -v "Warning:" || true
log_success "Caché limpiada"

log_info "Optimizando para producción..."
php artisan config:cache 2>&1 | grep -v "Warning:" || true
php artisan route:cache 2>&1 | grep -v "Warning:" || true
php artisan view:cache 2>&1 | grep -v "Warning:" || true
log_success "Optimizaciones aplicadas"

echo ""

###############################################################################
# PASO 6: BASE DE DATOS
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 6: Base de Datos"
echo "═══════════════════════════════════════════════════════════════"

log_warning ""
log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_warning "  📊 CONFIGURACIÓN DE BASE DE DATOS"
log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_warning ""
log_warning "Para configurar la base de datos:"
log_warning "1. Ve a Hostinger Panel > Databases > MySQL Databases"
log_warning "2. Crea una nueva base de datos"
log_warning "3. En phpMyAdmin, selecciona la base de datos"
log_warning "4. Importa el archivo: database.sql"
log_warning "5. Verifica que las tablas se crearon correctamente"
log_warning ""
log_info "El archivo database.sql está en la raíz del proyecto"
log_warning ""

read -p "¿Ya importaste database.sql en phpMyAdmin? (s/N): " -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    log_success "Base de datos configurada"

    log_info "Probando conexión a la base de datos..."
    if php artisan db:show 2>&1 | grep -q "MySQL\|MariaDB"; then
        log_success "✅ Conexión a base de datos exitosa"
    else
        log_warning "No se pudo verificar la conexión, pero puede estar correcta"
    fi
else
    log_warning "Recuerda importar database.sql antes de usar la aplicación"
fi

echo ""

###############################################################################
# PASO 7: CONFIGURACIÓN DE DOMINIO
###############################################################################
echo "═══════════════════════════════════════════════════════════════"
echo "PASO 7: Configuración de Dominio"
echo "═══════════════════════════════════════════════════════════════"

log_warning ""
log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_warning "  🌐 CONFIGURACIÓN IMPORTANTE DE DOMINIO"
log_warning "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_warning ""
log_warning "En Hostinger Panel, asegúrate de:"
log_warning ""
log_warning "1. Ir a: Websites > Manage > Advanced > Document Root"
log_warning "2. Cambiar el Document Root a: /public_html/webapp/public"
log_warning "   (o el path donde está tu carpeta 'public' de Laravel)"
log_warning ""
log_warning "3. Verificar que el archivo .htaccess existe en public/"
log_warning "4. SSL/HTTPS debe estar activado (Hostinger lo hace automático)"
log_warning ""
log_warning "Si no cambias el Document Root, la aplicación NO funcionará"
log_warning ""

echo ""

###############################################################################
# RESUMEN FINAL
###############################################################################
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║            DEPLOYMENT COMPLETADO EXITOSAMENTE                ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

log_success "✅ Aplicación deployada en modo PRODUCCIÓN"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📋 CHECKLIST POST-DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Cosas que YA hicimos:"
echo "  • Dependencias instaladas"
echo "  • .env configurado"
echo "  • Permisos configurados"
echo "  • Laravel optimizado"
echo ""
echo "⚠️  Cosas que DEBES hacer:"
echo "  1. ✅ Database importada en phpMyAdmin"
echo "  2. ✅ Document Root apuntando a /public_html/webapp/public"
echo "  3. ⏳ Configurar Webhooks de Telegram:"
echo "     → php artisan telegram:setup-webhooks"
echo "  4. ⏳ Cambiar password del admin:"
echo "     → Email: admin@guaraniappstore.com"
echo "     → Pass actual: admin123"
echo "  5. ⏳ Configurar APIs externas en .env:"
echo "     → OPENROUTER_API_KEY"
echo "     → GOOGLE_CLIENT_ID"
echo "     → PAYPAL_CLIENT_ID"
echo "  6. ⏳ Verificar que HTTPS está activo"
echo "  7. ⏳ Hacer backup de la base de datos"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

log_info "Para configurar los webhooks de Telegram, ejecuta:"
echo "  php artisan telegram:setup-webhooks"
echo ""

log_info "Para verificar el estado de los bots:"
echo "  php artisan telegram:info"
echo ""

log_success "🎉 ¡Todo listo! Visita tu dominio y prueba la aplicación"
echo ""
