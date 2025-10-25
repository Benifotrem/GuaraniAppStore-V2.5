# 🚀 Guía de Deployment con Docker Compose + Cloudflare

## 📋 Requisitos Previos

- VPS con Docker y Docker Compose instalados
- Dominio configurado en Cloudflare
- Acceso SSH al VPS
- Mínimo 2GB RAM, 2 CPU cores, 20GB storage

---

## 1️⃣ Preparación del VPS

### Instalar Docker (si no está instalado)

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

### Configurar Firewall

```bash
# Permitir puertos necesarios
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

---

## 2️⃣ Configuración de Cloudflare

### En el Dashboard de Cloudflare:

1. **DNS Records:**
   ```
   Type: A
   Name: @
   Content: [IP de tu VPS]
   Proxy status: Proxied (naranja)
   TTL: Auto

   Type: A
   Name: www
   Content: [IP de tu VPS]
   Proxy status: Proxied (naranja)
   TTL: Auto
   ```

2. **SSL/TLS Settings:**
   - Ve a SSL/TLS → Overview
   - Selecciona: **"Full"** (recomendado) o **"Flexible"**
   - Habilita: "Always Use HTTPS"
   - Habilita: "Automatic HTTPS Rewrites"

3. **Firewall Rules (Opcional pero recomendado):**
   - Ve a Security → WAF
   - Habilita protección contra bots
   - Configura rate limiting si lo deseas

4. **Page Rules (Opcional):**
   - Crear regla para forzar HTTPS:
     ```
     URL: http://*tudominio.com/*
     Settings: Always Use HTTPS
     ```

5. **Caching:**
   - Ve a Caching → Configuration
   - Browser Cache TTL: 4 hours
   - Purge cache después del deployment

---

## 3️⃣ Deployment en el VPS

### Subir archivos al VPS

```bash
# Opción 1: Clonar desde GitHub (recomendado)
cd /opt
sudo git clone https://github.com/tu-usuario/GuaraniAppStore-V2.5.git
cd GuaraniAppStore-V2.5

# Opción 2: Transferir archivos con SCP
scp -r /ruta/local/app usuario@ip-vps:/opt/GuaraniAppStore-V2.5
```

### Configurar variables de entorno

```bash
cd /opt/guaraniappstore

# Copiar y editar .env del backend
cp .env.example backend/.env
nano backend/.env

# Configurar las siguientes variables CRÍTICAS:
# - REACT_APP_BACKEND_URL=https://tudominio.com
# - JWT_SECRET (generar con: openssl rand -hex 32)
# - SECRET_KEY (generar con: openssl rand -hex 32)
# - MONGO_URL=mongodb://mongodb:27017/guarani_appstore
# - CORS_ORIGINS=https://tudominio.com
# - FRONTEND_URL=https://tudominio.com
# - Tokens de Telegram Bots
# - Credenciales de APIs que uses

# Crear .env en la raíz para docker-compose
nano .env

# Agregar:
REACT_APP_BACKEND_URL=https://tudominio.com
```

### Generar secrets seguros

```bash
# Generar JWT_SECRET
openssl rand -hex 32

# Generar SECRET_KEY
openssl rand -hex 32

# Generar TELEGRAM_WEBHOOK_SECRET
openssl rand -hex 16
```

---

## 4️⃣ Construir y Ejecutar

### Build y Start

```bash
# Construir las imágenes
docker-compose build

# Iniciar todos los servicios
docker-compose up -d

# Verificar que todos los servicios están corriendo
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs específicos
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Verificar Health

```bash
# Verificar backend
curl http://localhost:8001/health

# Verificar frontend
curl http://localhost:3000

# Verificar MongoDB
docker exec -it guarani_mongodb mongosh --eval "db.adminCommand('ping')"
```

---

## 5️⃣ Inicializar Base de Datos

```bash
# Entrar al contenedor del backend
docker exec -it guarani_backend bash

# Ejecutar script de inicialización
python init_services_mongo_v2.py

# Verificar usuario admin
python check_admin.py

# Salir del contenedor
exit
```

---

## 6️⃣ Configurar Webhooks de Telegram (Opcional)

```bash
# Dentro del contenedor backend
docker exec -it guarani_backend python3 -c "
import os
import requests

bots = {
    'PULSEBOT_TOKEN': os.getenv('PULSEBOT_TOKEN'),
    'MOMENTUM_BOT_TOKEN': os.getenv('MOMENTUM_BOT_TOKEN'),
    'STOPFRAUDE_BOT_TOKEN': os.getenv('STOPFRAUDE_BOT_TOKEN'),
}

webhook_url = os.getenv('TELEGRAM_WEBHOOK_URL')
webhook_secret = os.getenv('TELEGRAM_WEBHOOK_SECRET')

for name, token in bots.items():
    if token and token != 'tu_bot_token_aqui':
        url = f'https://api.telegram.org/bot{token}/setWebhook'
        data = {
            'url': webhook_url + '/' + name.lower().replace('_token', ''),
            'secret_token': webhook_secret
        }
        response = requests.post(url, json=data)
        print(f'{name}: {response.json()}')
"
```

---

## 7️⃣ Configuración SSL con Cloudflare

### Cloudflare maneja el SSL automáticamente, pero puedes optimizar:

**Opción 1: Full SSL (Recomendado)**
- Cloudflare → SSL/TLS → Full
- Tu nginx escucha en puerto 80
- Cloudflare maneja HTTPS externamente

**Opción 2: Full (Strict) - Requiere certificado en servidor**
```bash
# Generar certificado self-signed para origen
sudo apt install -y openssl
sudo mkdir -p /opt/guaraniappstore/nginx/ssl

# Generar certificado
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/guaraniappstore/nginx/ssl/privkey.pem \
  -out /opt/guaraniappstore/nginx/ssl/fullchain.pem

# Reiniciar nginx
docker-compose restart nginx
```

---

## 8️⃣ Mantenimiento y Monitoreo

### Comandos útiles

```bash
# Ver logs
docker-compose logs -f --tail=100

# Reiniciar servicios
docker-compose restart backend
docker-compose restart frontend
docker-compose restart mongodb

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra datos)
docker-compose down -v

# Actualizar aplicación
git pull origin main
docker-compose build
docker-compose up -d

# Backup de MongoDB
docker exec guarani_mongodb mongodump --out /data/db/backup
docker cp guarani_mongodb:/data/db/backup ./mongodb_backup_$(date +%Y%m%d)

# Restaurar MongoDB
docker exec -i guarani_mongodb mongorestore /data/db/backup
```

### Monitoreo

```bash
# Ver uso de recursos
docker stats

# Ver espacio en disco
df -h
docker system df

# Limpiar recursos no usados
docker system prune -a
```

---

## 9️⃣ Troubleshooting

### Backend no inicia
```bash
docker-compose logs backend
# Verificar .env variables
# Verificar MongoDB está corriendo
```

### Frontend no carga
```bash
docker-compose logs frontend
# Verificar REACT_APP_BACKEND_URL en .env
# Verificar build correcto
```

### MongoDB connection error
```bash
docker-compose logs mongodb
# Verificar que el contenedor está corriendo
# Verificar MONGO_URL en backend/.env
```

### Cloudflare errores
- Error 520/521: Verificar que nginx está corriendo en puerto 80
- Error 522: Verificar firewall permite puertos 80/443
- Error 525: Revisar configuración SSL/TLS en Cloudflare

---

## 🔒 Checklist de Seguridad

- [ ] JWT_SECRET y SECRET_KEY únicos y seguros
- [ ] Firewall configurado (solo puertos 22, 80, 443)
- [ ] Cloudflare proxy habilitado (naranja)
- [ ] SSL/TLS en modo "Full" o "Full (Strict)"
- [ ] Rate limiting configurado
- [ ] Variables sensibles en .env (no en código)
- [ ] .env agregado a .gitignore
- [ ] Backups automáticos de MongoDB configurados
- [ ] Monitoring y alertas configurados

---

## 📊 URLs de Acceso

Después del deployment:

- **Frontend:** https://tudominio.com
- **Backend API:** https://tudominio.com/api
- **Health Check:** https://tudominio.com/api/health
- **Admin Dashboard:** https://tudominio.com/admin-dashboard
- **Client Dashboard:** https://tudominio.com/client-dashboard

---

## 🆘 Soporte

Si tienes problemas:
1. Revisar logs: `docker-compose logs -f`
2. Verificar Cloudflare dashboard → Analytics
3. Revisar firewall: `sudo ufw status`
4. Testear conectividad: `curl http://localhost:8001/health`

---

**¡Deployment completado! 🎉**
