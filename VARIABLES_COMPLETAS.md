# 📋 Lista Completa de Variables de Entorno - GuaraniAppStore V2.5 Pro

## ✅ Variables OBLIGATORIAS para el Funcionamiento Básico

### 🌐 Dominio y URLs
```bash
REACT_APP_BACKEND_URL=https://tudominio.com
FRONTEND_URL=https://tudominio.com
```

### 🔐 Seguridad (JWT y Secrets)
```bash
JWT_SECRET=[Generar con: openssl rand -hex 32]
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=720
SECRET_KEY=[Generar con: openssl rand -hex 32]
```

### 🗄️ MongoDB (Base de Datos Principal)
```bash
MONGO_URL=mongodb://mongodb:27017/guarani_appstore
DB_NAME=guarani_appstore
USE_MONGODB=true
```

### 🐘 PostgreSQL (Base de Datos RAG del Agente)
```bash
POSTGRES_USER=soporte_user_seguro
POSTGRES_PASSWORD=[Generar con: openssl rand -base64 24]
POSTGRES_DB=soporte_db_rag
```

### 🤖 OpenRouter (Agente Developer - OBLIGATORIO)
```bash
OPENROUTER_API_KEY=sk-or-v1-XXXXXXXXXX
OPENROUTER_MODEL_ID_HIGH=anthropic/claude-sonnet-4.5
OPENROUTER_MODEL_ID_LOW=openai/gpt-4o-mini
OPENROUTER_EMBEDDING_MODEL=text-embedding-ada-002
```

### 🌍 CORS
```bash
CORS_ORIGINS=https://tudominio.com,https://www.tudominio.com,https://agente.tudominio.com
```

---

## ⚙️ Variables OPCIONALES (Funcionalidades Adicionales)

### 🤖 Anthropic Direct (Fallback del Agente)
```bash
ANTHROPIC_API_KEY_FALLBACK=sk-ant-api03-XXXXXXXXXX
```

### 📱 Telegram Bots
```bash
# Pulse IA Bot
PULSEBOT_TOKEN=8340604460:XXXXXXXXXX

# Momentum Predictor Bot
MOMENTUM_BOT_TOKEN=8063382537:XXXXXXXXXX

# CryptoShield Bot
STOPFRAUDE_BOT_TOKEN=8225457458:XXXXXXXXXX

# Guarani Assistant Bot
GUARANI_ASSISTANT_BOT_TOKEN=8389331625:XXXXXXXXXX

# Rocio Bot
ROCIO_BOT_TOKEN=8248705316:XXXXXXXXXX

# Telegram Webhooks
TELEGRAM_WEBHOOK_URL=https://tudominio.com/api/telegram/webhook
TELEGRAM_WEBHOOK_SECRET=[Generar con: openssl rand -hex 16]
```

### 🐦 Twitter/X API (Para Pulse IA)
```bash
TWITTER_API_KEY=XXXXXXXXXX
TWITTER_API_SECRET=XXXXXXXXXX
TWITTER_BEARER_TOKEN=XXXXXXXXXX
TWITTER_ACCESS_TOKEN=XXXXXXXXXX
TWITTER_ACCESS_SECRET=XXXXXXXXXX
```

### 🤖 Reddit API (Para Pulse IA)
```bash
REDDIT_CLIENT_ID=XXXXXXXXXX
REDDIT_CLIENT_SECRET=XXXXXXXXXX
REDDIT_USER_AGENT=guaraniappstore/1.0
```

### 📧 Email SMTP (Brevo)
```bash
BREVO_SMTP_HOST=smtp-relay.brevo.com
BREVO_SMTP_PORT=587
BREVO_SMTP_USER=XXXXXXXXXX
BREVO_SMTP_PASSWORD=XXXXXXXXXX
BREVO_FROM_EMAIL=noreply@tudominio.com
BREVO_FROM_NAME=GuaraniAppStore
```

### 🪙 Crypto Wallets (Direcciones Públicas)
```bash
BTC_WALLET=335hN9Mc46GcFbEyLftEUjWVMXGmqzNvHm
ETH_WALLET=0x767e4362DBd2634129DF9Eb071bAD488666dE6e9
USDT_ETH_WALLET=0x767e4362DBd2634129DF9Eb071bAD488666dE6e9
ETHERSCAN_API_KEY=XXXXXXXXXX
```

### 💳 Payment Gateways
```bash
# PagoPar
PAGOPAR_PUBLIC_KEY=XXXXXXXXXX
PAGOPAR_PRIVATE_KEY=XXXXXXXXXX
PAGOPAR_ENV=production
PAGOPAR_PRODUCTION_URL=https://api.pagopar.com

# Stripe
STRIPE_SECRET_KEY=sk_live_XXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXX
```

### 🌐 Google APIs
```bash
GOOGLE_CLIENT_ID=XXXXXXXXXX.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-XXXXXXXXXX
GOOGLE_REDIRECT_URI=https://tudominio.com/api/auth/google/callback
GOOGLE_OAUTH_CLIENT_ID=XXXXXXXXXX.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-XXXXXXXXXX
GOOGLE_APPLICATION_CREDENTIALS=/app/backend/google_credentials.json
GOOGLE_CLOUD_PROJECT=guaraniappstore
```

### 🔍 APIs de Datos
```bash
# CoinGecko / CoinMarketCap
COINGECKO_API_KEY=
COINMARKETCAP_API_KEY=

# Web Scraping
OUTSCRAPER_API_KEY=XXXXXXXXXX
APIFY_TOKEN=apify_api_XXXXXXXXXX
APIFY_API_KEY=apify_api_XXXXXXXXXX

# Blockchain APIs
BSCSCAN_API_KEY=XXXXXXXXXX
```

### 🧠 LLM APIs (Alternativas)
```bash
# Emergent Universal Key
EMERGENT_LLM_KEY=XXXXXXXXXX

# OpenAI Direct
OPENAI_API_KEY=sk-XXXXXXXXXX

# Claude Direct
CLAUDE_API_KEY=sk-ant-api03-XXXXXXXXXX
```

### 🔴 Redis (Cache - Si se implementa)
```bash
REDIS_URL=redis://redis:6379
```

### 👁️ Model Watcher
```bash
WATCHER_CHECK_INTERVAL=3600
```

### 📧 Admin Contact
```bash
ADMIN_EMAIL=admin@tudominio.com
```

---

## 📝 Resumen por Servicio

### Frontend (React)
**Variables necesarias:**
- `REACT_APP_BACKEND_URL`

### Backend Principal (FastAPI)
**Variables necesarias:**
- `MONGO_URL`
- `JWT_SECRET`
- `SECRET_KEY`
- `CORS_ORIGINS`
- `FRONTEND_URL`
- Todas las API keys de servicios que uses (Telegram, Email, etc.)

### Agente Developer (soporte_backend)
**Variables necesarias:**
- `POSTGRES_URL` (generada automáticamente desde POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
- `OPENROUTER_API_KEY` ⚠️ OBLIGATORIA
- `OPENROUTER_MODEL_ID_HIGH`
- `OPENROUTER_MODEL_ID_LOW`
- `OPENROUTER_EMBEDDING_MODEL`
- `ANTHROPIC_API_KEY_FALLBACK` (opcional)
- `MONGO_URL` (para leer datos de la app)

### PostgreSQL RAG
**Variables necesarias:**
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

### Model Watcher
**Variables necesarias:**
- `OPENROUTER_API_KEY`
- `CHECK_INTERVAL`

### Migration Tool
**Variables necesarias:**
- `MONGO_URL`
- `POSTGRES_URL`

---

## 🎯 Variables Mínimas para Arrancar

Si quieres arrancar con lo mínimo funcional:

```bash
# .env (raíz)
REACT_APP_BACKEND_URL=https://tudominio.com
OPENROUTER_API_KEY=sk-or-v1-XXXXXXXXXX
POSTGRES_USER=soporte_user_seguro
POSTGRES_PASSWORD=[generar]
POSTGRES_DB=soporte_db_rag

# backend/.env
MONGO_URL=mongodb://mongodb:27017/guarani_appstore
USE_MONGODB=true
JWT_SECRET=[generar]
SECRET_KEY=[generar]
CORS_ORIGINS=https://tudominio.com
FRONTEND_URL=https://tudominio.com
```

---

## 🔧 Cómo Generar los Secrets

```bash
# JWT Secret (32 bytes hex)
openssl rand -hex 32

# Secret Key (32 bytes hex)
openssl rand -hex 32

# PostgreSQL Password (24 bytes base64, 20 chars)
openssl rand -base64 24 | tr -d "=+/" | cut -c1-20

# Telegram Webhook Secret (16 bytes hex)
openssl rand -hex 16
```

---

## 📍 Dónde se Usan

### En docker-compose.yml
- Sección `environment:` de cada servicio lee del archivo `.env` raíz

### En Dockerfiles
- `ENV` statements o `ARG` para build-time

### En código Python (backend)
- `os.getenv('VARIABLE_NAME')`

### En código React (frontend)
- `process.env.REACT_APP_VARIABLE_NAME`

---

## ✅ Checklist de Configuración

**Antes del primer deployment:**
- [ ] Generar JWT_SECRET y SECRET_KEY
- [ ] Generar POSTGRES_PASSWORD
- [ ] Obtener OPENROUTER_API_KEY
- [ ] Configurar dominio en REACT_APP_BACKEND_URL
- [ ] Configurar CORS_ORIGINS con tu dominio

**Opcional (según funcionalidades):**
- [ ] Telegram bots tokens (si usas bots)
- [ ] Email SMTP (si envías emails)
- [ ] Payment gateways (si procesas pagos)
- [ ] Social media APIs (si usas Pulse IA)

---

## 🚨 Variables que NUNCA se Commitean

Estas variables NUNCA deben estar en Git (ya en .gitignore):
- Cualquier API key (OpenRouter, Anthropic, etc.)
- JWT_SECRET y SECRET_KEY
- Passwords (POSTGRES_PASSWORD, BREVO_SMTP_PASSWORD)
- Tokens de Telegram
- Private keys de payment gateways

**Solo se commitean:**
- `.env.example` (con placeholders)
- Documentación (este archivo)

---

## 📚 Referencias

- **OpenRouter Keys:** https://openrouter.ai/keys
- **Anthropic Keys:** https://console.anthropic.com/
- **Telegram BotFather:** https://t.me/BotFather
- **Brevo SMTP:** https://www.brevo.com/
- **Stripe Keys:** https://dashboard.stripe.com/apikeys

---

**Última actualización:** 2025-01-24
**Versión:** 2.5 Pro con Agente Developer
