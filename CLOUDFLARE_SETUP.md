# GuaraniAppStore V2.5 Pro - Configuración de Cloudflare para Producción

## 🌐 Guía Completa de Configuración de Cloudflare

---

## 📋 Requisitos Previos

1. **Dominio registrado** (ej: `guaraniappstore.com`)
2. **Cuenta de Cloudflare** (gratuita o plan Pro)
3. **Servidor/VPS** con IP pública
4. **DNS configurado** apuntando a Cloudflare

---

## 🚀 Paso 1: Configuración Inicial de Cloudflare

### 1.1 Agregar Sitio a Cloudflare

1. Login en Cloudflare: https://dash.cloudflare.com
2. Click en "Add a Site"
3. Ingresa tu dominio: `guaraniappstore.com`
4. Selecciona plan (Free es suficiente para empezar)
5. Cloudflare escaneará tus DNS records existentes

### 1.2 Configurar Nameservers

Cloudflare te dará 2 nameservers, ejemplo:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

Ve a tu registrador de dominios (GoDaddy, Namecheap, etc.) y cambia los nameservers a los de Cloudflare.

⏰ **Tiempo de propagación**: 5 minutos a 48 horas (usualmente < 1 hora)

---

## 🔧 Paso 2: Configuración de DNS Records

### 2.1 Records Necesarios

En Cloudflare Dashboard → DNS → Records:

```
Type    Name    Content             Proxy Status    TTL
A       @       YOUR_SERVER_IP      Proxied (🟠)    Auto
A       www     YOUR_SERVER_IP      Proxied (🟠)    Auto
A       api     YOUR_SERVER_IP      Proxied (🟠)    Auto
CNAME   *       guaraniappstore.com Proxied (🟠)    Auto
```

**⚠️ IMPORTANTE**: 
- **Proxied (🟠 naranja)**: Tráfico pasa por Cloudflare (recomendado)
- **DNS Only (☁️ gris)**: Tráfico directo al servidor (bypass Cloudflare)

---

## 🔐 Paso 3: Configuración SSL/TLS

### 3.1 SSL Mode

Cloudflare Dashboard → SSL/TLS → Overview:

**Seleccionar**: `Full (strict)` ✅ RECOMENDADO

Opciones:
- ❌ **Off**: Sin SSL (no usar)
- ❌ **Flexible**: Cloudflare ↔ Cliente usa SSL, Cloudflare ↔ Servidor sin SSL
- ⚠️ **Full**: SSL en ambos lados, pero sin validar certificado del servidor
- ✅ **Full (strict)**: SSL en ambos lados con validación completa

### 3.2 Always Use HTTPS

SSL/TLS → Edge Certificates:
- ✅ **Always Use HTTPS**: ON
- ✅ **HSTS**: ON (Strict-Transport-Security)
- ✅ **Minimum TLS Version**: TLS 1.2

### 3.3 Certificado SSL en el Servidor

Cloudflare Dashboard → SSL/TLS → Origin Server:

1. Click "Create Certificate"
2. Selecciona "Let Cloudflare generate a private key and a CSR"
3. Hostnames: `guaraniappstore.com`, `*.guaraniappstore.com`
4. Validity: 15 years
5. Click "Create"

Cloudflare te dará:
- **Origin Certificate** (guardar como `/etc/ssl/certs/cloudflare_origin.pem`)
- **Private Key** (guardar como `/etc/ssl/private/cloudflare_origin.key`)

**Configurar en Nginx**:
```nginx
server {
    listen 443 ssl http2;
    server_name guaraniappstore.com www.guaraniappstore.com;

    ssl_certificate /etc/ssl/certs/cloudflare_origin.pem;
    ssl_certificate_key /etc/ssl/private/cloudflare_origin.key;

    # Resto de configuración...
}
```

---

## ⚡ Paso 4: Optimización de Performance

### 4.1 Caching

Cloudflare Dashboard → Caching → Configuration:

- **Caching Level**: Standard
- **Browser Cache TTL**: 4 hours
- **Always Online**: ON

### 4.2 Page Rules (para APIs)

Cloudflare Dashboard → Rules → Page Rules:

**Rule 1: No Cache para API**
```
URL: api.guaraniappstore.com/*
Settings:
  - Cache Level: Bypass
  - Disable Performance
```

**Rule 2: Cache para Assets**
```
URL: guaraniappstore.com/static/*
Settings:
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month
```

### 4.3 Speed Settings

Cloudflare Dashboard → Speed → Optimization:

- ✅ **Auto Minify**: JavaScript, CSS, HTML
- ✅ **Brotli**: ON
- ✅ **Early Hints**: ON
- ✅ **Rocket Loader**: OFF (puede romper React)

---

## 🛡️ Paso 5: Configuración de Seguridad

### 5.1 Security Level

Cloudflare Dashboard → Security → Settings:

- **Security Level**: Medium (o High si tienes muchos ataques)
- **Challenge Passage**: 30 minutes

### 5.2 Bot Fight Mode

Cloudflare Dashboard → Security → Bots:

- ✅ **Bot Fight Mode**: ON (plan Free)
- ✅ **Super Bot Fight Mode**: ON (plan Pro+)

### 5.3 Firewall Rules

Cloudflare Dashboard → Security → WAF:

**Rule 1: Bloquear países sospechosos (opcional)**
```
Field: Country
Operator: equals
Value: CN, RU, KP (ejemplo)
Action: Block
```

**Rule 2: Rate Limiting para Login**
```
Field: URI Path
Operator: equals
Value: /api/auth/login
Rate: 5 requests per 60 seconds
Action: Challenge
```

**Rule 3: Permitir Telegram Webhooks**
```
Field: IP Address
Operator: is in
Value: 149.154.160.0/20, 91.108.4.0/22 (IPs de Telegram)
AND
Field: URI Path
Operator: contains
Value: /api/telegram/webhook
Action: Allow
```

---

## 🤖 Paso 6: Configuración Específica para Telegram Webhooks

### 6.1 Rango de IPs de Telegram

Telegram usa estas IPs para webhooks (verificar en https://core.telegram.org/bots/webhooks):
```
149.154.160.0/20
91.108.4.0/22
```

### 6.2 Firewall Rule para Webhooks

Cloudflare Dashboard → Security → WAF → Custom Rules:

```
Name: Allow Telegram Webhooks
Expression:
  (ip.src in {149.154.160.0/20 91.108.4.0/22}) and 
  (http.request.uri.path contains "/api/telegram/webhook")
Action: Allow
```

### 6.3 Variables de Entorno para Webhooks

En tu servidor, actualizar `/app/backend/.env`:

```bash
# URL base de Cloudflare para webhooks
TELEGRAM_WEBHOOK_URL=https://api.guaraniappstore.com/api/telegram/webhook

# O si usas dominio principal
TELEGRAM_WEBHOOK_URL=https://guaraniappstore.com/api/telegram/webhook

# Secret token (ya configurado)
TELEGRAM_WEBHOOK_SECRET=guarani_webhook_secret_2025_secure
```

### 6.4 Configurar Webhooks con Cloudflare URL

Una vez que Cloudflare esté activo:

```bash
# Login como admin
TOKEN=$(curl -X POST "https://guaraniappstore.com/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@guaraniappstore.com","password":"admin123"}' \
  | jq -r '.access_token')

# Configurar webhooks con URL de Cloudflare
curl -X POST "https://guaraniappstore.com/api/telegram/webhook/setup-all" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📊 Paso 7: Configuración de Backend para Cloudflare

### 7.1 Middleware Ya Configurado ✅

El backend ya incluye `CloudflareMiddleware` que:
- ✅ Extrae IP real desde `CF-Connecting-IP`
- ✅ Registra `CF-Ray` para debugging
- ✅ Detecta país del visitante (`CF-IPCountry`)
- ✅ Maneja protocolo original (`CF-Visitor`)

### 7.2 Trusted Proxies

Agregar a `/app/backend/.env`:

```bash
# Cloudflare es un proxy confiable
TRUSTED_PROXIES=cloudflare

# O especificar IPs de Cloudflare (actualizar periódicamente)
# https://www.cloudflare.com/ips/
```

### 7.3 Headers de Cloudflare Disponibles

En el código backend, puedes usar:

```python
from cloudflare_middleware import get_real_ip, get_cf_ray, get_country

@api_router.get('/my-endpoint')
async def my_endpoint(request: Request):
    real_ip = get_real_ip(request)        # IP real del cliente
    cf_ray = get_cf_ray(request)          # CF-Ray ID para debugging
    country = get_country(request)        # Código de país (ej: 'PY')
    
    return {
        'ip': real_ip,
        'cf_ray': cf_ray,
        'country': country
    }
```

---

## ⏱️ Paso 8: Timeouts y Límites de Cloudflare

### 8.1 Límites por Plan

| Feature | Free | Pro | Business | Enterprise |
|---------|------|-----|----------|------------|
| **Connection Timeout** | 100s | 100s | 100s | 600s |
| **Request Timeout** | 100s | 100s | 600s | 600s |
| **Upload Size** | 100MB | 100MB | 500MB | 500MB |

### 8.2 Ajustar Endpoints Largos

Para endpoints que pueden tardar más de 100 segundos (plan Free/Pro):

**Opción A**: Usar procesamiento asíncrono
```python
@api_router.post('/long-task')
async def long_task(background_tasks: BackgroundTasks):
    # Iniciar tarea en background
    task_id = generate_task_id()
    background_tasks.add_task(process_long_task, task_id)
    
    # Devolver inmediatamente
    return {'task_id': task_id, 'status': 'processing'}

@api_router.get('/task-status/{task_id}')
async def get_task_status(task_id: str):
    # Cliente hace polling para ver el estado
    return {'task_id': task_id, 'status': 'completed', 'result': '...'}
```

**Opción B**: Upgrade a plan Business ($200/mes) para 600s timeout

---

## 🔍 Paso 9: Monitoreo y Analytics

### 9.1 Cloudflare Analytics

Cloudflare Dashboard → Analytics:

- **Traffic**: Requests, bandwidth, países
- **Security**: Amenazas bloqueadas
- **Performance**: Cache ratio, tiempo de respuesta
- **DNS**: Queries DNS

### 9.2 Logs (requiere plan Enterprise)

Para debugging detallado, considera:
- **Cloudflare Logs**: $5/GB (Logpush)
- **Worker Analytics**: Incluido con Workers ($5/mes)

### 9.3 Alertas

Cloudflare Dashboard → Notifications:

Configurar alertas para:
- ✅ **DOS Attack**: Detectado ataque DDoS
- ✅ **SSL/TLS**: Certificado por expirar
- ✅ **Origin Error Rate**: Errores 5xx del servidor
- ✅ **Health Check**: Servidor caído

---

## 🧪 Paso 10: Testing de Configuración

### 10.1 Verificar DNS Propagation

```bash
# Check DNS
nslookup guaraniappstore.com

# Check si pasa por Cloudflare (debería devolver IP de Cloudflare, no tu servidor)
dig guaraniappstore.com
```

### 10.2 Verificar SSL

```bash
# SSL Labs Test
https://www.ssllabs.com/ssltest/analyze.html?d=guaraniappstore.com

# Debería obtener A+ rating
```

### 10.3 Verificar Headers de Cloudflare

```bash
curl -I https://guaraniappstore.com

# Deberías ver estos headers:
# CF-Ray: xxxxx
# CF-Cache-Status: DYNAMIC/HIT/MISS
# Server: cloudflare
```

### 10.4 Verificar IP Real en Backend

```bash
# Hacer request y verificar logs del backend
curl https://guaraniappstore.com/api/health

# En logs del backend deberías ver:
# "Real IP from Cloudflare: YOUR_REAL_IP"
# No la IP de Cloudflare
```

### 10.5 Testing de Webhooks Telegram

```bash
# Verificar info de webhook
curl -X GET "https://guaraniappstore.com/api/telegram/webhook/info/asistente" \
  -H "Authorization: Bearer TOKEN"

# Debería mostrar:
# "webhook_url": "https://guaraniappstore.com/api/telegram/webhook/asistente"
```

---

## 🎯 Checklist de Configuración Final

### DNS & SSL
- [ ] Nameservers cambiados a Cloudflare
- [ ] Records DNS configurados (A, CNAME)
- [ ] Proxy Status en "Proxied" (🟠)
- [ ] SSL Mode: Full (strict)
- [ ] Always Use HTTPS: ON
- [ ] Certificado Origin instalado en servidor

### Performance
- [ ] Page Rules configuradas (No cache API, Cache assets)
- [ ] Auto Minify habilitado
- [ ] Brotli habilitado
- [ ] Rocket Loader deshabilitado (React)

### Seguridad
- [ ] Bot Fight Mode: ON
- [ ] Security Level: Medium/High
- [ ] Firewall rule para Telegram IPs
- [ ] Rate limiting para /auth/login

### Backend
- [ ] CloudflareMiddleware agregado a server.py
- [ ] TELEGRAM_WEBHOOK_URL actualizada con dominio Cloudflare
- [ ] Webhooks reconfigurados con nueva URL
- [ ] Testing de IP real funcionando

### Monitoreo
- [ ] Alertas configuradas (DOS, SSL, Origin errors)
- [ ] Analytics dashboard revisado

---

## 📞 Soporte y Debugging

### Logs de Cloudflare

Para ver requests en tiempo real:
1. Cloudflare Dashboard → Analytics → Logs
2. Plan Free: últimas 24 horas
3. Plan Pro+: últimas 72 horas

### Common Issues

**Issue 1: "Too Many Redirects"**
- Causa: SSL Mode incorrecto
- Solución: Cambiar a Full (strict) y asegurar que servidor tiene certificado

**Issue 2: "521 Web Server Is Down"**
- Causa: Servidor caído o firewall bloqueando IPs de Cloudflare
- Solución: Verificar que servidor permite IPs de Cloudflare

**Issue 3: "524 A Timeout Occurred"**
- Causa: Request tarda más de 100 segundos
- Solución: Implementar procesamiento asíncrono o upgrade a Business plan

**Issue 4: "Webhooks de Telegram no llegan"**
- Causa: Firewall bloqueando IPs de Telegram
- Solución: Agregar firewall rule para permitir IPs de Telegram

### Contacto Cloudflare Support

- **Community**: https://community.cloudflare.com
- **Support Ticket**: Dashboard → Help Center (planes Pro+)
- **Status Page**: https://www.cloudflarestatus.com

---

## 🚀 Resumen de URLs en Producción

| Servicio | URL | Uso |
|----------|-----|-----|
| **Frontend** | https://guaraniappstore.com | Landing page, dashboard |
| **API Backend** | https://api.guaraniappstore.com | REST API |
| **Webhooks Telegram** | https://guaraniappstore.com/api/telegram/webhook | Recibir updates de Telegram |
| **Admin Panel** | https://guaraniappstore.com/admin | Panel de administración |

---

**Versión**: 1.0  
**Última actualización**: 23 Octubre 2024  
**Status**: ✅ Listo para producción con Cloudflare
