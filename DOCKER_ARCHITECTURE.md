# Arquitectura Docker - GuaraniAppStore V2.5 Pro

## 📊 Diagrama de Servicios

```
┌─────────────────────────────────────────────────────────────┐
│                         Internet                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Nginx (Port 80/443)  │
              │   Reverse Proxy + SSL  │
              └────────┬───────┬───────┘
                       │       │
         ┌─────────────┘       └─────────────┐
         ▼                                   ▼
┌──────────────────┐              ┌──────────────────┐
│  Frontend (3000) │              │  Backend (8001)  │
│  React + Nginx   │              │     FastAPI      │
│  Static Files    │              │   Python 3.11    │
└──────────────────┘              └─────────┬────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │ PostgreSQL (5432)│
                                  │   Database       │
                                  └──────────────────┘
```

## 🐳 Contenedores

### 1. **nginx** (Reverse Proxy)
- **Imagen**: `nginx:alpine`
- **Puertos**: 80, 443
- **Función**: 
  - Enrutamiento de peticiones
  - Terminación SSL
  - Compresión gzip
  - Headers de seguridad
- **Volúmenes**:
  - `./nginx/nginx.conf` → `/etc/nginx/nginx.conf`
  - `./nginx/conf.d` → `/etc/nginx/conf.d`
  - `./nginx/ssl` → `/etc/nginx/ssl`

### 2. **frontend** (React App)
- **Build**: Multi-stage (node:18-alpine → nginx:alpine)
- **Puerto**: 3000 (interno), 80 (expuesto)
- **Función**:
  - Servir aplicación React compilada
  - Assets estáticos
  - Client-side routing
- **Variables de entorno**:
  - `REACT_APP_BACKEND_URL`

### 3. **backend** (FastAPI)
- **Build**: Custom (python:3.11-slim)
- **Puerto**: 8001
- **Función**:
  - API REST
  - Lógica de negocio
  - Autenticación
  - Integración con servicios externos
- **Dependencias**:
  - PostgreSQL (espera health check)
- **Comando**: `alembic upgrade head && uvicorn server:app`

### 4. **postgres** (Database)
- **Imagen**: `postgres:15-alpine`
- **Puerto**: 5432
- **Función**: Base de datos principal
- **Volumen persistente**: `postgres_data`
- **Health check**: `pg_isready`

## 🌐 Networking

### Red: `guarani_network`
- Tipo: Bridge
- Permite comunicación entre contenedores
- Aislamiento del host

### Resolución DNS interna:
- `postgres:5432` → Base de datos
- `backend:8001` → API
- `frontend:80` → React App

## 🔄 Flujo de Peticiones

### Petición a Frontend (/)
```
Internet → Nginx:80 → Frontend:80 → React App
```

### Petición a API (/api/*)
```
Internet → Nginx:80 → Backend:8001 → PostgreSQL:5432
```

### Petición con SSL (/api/*)
```
Internet → Nginx:443 (SSL) → Backend:8001 → PostgreSQL:5432
```

## 💾 Volúmenes Persistentes

### postgres_data
- **Tipo**: Named volume
- **Ubicación**: `/var/lib/docker/volumes/`
- **Contenido**: Datos de PostgreSQL
- **Backup**: Ver `scripts/backup.sh`

### Bind Mounts (Desarrollo)
```yaml
backend:
  volumes:
    - ./backend:/app  # Hot reload en desarrollo
```

## 🚀 Comandos de Gestión

### Iniciar servicios
```bash
docker compose up -d
```

### Ver logs en tiempo real
```bash
docker compose logs -f [service]
```

### Reiniciar un servicio
```bash
docker compose restart [service]
```

### Acceder a un contenedor
```bash
docker compose exec [service] sh
```

### Ver recursos utilizados
```bash
docker stats
```

## 🔧 Configuración de Producción

### Variables de entorno por servicio

#### `.env` (raíz - Docker Compose)
```bash
POSTGRES_USER=guarani_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=guarani_appstore
REACT_APP_BACKEND_URL=https://tu-dominio.com
```

#### `backend/.env` (Backend)
- Todas las API keys
- Configuración de servicios externos
- Ver: `backend/.env.example`

#### `frontend/.env` (Frontend Build)
- `REACT_APP_BACKEND_URL`
- Variables de entorno de build

## 🔒 Seguridad

### Network Isolation
- Frontend no tiene acceso directo a PostgreSQL
- Solo Backend puede comunicarse con la DB
- Nginx expone solo puertos necesarios

### Secrets Management
- No se incluyen `.env` en imagen
- Variables inyectadas en runtime
- Archivos sensibles en `.dockerignore`

### Health Checks
```yaml
postgres:
  healthcheck:
    test: pg_isready -U $POSTGRES_USER
    interval: 10s
    
backend:
  healthcheck:
    test: curl -f http://localhost:8001/health
    interval: 30s
```

## 📈 Escalabilidad

### Escalar servicios
```bash
# Múltiples instancias de backend
docker compose up -d --scale backend=3
```

### Load Balancing
Nginx puede configurarse para balancear entre múltiples backends:
```nginx
upstream backend {
    server backend_1:8001;
    server backend_2:8001;
    server backend_3:8001;
}
```

## 🛠️ Troubleshooting

### Container no inicia
```bash
docker compose logs [service]
docker compose ps
```

### Problema de conexión entre servicios
```bash
# Verificar red
docker network inspect guarani_guarani_network

# Ping entre servicios
docker compose exec backend ping postgres
```

### Reinicio limpio
```bash
docker compose down -v  # ⚠️ Elimina volúmenes
docker compose build --no-cache
docker compose up -d
```

## 📚 Referencias

- [Documentación Docker Compose](https://docs.docker.com/compose/)
- [Nginx Docker](https://hub.docker.com/_/nginx)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

---

Para deployment completo ver: [DEPLOYMENT.md](./DEPLOYMENT.md)
