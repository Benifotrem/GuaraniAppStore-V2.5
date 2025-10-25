# 🚀 Comandos de Deployment - GuaraniAppStore V2.5

## 📋 Comandos Exactos para Clonar y Deployar

### 1. En tu VPS (conectado por SSH)

```bash
# Ir al directorio de trabajo
cd /opt

# Clonar el repositorio
sudo git clone https://github.com/tu-usuario/GuaraniAppStore-V2.5.git

# Entrar al directorio
cd GuaraniAppStore-V2.5

# Dar permisos al usuario actual
sudo chown -R $USER:$USER .
```

### 2. Configurar Variables de Entorno

```bash
# Copiar template de variables
cp .env.example backend/.env

# Editar variables del backend
nano backend/.env

# CONFIGURAR LAS SIGUIENTES VARIABLES CRÍTICAS:
# - JWT_SECRET (generar con: openssl rand -hex 32)
# - SECRET_KEY (generar con: openssl rand -hex 32)
# - MONGO_URL=mongodb://mongodb:27017/guarani_appstore
# - CORS_ORIGINS=https://tudominio.com
# - FRONTEND_URL=https://tudominio.com
# - TELEGRAM_WEBHOOK_URL=https://tudominio.com/api/telegram/webhook
# - Tokens de tus Telegram Bots
# - Credenciales de APIs que uses

# Crear .env en la raíz
echo "REACT_APP_BACKEND_URL=https://tudominio.com" > .env
```

### 3. Generar Secrets Seguros

```bash
# Generar JWT_SECRET
openssl rand -hex 32
# Copiar el resultado y ponerlo en backend/.env como JWT_SECRET

# Generar SECRET_KEY
openssl rand -hex 32
# Copiar el resultado y ponerlo en backend/.env como SECRET_KEY

# Generar TELEGRAM_WEBHOOK_SECRET
openssl rand -hex 16
# Copiar el resultado y ponerlo en backend/.env como TELEGRAM_WEBHOOK_SECRET
```

### 4. Ejecutar Deployment

```bash
# Hacer ejecutable el script
chmod +x deploy.sh

# Ejecutar deployment automático
./deploy.sh

# O manual:
docker-compose build
docker-compose up -d
```

### 5. Verificar que Todo Funciona

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs
docker-compose logs -f

# Verificar backend
curl http://localhost:8001/health

# Verificar frontend
curl http://localhost:3000

# Verificar MongoDB
docker exec -it guarani_mongodb mongosh --eval "db.adminCommand('ping')"
```

### 6. Inicializar Base de Datos

```bash
# Entrar al contenedor backend
docker exec -it guarani_backend bash

# Inicializar servicios
python init_services_mongo_v2.py

# Verificar admin user (email: admin@guaraniappstore.com, pass: admin123)
python check_admin.py

# Salir
exit
```

### 7. Verificar desde Internet (con Cloudflare)

```bash
# Desde tu máquina local o cualquier lugar
curl https://tudominio.com/api/health

# Debería retornar: {"status":"healthy"}
```

---

## 🔄 Comandos de Mantenimiento

### Ver Logs

```bash
cd /opt/GuaraniAppStore-V2.5

# Todos los logs
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Reiniciar Servicios

```bash
cd /opt/GuaraniAppStore-V2.5

# Reiniciar todo
docker-compose restart

# Reiniciar solo backend
docker-compose restart backend

# Reiniciar solo frontend
docker-compose restart frontend
```

### Actualizar Aplicación

```bash
cd /opt/GuaraniAppStore-V2.5

# Actualizar código desde Git
git pull origin main

# Rebuild y reiniciar
docker-compose build
docker-compose up -d

# Ver logs para verificar
docker-compose logs -f
```

### Detener Aplicación

```bash
cd /opt/GuaraniAppStore-V2.5

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra base de datos)
docker-compose down -v
```

### Backup de MongoDB

```bash
cd /opt/GuaraniAppStore-V2.5

# Crear backup
docker exec guarani_mongodb mongodump --out /data/db/backup

# Copiar backup a host
docker cp guarani_mongodb:/data/db/backup ./mongodb_backup_$(date +%Y%m%d)

# Comprimir backup
tar -czf mongodb_backup_$(date +%Y%m%d).tar.gz ./mongodb_backup_$(date +%Y%m%d)
```

### Restaurar MongoDB

```bash
cd /opt/GuaraniAppStore-V2.5

# Copiar backup al contenedor
docker cp ./mongodb_backup_20250124 guarani_mongodb:/data/db/restore

# Restaurar
docker exec guarani_mongodb mongorestore /data/db/restore
```

---

## 🆘 Troubleshooting

### Backend no arranca

```bash
# Ver logs detallados
docker-compose logs backend | tail -100

# Verificar variables de entorno
docker exec guarani_backend env | grep MONGO_URL

# Reiniciar backend
docker-compose restart backend
```

### Frontend no carga

```bash
# Ver logs
docker-compose logs frontend

# Rebuild sin cache
docker-compose build frontend --no-cache
docker-compose up -d frontend
```

### MongoDB no conecta

```bash
# Verificar que está corriendo
docker-compose ps mongodb

# Ver logs
docker-compose logs mongodb

# Reiniciar
docker-compose restart mongodb
```

### Ver uso de recursos

```bash
# Uso de CPU y RAM por contenedor
docker stats

# Espacio en disco
df -h

# Espacio usado por Docker
docker system df
```

---

## 📞 URLs Importantes

Después del deployment, tu aplicación estará disponible en:

- **Frontend:** https://tudominio.com
- **Backend API:** https://tudominio.com/api
- **Health Check:** https://tudominio.com/api/health
- **Docs API:** https://tudominio.com/api/docs
- **Admin Dashboard:** https://tudominio.com/admin-dashboard
- **Client Dashboard:** https://tudominio.com/client-dashboard

---

## ✅ Verificación Final

Después del deployment, verifica:

- [ ] `docker-compose ps` muestra todos los servicios como "Up"
- [ ] `curl http://localhost:8001/health` retorna `{"status":"healthy"}`
- [ ] `curl http://localhost:3000` retorna HTML de React
- [ ] `curl https://tudominio.com` funciona desde internet
- [ ] Login en admin dashboard funciona
- [ ] MongoDB tiene datos iniciales

---

**¡Listo! Tu aplicación debería estar corriendo en producción** 🎉
