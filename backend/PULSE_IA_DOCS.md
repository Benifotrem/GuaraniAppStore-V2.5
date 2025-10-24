# 📊 Pulse IA - Documentación Completa

## 🎯 Descripción

Pulse IA es un sistema de análisis de sentimiento del mercado crypto que monitorea múltiples fuentes en tiempo real y proporciona insights accionables.

---

## ✅ Componentes Implementados

### 1. **Scrapers de Datos**
- ✅ **RSS Scraper**: 15 fuentes de noticias crypto
- ✅ **Twitter Scraper**: API v2 configurada
- ✅ **Reddit Scraper**: 5 subreddits principales

### 2. **Análisis con IA**
- ✅ **FinBERT**: Modelo pre-entrenado para sentimiento financiero
- ✅ **FOMO/FUD Detection**: Detección de keywords
- ✅ **Trending Keywords Extraction**: Keywords más mencionadas

### 3. **Bot de Telegram**
- ✅ Comandos interactivos
- ✅ Botones inline
- ✅ Sistema de suscripciones
- ✅ Tracking de símbolos

### 4. **API REST**
- ✅ 6 endpoints funcionales
- ✅ Documentación automática (Swagger)
- ✅ MongoDB para almacenamiento

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8001/api/pulse
```

### Endpoints Disponibles

#### 1. **Analizar Sentimiento**
```bash
GET /api/pulse/analyze/{symbol}
```

**Ejemplo:**
```bash
curl http://localhost:8001/api/pulse/analyze/BTC
```

**Response:**
```json
{
  "symbol": "BTC",
  "overall_sentiment": 45,
  "news_sentiment": 38,
  "social_sentiment": 52,
  "trend": "📈 Rising",
  "recommendation": "🟢 Bullish",
  "fomo_score": 35,
  "fud_score": 12,
  "sources_analyzed": 215,
  "trending_keywords": ["bitcoin", "price", "rally", "market", "crypto"]
}
```

#### 2. **Historial de Análisis**
```bash
GET /api/pulse/history/{symbol}?limit=20
```

#### 3. **Cryptos Trending**
```bash
GET /api/pulse/trending
```

**Response:**
```json
[
  {
    "symbol": "BTC",
    "overall_sentiment": 45,
    "trend": "📈 Rising",
    "recommendation": "🟢 Bullish"
  },
  ...
]
```

#### 4. **Estadísticas de Símbolo**
```bash
GET /api/pulse/stats/{symbol}
```

**Response:**
```json
{
  "symbol": "BTC",
  "total_analyses": 30,
  "avg_sentiment": 42.5,
  "max_sentiment": 78,
  "min_sentiment": -15,
  "current_sentiment": 45,
  "sentiment_change_7d": +12
}
```

#### 5. **Health Check**
```bash
GET /api/pulse/health
```

---

## 🤖 Bot de Telegram

### Comandos Disponibles

#### `/start`
Iniciar bot y ver menú principal

#### `/pulse <SYMBOL>`
Analizar sentimiento de una crypto
```
/pulse BTC
/pulse ETH
```

#### `/trending`
Ver análisis de las cryptos más populares

#### `/track <SYMBOL>`
Trackear un símbolo para recibir alertas
```
/track BTC
/track SOL
```

#### `/config`
Ver y modificar configuración personal

#### `/help`
Mostrar ayuda completa

---

## 🚀 Iniciar Servicios

### 1. Backend API (ya corriendo)
```bash
sudo supervisorctl restart backend
```

### 2. Bot de Telegram
```bash
cd /app/backend
bash start_pulse_bot.sh
```

O manualmente:
```bash
cd /app/backend
export $(cat .env | xargs)
python3 pulse_telegram_bot.py
```

---

## 📊 Fuentes de Datos

### RSS Feeds (15)
1. CoinDesk (95% reliability)
2. CoinTelegraph (90% reliability)
3. Decrypt (90% reliability)
4. The Block (95% reliability)
5. Bitcoin Magazine (85% reliability)
6. CryptoSlate (85% reliability)
7. BeInCrypto (80% reliability)
8. NewsBTC (75% reliability)
9. U.Today (75% reliability)
10. Bitcoinist (75% reliability)
11. CoinMarketCap News (90% reliability)
12. Crypto Briefing (85% reliability)
13. AMBCrypto (80% reliability)
14. Crypto News (75% reliability)
15. Bitcoin.com News (80% reliability)

### Reddit Subreddits (5)
- r/cryptocurrency
- r/bitcoin
- r/ethereum
- r/CryptoMarkets
- r/altcoin

### Twitter/X
- 300+ cuentas de influencers crypto
- Búsqueda por hashtags y keywords

---

## 🎯 Métricas de Sentimiento

### Overall Sentiment Score
- **-100 a -60**: 🔴 Muy Bearish
- **-60 a -20**: 🟠 Bearish
- **-20 a +20**: 🟡 Neutral
- **+20 a +60**: 🟢 Bullish
- **+60 a +100**: 🟢🟢 Muy Bullish

### FOMO Score (0-100)
- Detecta keywords de euforia
- >60: Alto nivel de FOMO 🚀
- <30: Bajo nivel de FOMO

### FUD Score (0-100)
- Detecta keywords de miedo
- >60: Alto nivel de FUD ⚠️
- <30: Bajo nivel de FUD

---

## 🔧 Configuración

### Variables de Entorno
```bash
# Twitter API
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_SECRET=your_secret

# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=PulseIA/1.0

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# Database
MONGO_URL=mongodb://localhost:27017/guarani_appstore
```

---

## 📈 Roadmap Completado

- [x] RSS Scraper (15 feeds)
- [x] Twitter API Integration
- [x] Reddit API Integration
- [x] FinBERT Sentiment Analysis
- [x] FOMO/FUD Detection
- [x] Telegram Bot
- [x] API REST (6 endpoints)
- [x] MongoDB Storage
- [x] Trending Keywords
- [x] System Documentation

---

## 🔜 Próximos Servicios

### Momentum Predictor IA
- LSTM para señales de trading
- Predicciones BUY/SELL/HOLD
- Niveles de entrada y salida

### CryptoShield IA
- Autoencoder para detección de fraudes
- Análisis de contratos inteligentes
- Detección de honeypots y rugpulls

---

## 📞 Soporte

Para soporte técnico:
- Telegram: @GuaraniAppStore
- Email: support@guaraniappstore.com

---

**Versión:** 1.0.0  
**Última actualización:** 23 Octubre 2025  
**Estado:** ✅ Producción
