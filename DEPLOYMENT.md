# Guía de Deployment - GuaraniAppStore V2.5 Pro

## 🐳 Deployment con Docker Compose

## 🔧 Desarrollo Local con Docker

Para desarrollo local con hot reload:

```bash
# Iniciar servicios de desarrollo
docker compose -f docker-compose.dev.yml up -d

# Ver logs
docker compose -f docker-compose.dev.yml logs -f

# Los cambios en el código se reflejarán automáticamente
```

**Características del modo desarrollo:**
- Hot reload en backend (FastAPI)
- Hot reload en frontend (React)
- PostgreSQL expuesto en puerto 5432
- Volúmenes montados para cambios en vivo

---


### Requisitos del VPS

- **Sistema Operativo**: Ubuntu 20.04+ / Debian 11+
- **RAM**: Mínimo 2GB (recomendado 4GB)
- **Disco**: Mínimo 20GB
- **Docker**: 20.10+
- **Docker Compose**: 2.0+

### Instalación de Docker en VPS

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose-plugin

# Verificar instalación
docker --version
docker compose version
```

## 📦 Preparación del Proyecto

### 1. Clonar o transferir el proyecto al VPS

```bash
# Opción A: Desde Git
git clone https://github.com/tu-usuario/guarani-appstore.git
cd guarani-appstore

# Opción B: Transferir con SCP
scp -r /ruta/local/guarani-appstore user@vps-ip:/home/user/
```

### 2. Configurar variables de entorno

```bash
# Copiar archivos de ejemplo
cp .env.docker .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Editar .env principal
nano .env
```

**Configuración mínima en `.env`:**
```bash
POSTGRES_USER=guarani_user
POSTGRES_PASSWORD=TU_PASSWORD_SEGURO_AQUI  # ⚠️ CAMBIAR
POSTGRES_DB=guarani_appstore
REACT_APP_BACKEND_URL=https://tu-dominio.com
DOMAIN=tu-dominio.com
```

**Editar `backend/.env`:**
```bash
nano backend/.env
```

Ver [SECURITY.md](./SECURITY.md) para la lista completa de variables requeridas.

**Editar `frontend/.env`:**
```bash
nano frontend/.env
```
```bash
REACT_APP_BACKEND_URL=https://tu-dominio.com
```

### 3. Configurar Nginx para tu dominio

```bash
nano nginx/conf.d/guarani.conf
```

Reemplazar `your-domain.com` con tu dominio real.

## 🚀 Deployment

### Opción A: Script automatizado

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Opción B: Manual

```bash
# Build containers
docker compose build

# Iniciar servicios
docker compose up -d

# Ver logs
docker compose logs -f
```

## 🔐 Configuración SSL (HTTPS)

### Con Let's Encrypt (Certbot)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Renovación automática (ya configurado)
sudo systemctl status certbot.timer
```

### Configurar SSL en Nginx

1. Los certificados se guardan en `/etc/letsencrypt/live/tu-dominio.com/`
2. Crear enlace simbólico en el proyecto:

```bash
mkdir -p nginx/ssl
sudo ln -s /etc/letsencrypt/live/tu-dominio.com/fullchain.pem nginx/ssl/
sudo ln -s /etc/letsencrypt/live/tu-dominio.com/privkey.pem nginx/ssl/
```

3. Descomentar líneas SSL en `nginx/conf.d/guarani.conf`
4. Reiniciar nginx: `docker compose restart nginx`

## 🛠️ Comandos Útiles

### Gestión de servicios

```bash
# Ver estado
docker compose ps

# Logs en tiempo real
docker compose logs -f

# Logs de un servicio específico
docker compose logs -f backend
docker compose logs -f frontend

# Reiniciar servicios
docker compose restart
docker compose restart backend

# Parar servicios
docker compose stop

# Parar y eliminar containers
docker compose down

# Parar y eliminar containers + volúmenes
docker compose down -v
```

### Base de datos

```bash
# Acceder a PostgreSQL
docker compose exec postgres psql -U guarani_user -d guarani_appstore

# Backup
chmod +x scripts/backup.sh
./scripts/backup.sh

# Restore
chmod +x scripts/restore.sh
./scripts/restore.sh

# Ver backups
ls -lh backups/
```

### Actualizar aplicación

```bash
# Pull cambios
git pull

# Rebuild y restart
docker compose build
docker compose up -d

# O usar script
./scripts/deploy.sh
```

## 📊 Monitoreo

### Health checks

```bash
# Backend health
curl http://localhost:8001/health

# Check de todos los servicios
docker compose ps
```

### Logs

```bash
# Logs de nginx
tail -f nginx/logs/guarani_access.log
tail -f nginx/logs/guarani_error.log

# Logs de aplicación
docker compose logs --tail=100 backend
docker compose logs --tail=100 frontend
```

## 🔥 Troubleshooting

### Backend no inicia

```bash
# Ver logs
docker compose logs backend

# Verificar conexión a BD
docker compose exec backend python -c "import psycopg2; print('OK')"

# Verificar variables de entorno
docker compose exec backend env | grep POSTGRES
```

### Frontend no carga

```bash
# Rebuild frontend
docker compose build frontend --no-cache
docker compose up -d frontend

# Verificar variable REACT_APP_BACKEND_URL
cat frontend/.env
```

### Base de datos no conecta

```bash
# Ver logs de postgres
docker compose logs postgres

# Verificar que está corriendo
docker compose ps postgres

# Reiniciar postgres
docker compose restart postgres
```

### Errores de permisos

```bash
# Dar permisos a scripts
chmod +x scripts/*.sh

# Permisos de logs nginx
sudo chown -R $USER:$USER nginx/logs
```

## 🔒 Seguridad en Producción

### Checklist de seguridad

- [ ] Cambiar todas las contraseñas por defecto
- [ ] Configurar SSL/HTTPS
- [ ] Configurar firewall (UFW)
- [ ] Limitar acceso SSH
- [ ] Configurar backups automáticos
- [ ] Actualizar sistema regularmente
- [ ] Revisar logs periódicamente

### Configurar Firewall

```bash
# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP y HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activar firewall
sudo ufw enable

# Ver estado
sudo ufw status
```

## 📈 Optimización

### Para alto tráfico

1. Aumentar workers de nginx en `nginx/nginx.conf`
2. Configurar Redis para caché
3. Usar CDN para assets estáticos
4. Optimizar queries de base de datos
5. Implementar rate limiting

## 📞 Soporte

Si encuentras problemas durante el deployment:

- Revisa logs: `docker compose logs -f`
- Consulta [SECURITY.md](./SECURITY.md) para configuración
- Email: admin@guaraniappstore.com

---

**Última actualización:** Enero 2025