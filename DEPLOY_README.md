# 📦 Archivos de Deployment - GuaraniAppStore V2.5 Pro

## 📁 Estructura de Archivos de Deployment

```
/app/
├── docker-compose.yml          # Configuración principal de Docker Compose
├── .env.example                # Template de variables de entorno
├── deploy.sh                   # Script automatizado de deployment
├── DEPLOYMENT.md               # Guía completa de deployment con Cloudflare
├── SECURITY.md                 # Documentación de seguridad
│
├── backend/
│   ├── Dockerfile              # Dockerfile para backend FastAPI
│   ├── .env                    # Variables de entorno del backend (crear desde .env.example)
│   └── requirements.txt        # Dependencias de Python
│
├── frontend/
│   ├── Dockerfile              # Dockerfile multi-stage para React
│   ├── nginx.conf              # Configuración de nginx para servir React
│   ├── package.json            # Dependencias de Node.js
│   └── yarn.lock               # Lock file de Yarn
│
└── nginx/
    └── nginx.conf              # Configuración de nginx como reverse proxy + Cloudflare
```

---

## 🚀 Quick Start

### 1. Preparar Variables de Entorno

```bash
# Copiar template
cp .env.example .env
cp .env.example backend/.env

# Editar y configurar
nano .env              # REACT_APP_BACKEND_URL=https://tudominio.com
nano backend/.env      # Configurar todas las variables necesarias
```

### 2. Generar Secrets Seguros

```bash
# JWT Secret
openssl rand -hex 32

# Secret Key
openssl rand -hex 32

# Telegram Webhook Secret
openssl rand -hex 16
```

### 3. Ejecutar Deployment

```bash
# Opción 1: Script automático (recomendado)
./deploy.sh

# Opción 2: Manual
docker-compose build
docker-compose up -d
docker-compose logs -f
```

---

## 🔧 Servicios en Docker Compose

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **mongodb** | 27017 | Base de datos MongoDB 7.0 |
| **backend** | 8001 | API FastAPI (Python 3.11) |
| **frontend** | 3000 | React App + Nginx |
| **nginx** | 80, 443 | Reverse Proxy (opcional) |

---

## 🌐 Configuración con Cloudflare

### DNS Records en Cloudflare

```
Type: A
Name: @
Content: [IP-VPS]
Proxy: ✅ Proxied (Naranja)

Type: A
Name: www
Content: [IP-VPS]
Proxy: ✅ Proxied (Naranja)
```

### SSL/TLS Settings

- **Modo recomendado:** Full
- Always Use HTTPS: ✅ Habilitado
- Automatic HTTPS Rewrites: ✅ Habilitado
- Minimum TLS Version: 1.2

### Ventajas de Usar Cloudflare

✅ SSL/TLS automático y gratuito  
✅ DDoS protection  
✅ CDN global  
✅ Rate limiting  
✅ Web Application Firewall (WAF)  
✅ Bot protection  
✅ Page caching  
✅ Analytics

---

## 📊 Verificación Post-Deployment

### Verificar Servicios

```bash
# Estado de contenedores
docker-compose ps

# Health checks
curl http://localhost:8001/health        # Backend
curl http://localhost:3000               # Frontend
docker exec guarani_mongodb mongosh --eval "db.adminCommand('ping')"  # MongoDB
```

### Verificar desde Internet (con Cloudflare)

```bash
curl https://tudominio.com/api/health    # Debe retornar {"status":"healthy"}
curl https://tudominio.com               # Debe retornar HTML de React
```

---

## 🗄️ Inicialización de Base de Datos

```bash
# Entrar al contenedor backend
docker exec -it guarani_backend bash

# Inicializar servicios
python init_services_mongo_v2.py

# Verificar usuario admin (email: admin@guaraniappstore.com, pass: admin123)
python check_admin.py

# Salir
exit
```

---

## 🔄 Comandos de Mantenimiento

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Reiniciar Servicios

```bash
# Todos
docker-compose restart

# Específico
docker-compose restart backend
docker-compose restart frontend
```

### Actualizar Aplicación

```bash
# Si usas Git
git clone https://github.com/tu-usuario/GuaraniAppStore-V2.5.git
cd GuaraniAppStore-V2.5

# Rebuild y restart
docker-compose build
docker-compose up -d

# O usar el script
./deploy.sh
```

### Backup de MongoDB

```bash
# Crear backup
docker exec guarani_mongodb mongodump --out /data/db/backup
docker cp guarani_mongodb:/data/db/backup ./mongodb_backup_$(date +%Y%m%d)

# Restaurar backup
docker cp ./mongodb_backup_20250124 guarani_mongodb:/data/db/restore
docker exec guarani_mongodb mongorestore /data/db/restore
```

---

## 🔒 Seguridad

### Variables Críticas que DEBES Cambiar

⚠️ **IMPORTANTE:** Antes de deployment, cambiar:

- `JWT_SECRET` - Generar con `openssl rand -hex 32`
- `SECRET_KEY` - Generar con `openssl rand -hex 32`
- `TELEGRAM_WEBHOOK_SECRET` - Generar con `openssl rand -hex 16`
- Tokens de Telegram Bots
- Credenciales de APIs
- Contraseña de PostgreSQL (si se usa)

### Firewall en VPS

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 🐛 Troubleshooting

### Error: "Cannot connect to MongoDB"

```bash
# Verificar que MongoDB está corriendo
docker-compose ps mongodb

# Ver logs
docker-compose logs mongodb

# Reiniciar
docker-compose restart mongodb
```

### Error: "Backend 500 Internal Server Error"

```bash
# Ver logs detallados
docker-compose logs backend | tail -100

# Verificar variables de entorno
docker exec guarani_backend env | grep MONGO_URL

# Reiniciar backend
docker-compose restart backend
```

### Error: "Frontend no carga"

```bash
# Ver logs
docker-compose logs frontend

# Verificar build
docker-compose build frontend --no-cache

# Reiniciar
docker-compose restart frontend
```

### Cloudflare Error 520/521

- Verificar que nginx está corriendo: `docker-compose ps nginx`
- Verificar firewall permite puerto 80: `sudo ufw status`
- Ver logs de nginx: `docker-compose logs nginx`

---

## 📞 Soporte

Para más ayuda, revisar:
- `DEPLOYMENT.md` - Guía completa paso a paso
- `SECURITY.md` - Documentación de seguridad
- Logs de servicios: `docker-compose logs -f`

---

## ✅ Checklist Pre-Deployment

- [ ] Variables de entorno configuradas (`.env` y `backend/.env`)
- [ ] Secrets generados (JWT_SECRET, SECRET_KEY)
- [ ] Docker y Docker Compose instalados
- [ ] Cloudflare DNS configurado
- [ ] Cloudflare SSL/TLS en modo "Full"
- [ ] Firewall configurado en VPS
- [ ] Puerto 80 y 443 abiertos
- [ ] Backup strategy definida

---

**🎉 ¡Listo para deployment!**

Ejecuta: `./deploy.sh` y tu aplicación estará en línea.
