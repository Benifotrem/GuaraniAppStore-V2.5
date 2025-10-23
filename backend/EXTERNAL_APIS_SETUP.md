# GuaraniAppStore V2.5 Pro - Configuración de APIs Externas

## 📋 Resumen de Implementación

Se han implementado 4 servicios principales de integración con APIs externas:

### ✅ Servicios Implementados

1. **Google Cloud Vision API** (OCR para facturas/documentos)
2. **CoinGecko API** (Datos de criptomonedas en tiempo real)
3. **Etherscan API** (Datos blockchain de Ethereum)
4. **Google OAuth 2.0** (Acceso a Calendar, Sheets, Blogger del usuario)

### 📦 Dependencias Instaladas

```bash
google-cloud-vision      # OCR con Google Cloud
pycoingecko             # API de CoinGecko
etherscan-python        # API de Etherscan  
redis                   # Caching
apify-client           # Web automation
outscraper             # Web scraping
google-api-python-client # Google APIs
google-auth-oauthlib    # Google OAuth
```

---

## 🔧 Configuración Requerida

### 1. Google Cloud Vision API (OCR)

**Arquitectura**: Service Account (servidor centralizado, sin intervención del usuario)

**Pasos de configuración**:

1. Crear proyecto en Google Cloud Console (https://console.cloud.google.com)
2. Habilitar "Cloud Vision API"
3. Crear Service Account y descargar JSON de credenciales
4. Colocar el archivo JSON en `/app/backend/google_credentials.json`
5. Configurar en `.env`:
   ```bash
   GOOGLE_APPLICATION_CREDENTIALS=/app/backend/google_credentials.json
   GOOGLE_CLOUD_PROJECT=your_project_id
   ```

**Endpoints disponibles**:
- `POST /api/ocr/process` - Procesar imagen para OCR (requiere autenticación)

**Uso**:
```bash
curl -X POST "http://localhost:8001/api/ocr/process?language_hint=es" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@factura.jpg"
```

---

### 2. CoinGecko API (Criptomonedas)

**Estado**: ✅ **FUNCIONA SIN CONFIGURACIÓN** (usa tier gratuito)

**Opcional - Mejorar rate limits**:
- Obtener API key en https://www.coingecko.com/en/api/pricing
- Agregar a `.env`: `COINGECKO_API_KEY=your_key_here`

**Endpoints disponibles**:
- `GET /api/crypto/price/{coin_id}?vs_currency=usd` - Precio de una crypto
- `GET /api/crypto/top?limit=50` - Top 50 criptomonedas por market cap

**Uso**:
```bash
# Obtener precio de Bitcoin
curl "http://localhost:8001/api/crypto/price/bitcoin?vs_currency=usd"

# Top 50 cryptos
curl "http://localhost:8001/api/crypto/top?limit=50"
```

**Caching**: Datos cacheados por 60 segundos para optimizar rate limits

---

### 3. Etherscan API (Blockchain Ethereum)

**Pasos de configuración**:

1. Crear cuenta en https://etherscan.io/
2. Generar API Key en "API Keys" section
3. Configurar en `.env`:
   ```bash
   ETHERSCAN_API_KEY=your_etherscan_api_key_here
   ```

**Endpoints disponibles**:
- `GET /api/blockchain/eth/balance/{address}` - Balance de ETH
- `GET /api/blockchain/verify/{tx_hash}?network=ethereum` - Verificar transacción

**Uso**:
```bash
# Obtener balance ETH
curl "http://localhost:8001/api/blockchain/eth/balance/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Verificar transacción
curl "http://localhost:8001/api/blockchain/verify/0xabc123...?network=ethereum"
```

**BSCScan** (Binance Smart Chain): Pendiente implementación completa

---

### 4. Google OAuth 2.0 (Calendar, Sheets, Blogger)

**Arquitectura**: OAuth 2.0 por usuario (cada usuario autoriza su propia cuenta)

**Pasos de configuración**:

1. Ir a Google Cloud Console (mismo proyecto que Vision API)
2. Habilitar APIs: "Google Calendar API", "Google Sheets API", "Blogger API"
3. Crear "OAuth 2.0 Client ID" (tipo "Web application")
4. Agregar redirect URI: `http://localhost:8001/api/google/oauth/callback`
5. Descargar credenciales y extraer `client_id` y `client_secret`
6. Configurar en `.env`:
   ```bash
   GOOGLE_OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
   GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8001/api/google/oauth/callback
   ```

**Endpoints disponibles**:
- `GET /api/google/oauth/authorize` - Obtener URL de autorización

**Flujo de autorización**:
1. Frontend llama a `/api/google/oauth/authorize`
2. Usuario visita la URL devuelta
3. Usuario autoriza acceso en Google
4. Google redirige a `redirect_uri` con código
5. Backend intercambia código por tokens (refresh token guardado por usuario)
6. Backend usa refresh token para acceder a Calendar/Sheets/Blogger

**⚠️ Implementación pendiente**: 
- Callback handler (`/api/google/oauth/callback`)
- Token storage en base de datos por usuario
- Refresh token logic
- Endpoints específicos de Calendar/Sheets/Blogger

---

## 📝 Variables de Entorno (.env)

Copiar estas variables a `/app/backend/.env` y completar con valores reales:

```bash
# ============================================
# GOOGLE CLOUD VISION API (OCR)
# ============================================
GOOGLE_APPLICATION_CREDENTIALS=/app/backend/google_credentials.json
GOOGLE_CLOUD_PROJECT=your_project_id

# ============================================
# COINGECKO API (OPCIONAL)
# ============================================
COINGECKO_API_KEY=your_coingecko_api_key_optional

# ============================================
# ETHERSCAN & BSCSCAN APIs
# ============================================
ETHERSCAN_API_KEY=your_etherscan_api_key
BSCSCAN_API_KEY=your_bscscan_api_key

# ============================================
# GOOGLE OAUTH CREDENTIALS
# Para Calendar, Sheets, Blogger
# ============================================
GOOGLE_OAUTH_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_client_secret
GOOGLE_OAUTH_REDIRECT_URI=http://localhost:8001/api/google/oauth/callback

# ============================================
# APIFY API (WEB AUTOMATION)
# ============================================
APIFY_API_KEY=your_apify_api_key

# ============================================
# OUTSCRAPER API (WEB SCRAPING)
# ============================================
OUTSCRAPER_API_KEY=your_outscraper_api_key

# ============================================
# REDIS (CACHING)
# ============================================
REDIS_URL=redis://localhost:6379
```

---

## 🎯 Próximos Pasos de Implementación

### Prioridad Alta
1. **Completar Google OAuth flow**:
   - Implementar callback handler
   - Almacenar tokens por usuario en DB
   - Implementar refresh logic
   
2. **Endpoints de Google Calendar**:
   - Crear evento en calendar del usuario
   - Listar eventos
   - Actualizar/eliminar eventos

3. **Endpoints de Google Sheets**:
   - Leer/escribir en sheets del usuario
   - Crear nuevas hojas
   - Exportar datos

4. **Endpoints de Google Blogger**:
   - Crear posts automáticos
   - Listar blogs del usuario

### Prioridad Media
5. **BSCScan API completa** (Binance Smart Chain)
6. **Apify integration** (automatización web)
7. **Outscraper integration** (scraping de Google Maps, etc.)

### Optimizaciones
8. **Redis caching avanzado**
9. **Rate limiting por usuario**
10. **Fraud detection en transacciones blockchain**

---

## 🧪 Testing de APIs

### Test CoinGecko (funciona ahora sin configuración):
```bash
curl "http://localhost:8001/api/crypto/price/bitcoin"
curl "http://localhost:8001/api/crypto/top?limit=10"
```

### Test Google Vision (requiere configuración):
```bash
# Primero hacer login para obtener token
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@guaraniappstore.com","password":"admin123"}'

# Luego usar el token para OCR
curl -X POST "http://localhost:8001/api/ocr/process" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_image.jpg"
```

### Test Etherscan (requiere API key):
```bash
curl "http://localhost:8001/api/blockchain/eth/balance/0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

---

## 📚 Recursos Adicionales

- **Google Cloud Vision**: https://cloud.google.com/vision/docs
- **CoinGecko API**: https://www.coingecko.com/en/api
- **Etherscan API**: https://docs.etherscan.io/
- **Google OAuth 2.0**: https://developers.google.com/identity/protocols/oauth2
- **Google Calendar API**: https://developers.google.com/calendar/api
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Blogger API**: https://developers.google.com/blogger

---

## ⚠️ Notas Importantes

1. **Google Cloud Vision** requiere billing habilitado (primeros 1000 requests/mes gratis)
2. **CoinGecko** tier gratuito tiene rate limit de 5-15 calls/min
3. **Etherscan** tier gratuito: 5 calls/segundo, 100,000 calls/día
4. **Google OAuth** requiere configurar pantalla de consentimiento en Google Cloud Console
5. Todos los servicios tienen fallback gracioso si API keys no están configuradas
6. El código está diseñado para ser modular y fácil de extender

---

## 🛠️ Troubleshooting

### "Google Cloud Vision no está disponible"
- Verificar que `GOOGLE_APPLICATION_CREDENTIALS` apunta al archivo JSON correcto
- Verificar que el archivo JSON existe y tiene permisos de lectura
- Verificar que Vision API está habilitada en Google Cloud Console

### "CoinGecko API rate limit exceeded"
- Implementar API key de CoinGecko Demo plan ($129/mes, 30 calls/min)
- O aumentar el cache TTL en `external_apis_service.py`

### "Etherscan API error"
- Verificar que `ETHERSCAN_API_KEY` está configurada correctamente
- Verificar límites de rate (5 calls/segundo en tier gratuito)
- Considerar upgrade a plan Pro si necesitas más requests

### "Google OAuth credentials missing"
- Verificar que las 3 variables de OAuth están configuradas en .env
- Verificar que el redirect_uri coincide exactamente con el configurado en Google Cloud Console
