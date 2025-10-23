# 🚀 Inicio Rápido - GuaraniAppStore V2.5 Pro

## Para Desarrollo Local (Con Docker)

```bash
# 1. Clonar proyecto
git clone <tu-repo>
cd guarani-appstore

# 2. Configurar entorno
cp .env.docker .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 3. Editar backend/.env con tus API keys
nano backend/.env

# 4. Iniciar en modo desarrollo
docker compose -f docker-compose.dev.yml up -d

# 5. Abrir navegador
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

✅ **Hot reload activado** - Los cambios en código se reflejan automáticamente

---

## Para Deployment en VPS

```bash
# 1. En tu VPS, instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Transferir proyecto al VPS
scp -r ./guarani-appstore user@vps-ip:/home/user/

# 3. En el VPS, configurar
cd guarani-appstore
cp .env.docker .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Editar archivos .env con valores de producción
nano .env
nano backend/.env
nano frontend/.env

# 4. Verificar configuración
./scripts/pre-deploy-check.sh

# 5. Deploy
./scripts/deploy.sh

# 6. Configurar SSL (opcional pero recomendado)
sudo certbot --nginx -d tu-dominio.com
```

---

## Comandos Útiles

### Ver logs
```bash
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
```

### Reiniciar servicios
```bash
docker compose restart
docker compose restart backend
```

### Parar todo
```bash
docker compose down
```

### Backup de base de datos
```bash
./scripts/backup.sh
```

### Limpiar Docker
```bash
./scripts/docker-cleanup.sh
```

---

## Solución de Problemas Rápidos

### Backend no inicia
```bash
docker compose logs backend
```

### Frontend muestra error de conexión
Verifica que `REACT_APP_BACKEND_URL` en `frontend/.env` apunte al backend correcto.

### Base de datos no conecta
```bash
docker compose restart postgres
docker compose logs postgres
```

---

## Próximos Pasos

1. ✅ **Configurar API Keys**: Edita `backend/.env` con tus credenciales
   - Ver [SECURITY.md](./SECURITY.md) para dónde obtenerlas

2. 🔐 **SSL en producción**: Configura Let's Encrypt
   - Ver [DEPLOYMENT.md](./DEPLOYMENT.md#configuración-ssl-https)

3. 🧪 **Testing**: Prueba los endpoints
   ```bash
   curl http://localhost:8001/health
   ```

4. 📚 **Documentación completa**:
   - [README.md](./README.md) - Overview general
   - [SECURITY.md](./SECURITY.md) - Configuración de seguridad
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía completa de deployment
   - [DOCKER_ARCHITECTURE.md](./DOCKER_ARCHITECTURE.md) - Arquitectura

---

## ⚡ TL;DR - Un comando para desarrollo

```bash
cp .env.docker .env && \
cp backend/.env.example backend/.env && \
cp frontend/.env.example frontend/.env && \
docker compose -f docker-compose.dev.yml up -d && \
echo "✅ Todo listo! Frontend: http://localhost:3000"
```

**⚠️ Recuerda editar backend/.env con tus API keys**
