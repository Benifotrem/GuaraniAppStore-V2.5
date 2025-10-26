#!/bin/bash

# ============================================
# Generador de .env con Claves Reales
# ============================================
# Este script te ayuda a crear un .env con tus claves reales
# NUNCA subas este archivo a Git - solo úsalo localmente

echo "🔐 Generador de .env con Claves Reales"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANTE: Este archivo NUNCA se sube a Git"
echo "    Solo se usa localmente y se transfiere al VPS por SCP"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Archivo de salida
OUTPUT_FILE=".env"
OUTPUT_BACKEND=".env.backend"

# Verificar si ya existe
if [ -f "$OUTPUT_FILE" ]; then
    echo -e "${YELLOW}⚠️  El archivo .env ya existe.${NC}"
    read -p "¿Deseas sobrescribirlo? (s/n): " overwrite
    if [ "$overwrite" != "s" ]; then
        echo "Operación cancelada."
        exit 0
    fi
fi

echo ""
echo "Empezaremos a solicitar tus claves..."
echo ""

# ============================================
# DOMINIO
# ============================================
echo -e "${GREEN}[1/10] Configuración de Dominio${NC}"
read -p "Tu dominio (ej: guaraniappstore.com): " DOMAIN
REACT_APP_BACKEND_URL="https://${DOMAIN}"

# ============================================
# OPENROUTER
# ============================================
echo ""
echo -e "${GREEN}[2/10] OpenRouter API${NC}"
echo "Obtén tu clave en: https://openrouter.ai/keys"
read -p "OpenRouter API Key: " OPENROUTER_API_KEY

# ============================================
# ANTHROPIC (OPCIONAL)
# ============================================
echo ""
echo -e "${GREEN}[3/10] Anthropic API (Opcional - Fallback)${NC}"
echo "Si no tienes, presiona Enter para omitir"
read -p "Anthropic API Key (opcional): " ANTHROPIC_API_KEY_FALLBACK

# ============================================
# POSTGRESQL
# ============================================
echo ""
echo -e "${GREEN}[4/10] PostgreSQL (Base de datos RAG)${NC}"
read -p "PostgreSQL User [soporte_user_seguro]: " POSTGRES_USER
POSTGRES_USER=${POSTGRES_USER:-soporte_user_seguro}

echo "Generando contraseña segura..."
POSTGRES_PASSWORD=$(openssl rand -base64 24 | tr -d "=+/" | cut -c1-20)
echo -e "Contraseña generada: ${YELLOW}${POSTGRES_PASSWORD}${NC}"

read -p "PostgreSQL Database [soporte_db_rag]: " POSTGRES_DB
POSTGRES_DB=${POSTGRES_DB:-soporte_db_rag}

# ============================================
# JWT SECRETS
# ============================================
echo ""
echo -e "${GREEN}[5/10] JWT y Secret Keys${NC}"
echo "Generando secrets seguros..."

JWT_SECRET=$(openssl rand -hex 32)
echo -e "JWT_SECRET: ${YELLOW}${JWT_SECRET:0:20}...${NC}"

SECRET_KEY=$(openssl rand -hex 32)
echo -e "SECRET_KEY: ${YELLOW}${SECRET_KEY:0:20}...${NC}"

# ============================================
# TELEGRAM BOTS
# ============================================
echo ""
echo -e "${GREEN}[6/10] Telegram Bots${NC}"
echo "Si no tienes, presiona Enter para omitir cada uno"

read -p "PULSEBOT_TOKEN: " PULSEBOT_TOKEN
read -p "MOMENTUM_BOT_TOKEN: " MOMENTUM_BOT_TOKEN
read -p "STOPFRAUDE_BOT_TOKEN: " STOPFRAUDE_BOT_TOKEN

TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 16)
TELEGRAM_WEBHOOK_URL="https://${DOMAIN}/api/telegram/webhook"

# ============================================
# TWITTER/REDDIT (OPCIONAL)
# ============================================
echo ""
echo -e "${GREEN}[7/10] APIs de Redes Sociales (Opcional)${NC}"
echo "Para Pulse IA - Presiona Enter si no tienes"

read -p "Twitter API Key: " TWITTER_API_KEY
read -p "Twitter API Secret: " TWITTER_API_SECRET
read -p "Twitter Bearer Token: " TWITTER_BEARER_TOKEN
read -p "Reddit Client ID: " REDDIT_CLIENT_ID
read -p "Reddit Client Secret: " REDDIT_CLIENT_SECRET

# ============================================
# EMAIL (BREVO)
# ============================================
echo ""
echo -e "${GREEN}[8/10] Email SMTP (Brevo)${NC}"
echo "Si no tienes, presiona Enter para omitir"

read -p "Brevo SMTP User: " BREVO_SMTP_USER
read -p "Brevo SMTP Password: " BREVO_SMTP_PASSWORD

# ============================================
# CRYPTO WALLETS
# ============================================
echo ""
echo -e "${GREEN}[9/10] Wallets de Crypto (Direcciones Públicas)${NC}"

read -p "Bitcoin Wallet: " BTC_WALLET
read -p "Ethereum Wallet: " ETH_WALLET
USDT_ETH_WALLET=${ETH_WALLET}

# ============================================
# PAYMENT GATEWAYS (OPCIONAL)
# ============================================
echo ""
echo -e "${GREEN}[10/10] Payment Gateways (Opcional)${NC}"
echo "Presiona Enter para omitir"

read -p "PagoPar Public Key: " PAGOPAR_PUBLIC_KEY
read -p "PagoPar Private Key: " PAGOPAR_PRIVATE_KEY

# ============================================
# GENERAR ARCHIVO .ENV RAÍZ
# ============================================

cat > "$OUTPUT_FILE" <<EOF
# ==================================
# CONFIGURACIÓN GENERADA AUTOMÁTICAMENTE
# Fecha: $(date)
# ==================================

# ⚠️  NUNCA SUBIR ESTE ARCHIVO A GIT
# ⚠️  Este archivo contiene claves reales

# ==================================
# DOMINIO Y URLs
# ==================================
REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}

# ==================================
# AGENTE DEVELOPER - OpenRouter
# ==================================
OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
OPENROUTER_MODEL_ID_HIGH=anthropic/claude-sonnet-4.5
OPENROUTER_MODEL_ID_LOW=openai/gpt-4o-mini
OPENROUTER_EMBEDDING_MODEL=text-embedding-ada-002

# Anthropic Fallback (Opcional)
ANTHROPIC_API_KEY_FALLBACK=${ANTHROPIC_API_KEY_FALLBACK}

# ==================================
# POSTGRESQL (RAG Database)
# ==================================
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}

# ==================================
# WATCHER
# ==================================
WATCHER_CHECK_INTERVAL=3600
EOF

echo ""
echo -e "${GREEN}✅ Archivo .env creado exitosamente!${NC}"

# ============================================
# GENERAR ARCHIVO BACKEND/.ENV
# ============================================

cat > "$OUTPUT_BACKEND" <<EOF
# ==================================
# BACKEND .ENV - Claves Reales
# Fecha: $(date)
# ==================================

# Database
MONGO_URL=mongodb://mongodb:27017/guarani_appstore
USE_MONGODB=true

# JWT & Security
JWT_SECRET=${JWT_SECRET}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720
SECRET_KEY=${SECRET_KEY}

# CORS
CORS_ORIGINS=https://${DOMAIN},https://www.${DOMAIN},https://agente.${DOMAIN}

# URLs
FRONTEND_URL=https://${DOMAIN}
ADMIN_EMAIL=admin@${DOMAIN}

# Telegram Bots
PULSEBOT_TOKEN=${PULSEBOT_TOKEN}
MOMENTUM_BOT_TOKEN=${MOMENTUM_BOT_TOKEN}
STOPFRAUDE_BOT_TOKEN=${STOPFRAUDE_BOT_TOKEN}
TELEGRAM_WEBHOOK_URL=${TELEGRAM_WEBHOOK_URL}
TELEGRAM_WEBHOOK_SECRET=${TELEGRAM_WEBHOOK_SECRET}

# LLM Integration
EMERGENT_LLM_KEY=
OPENAI_API_KEY=
CLAUDE_API_KEY=

# Twitter/X API
TWITTER_API_KEY=${TWITTER_API_KEY}
TWITTER_API_SECRET=${TWITTER_API_SECRET}
TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN}
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# Reddit API
REDDIT_CLIENT_ID=${REDDIT_CLIENT_ID}
REDDIT_CLIENT_SECRET=${REDDIT_CLIENT_SECRET}
REDDIT_USER_AGENT=guaraniappstore/1.0

# Email (Brevo SMTP)
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=${BREVO_SMTP_USER}
BREVO_SMTP_PASSWORD=${BREVO_SMTP_PASSWORD}
BREVO_FROM_EMAIL=noreply@${DOMAIN}
BREVO_FROM_NAME=GuaraniAppStore

# Crypto Wallets
BTC_WALLET=${BTC_WALLET}
ETH_WALLET=${ETH_WALLET}
USDT_ETH_WALLET=${USDT_ETH_WALLET}

# Payment Gateways
PAGOPAR_PUBLIC_KEY=${PAGOPAR_PUBLIC_KEY}
PAGOPAR_PRIVATE_KEY=${PAGOPAR_PRIVATE_KEY}
PAGOPAR_ENV=production
PAGOPAR_PRODUCTION_URL=https://api.pagopar.com
EOF

echo -e "${GREEN}✅ Archivo .env.backend creado exitosamente!${NC}"
echo ""
echo "=============================================="
echo -e "${YELLOW}📋 PRÓXIMOS PASOS:${NC}"
echo "=============================================="
echo ""
echo "1. Revisa y verifica los archivos generados:"
echo "   - .env (raíz del proyecto)"
echo "   - .env.backend (para backend/)"
echo ""
echo "2. Copia .env.backend a backend/.env:"
echo "   cp .env.backend backend/.env"
echo ""
echo "3. Transferir al VPS (elige una opción):"
echo ""
echo "   Opción A - SCP (recomendado):"
echo "   scp .env usuario@ip-vps:/opt/GuaraniAppStore-V2.5/.env"
echo "   scp backend/.env usuario@ip-vps:/opt/GuaraniAppStore-V2.5/backend/.env"
echo ""
echo "   Opción B - GitHub Secrets (ver GITHUB_SECRETS.md)"
echo ""
echo "4. NUNCA subas estos archivos a Git"
echo "   (Ya están en .gitignore)"
echo ""
echo "=============================================="
echo -e "${GREEN}✅ Generación completada!${NC}"
echo "=============================================="
EOF

chmod +x /app/generate_env.sh
