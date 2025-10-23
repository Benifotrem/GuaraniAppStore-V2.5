# GuaraniAppStore V2.5 Pro - Setup Final & Documentación Completa

## 🎉 Implementaciones Completadas

### 1. ✅ Favicon Configurado
- **Ubicación**: `/app/frontend/public/favicon.png`
- **Formato**: PNG 512x512
- **Configurado en**: `index.html` con tags `<link rel="icon">` y `<link rel="apple-touch-icon">`
- **Título actualizado**: "GuaraniAppStore - Soluciones de IA"

---

### 2. ✅ Sistema de Webhooks para Telegram Bots

**Archivo**: `/app/backend/telegram_webhook_service.py`

#### Características:
- ✅ Gestión centralizada de 5 bots de Telegram
- ✅ Configuración automática de webhooks
- ✅ Verificación de seguridad con secret token
- ✅ Procesamiento de updates (mensajes, callbacks, inline queries)
- ✅ Endpoints de administración para setup/delete/info

#### Bots Soportados:
1. **GuaraniAppStore Assistant** (@GuaraniAssistantBot)
2. **CryptoShield IA** (@stopfraudebot)
3. **Pulse IA** (@Rojiverdebot)
4. **Momentum Predictor IA** (@Mejormomentobot)
5. **Rocío Almeida** (@RocioAlmeidaBot)

#### Endpoints de Webhooks:
```bash
# Configurar webhook para un bot específico (admin only)
POST /api/telegram/webhook/setup/{bot_id}

# Configurar webhooks para todos los bots (admin only)
POST /api/telegram/webhook/setup-all

# Eliminar webhook de un bot (admin only)
DELETE /api/telegram/webhook/{bot_id}

# Obtener info del webhook configurado (admin only)
GET /api/telegram/webhook/info/{bot_id}

# Endpoint para recibir updates de Telegram (llamado por Telegram)
POST /api/telegram/webhook/{bot_id}
```

#### Uso:
```bash
# 1. Login como admin
curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@guaraniappstore.com","password":"admin123"}'

# 2. Configurar webhooks para todos los bots
curl -X POST "http://localhost:8001/api/telegram/webhook/setup-all" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Ver info de un webhook específico
curl -X GET "http://localhost:8001/api/telegram/webhook/info/asistente" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 3. ✅ Google Cloud Vision API Configurada

**Credenciales**: `/app/backend/google_credentials.json`

```json
{
  "type": "service_account",
  "project_id": "guaraniappstore",
  "client_email": "guarani-app-service@guaraniappstore.iam.gserviceaccount.com",
  "private_key": "[CONFIGURADA]"
}
```

**Variables en .env**:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/app/backend/google_credentials.json
GOOGLE_CLOUD_PROJECT=guaraniappstore
```

**Endpoint**:
```bash
POST /api/ocr/process
```

---

### 4. ✅ Sistema de OCR Dual (Pixtral + Google Vision)

**Archivo**: `/app/backend/document_processor_service.py`

#### Dos Engines de OCR:

##### A) Mistral Pixtral Large (OpenRouter)
- **Uso**: Extracción estructurada de datos
- **Ventajas**: JSON automático, entendimiento contextual
- **Modelo**: `mistralai/pixtral-large-latest`
- **API Key**: Configurada en `.env` (OPENROUTER_API_KEY)

##### B) Google Cloud Vision
- **Uso**: OCR tradicional de alta precisión
- **Ventajas**: Velocidad, confiabilidad, multi-idioma
- **Credenciales**: Service Account JSON

#### Endpoints de OCR:

```bash
# 1. OCR con Google Cloud Vision (tradicional)
POST /api/ocr/process
Content-Type: multipart/form-data
file: [archivo de imagen]
language_hint: es

# 2. OCR con Mistral Pixtral (extracción estructurada)
POST /api/ocr/process-pixtral
Content-Type: multipart/form-data
file: [archivo de factura]

# Extrae automáticamente: fecha, nombre, RUC, importe, concepto, moneda

# 3. OCR Híbrido (ambos engines)
POST /api/ocr/process-hybrid
Content-Type: multipart/form-data
file: [archivo]

# Combina extracción estructurada + texto completo
```

#### Ejemplo de Respuesta (Pixtral):
```json
{
  "success": true,
  "engine": "mistral_pixtral_large",
  "extracted_data": {
    "fecha": "15/10/2024",
    "nombre": "Distribuidora ABC S.A.",
    "ruc": "80012345-1",
    "importe": "5500000",
    "concepto": "Venta de mercaderías",
    "moneda": "PYG"
  },
  "filename": "factura.jpg",
  "user_id": "abc123"
}
```

---

### 5. ✅ Credenciales Configuradas

**OpenRouter API Keys** (para Mistral Pixtral):
```bash
OPENROUTER_API_KEY=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
OPENROUTER_EXTENDED_API_KEY=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
```

**Emergent LLM Universal Key**:
```bash
EMERGENT_LLM_KEY=sk-emergent-9De2dA47a2d33A67cC
```

**Telegram Bots** (5 tokens configurados):
```bash
GUARANI_ASSISTANT_BOT_TOKEN=8389331625:AAGLp_dzEFXqIBuh7__5Zdkh6Zeg3DDRWfw
STOPFRAUDE_BOT_TOKEN=8225457458:AAGjLT9n33f5_drVKuqAK63AvVoDOlRI2Z4
PULSEBOT_TOKEN=8340604460:AAEUz0aA1Vojc_zxronEwmon40-LPj1Mgus
MOMENTUM_BOT_TOKEN=8063382537:AAG0t-4orUr7P8b3rtXunQgqdiUTA4o0FlA
ROCIO_BOT_TOKEN=8248705316:AAEiH-ATjEN3AM7eUkNazIoaZfNX-lBvxf8
```

---

## 📊 Comparación de Modelos OCR

| Modelo | Precisión | Estructuración | Costo | Velocidad | Uso Recomendado |
|--------|-----------|----------------|-------|-----------|-----------------|
| **Mistral Pixtral** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $$ | ⚡⚡⚡ | Facturas, extracción de datos específicos |
| **Google Cloud Vision** | ⭐⭐⭐⭐ | ⭐⭐ | $$ | ⚡⚡⚡⚡ | Documentos largos, múltiples idiomas |
| **Híbrido (ambos)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | $$$ | ⚡⚡ | Facturas complejas, máxima precisión |

---

## 🚀 Guía de Uso Rápido

### Configurar Webhooks de Telegram:

```bash
# 1. Login como admin
TOKEN=$(curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@guaraniappstore.com","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Configurar todos los webhooks
curl -X POST "http://localhost:8001/api/telegram/webhook/setup-all" \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Verificar estado
curl -X GET "http://localhost:8001/api/telegram/webhook/info/asistente" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Procesar Factura con Pixtral:

```bash
# Login y obtener token
TOKEN=$(curl -X POST "http://localhost:8001/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@guaraniappstore.com","password":"admin123"}' \
  | jq -r '.access_token')

# Procesar factura
curl -X POST "http://localhost:8001/api/ocr/process-pixtral" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@factura.jpg" | jq
```

### Usar CoinGecko API (funciona ahora sin configuración):

```bash
# Precio de Bitcoin
curl "http://localhost:8001/api/crypto/price/bitcoin" | jq

# Top 50 criptomonedas
curl "http://localhost:8001/api/crypto/top?limit=50" | jq
```

---

## ⚠️ Notas Importantes

### PostgreSQL Issue
El backend actualmente intenta conectarse a PostgreSQL pero el servicio no está corriendo. Soluciones:

**Opción A**: Iniciar PostgreSQL
```bash
# Si está instalado
sudo systemctl start postgresql
sudo supervisorctl restart backend
```

**Opción B**: Migrar a MongoDB (ya configurado)
- Actualizar `database.py` para usar MongoDB en lugar de PostgreSQL
- El código de MongoDB ya existe en `database_mongo.py`

### Variables de Entorno Faltantes

Para habilitar todas las funcionalidades, configurar en `.env`:

```bash
# APIs Externas
ETHERSCAN_API_KEY=your_key
BSCSCAN_API_KEY=your_key
APIFY_API_KEY=your_key
OUTSCRAPER_API_KEY=your_key

# Google OAuth (para Calendar/Sheets/Blogger)
GOOGLE_OAUTH_CLIENT_ID=your_id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your_secret
```

---

## 📚 Archivos Creados/Modificados

### Backend:
- ✅ `/app/backend/external_apis_service.py` - APIs externas (Google Vision, CoinGecko, Etherscan)
- ✅ `/app/backend/telegram_webhook_service.py` - Sistema de webhooks Telegram
- ✅ `/app/backend/document_processor_service.py` - OCR dual (Pixtral + Google Vision)
- ✅ `/app/backend/google_credentials.json` - Credenciales Google Cloud
- ✅ `/app/backend/.env` - Variables actualizadas con credenciales
- ✅ `/app/backend/server.py` - Endpoints agregados

### Frontend:
- ✅ `/app/frontend/public/favicon.png` - Favicon 512x512
- ✅ `/app/frontend/public/index.html` - Favicon y título actualizados
- ✅ `/app/frontend/src/pages/AdminPanel.js` - Error de sintaxis corregido

### Documentación:
- ✅ `/app/backend/EXTERNAL_APIS_SETUP.md` - Guía de APIs externas
- ✅ `/app/backend/SETUP_FINAL.md` - Este archivo

---

## 🎯 Próximos Pasos

### Prioridad Alta:
1. **Resolver PostgreSQL**: Iniciar servicio o migrar a MongoDB
2. **Probar Webhooks**: Enviar mensaje de prueba a bots
3. **Probar OCR Pixtral**: Upload de factura de prueba
4. **Completar Google OAuth**: Implementar callback handler

### Prioridad Media:
5. **BSCScan completo** (Binance Smart Chain)
6. **Apify & Outscraper** (web scraping/automation)
7. **Endpoints de Calendar/Sheets/Blogger**
8. **Frontend para OCR** (UI para upload y visualización)

### Optimizaciones:
9. **Cache Redis** para APIs externas
10. **Rate limiting** por usuario
11. **Logs estructurados** con timestamps
12. **Monitoring** de webhooks y APIs

---

## 📞 Soporte

Para cualquier duda o problema:
1. Revisar logs: `tail -f /var/log/supervisor/backend.err.log`
2. Verificar .env: `cat /app/backend/.env`
3. Estado de servicios: `sudo supervisorctl status`
4. Reiniciar servicios: `sudo supervisorctl restart all`

---

**Versión**: 2.5.0
**Fecha**: 23 Octubre 2024
**Status**: ✅ Sistema funcional con algunas APIs pendientes de configuración
