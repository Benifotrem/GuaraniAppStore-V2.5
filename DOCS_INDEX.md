# 📚 Índice de Documentación - GuaraniAppStore V2.5 Pro

## 🎯 Por Rol

### 👨‍💻 Desarrolladores
1. **[QUICKSTART.md](./QUICKSTART.md)** - Inicio rápido para empezar a desarrollar
2. **[README.md](./README.md)** - Overview general del proyecto
3. **[DOCKER_ARCHITECTURE.md](./DOCKER_ARCHITECTURE.md)** - Arquitectura de containers
4. **Backend**:
   - `backend/.env.example` - Variables de entorno
   - `backend/server.py` - API FastAPI
   - `backend/models.py` - Modelos de base de datos
5. **Frontend**:
   - `frontend/.env.example` - Variables de entorno
   - `frontend/src/` - Código React

### 🚀 DevOps / SysAdmins
1. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guía completa de deployment en VPS
2. **[DOCKER_ARCHITECTURE.md](./DOCKER_ARCHITECTURE.md)** - Arquitectura de servicios
3. **[MAINTENANCE.md](./MAINTENANCE.md)** - Tareas de mantenimiento
4. **Scripts**:
   - `scripts/deploy.sh` - Deploy automatizado
   - `scripts/backup.sh` - Backup de base de datos
   - `scripts/restore.sh` - Restore de base de datos
   - `scripts/docker-cleanup.sh` - Limpieza de Docker

### 🔒 Seguridad
1. **[SECURITY.md](./SECURITY.md)** - Configuración de seguridad y API keys
2. **Scripts**:
   - `scripts/check_security.sh` - Verificación de seguridad
   - `scripts/pre-deploy-check.sh` - Verificación pre-deployment

---

## 📖 Por Tarea

### Primera vez con el proyecto
```
1. QUICKSTART.md → Inicio rápido
2. README.md → Entender el proyecto
3. SECURITY.md → Configurar credenciales
```

### Desarrollo local
```
1. QUICKSTART.md → Configuración inicial
2. docker-compose.dev.yml → Hot reload
3. DOCKER_ARCHITECTURE.md → Entender servicios
```

### Deployment en VPS
```
1. SECURITY.md → Configurar .env files
2. scripts/pre-deploy-check.sh → Verificar pre-requisitos
3. DEPLOYMENT.md → Seguir guía paso a paso
4. scripts/deploy.sh → Deploy automatizado
```

### Configurar SSL
```
1. DEPLOYMENT.md → Sección "Configuración SSL"
2. nginx/conf.d/guarani.conf → Descomentar líneas SSL
```

### Hacer backup
```
1. scripts/backup.sh → Ejecutar backup
2. MAINTENANCE.md → Ver estrategias de backup
```

### Troubleshooting
```
1. DEPLOYMENT.md → Sección "Troubleshooting"
2. MAINTENANCE.md → Sección "Debugging Avanzado"
3. docker compose logs -f → Ver logs en tiempo real
```

### Actualizar aplicación
```
1. scripts/backup.sh → Backup primero
2. git pull → Obtener cambios
3. MAINTENANCE.md → Sección "Actualizar Aplicación"
4. scripts/deploy.sh → Rebuild y restart
```

---

## 🗂️ Estructura Completa de Archivos

### Documentación Principal
```
📄 README.md                    # Overview general
📄 QUICKSTART.md                # Inicio rápido
📄 SECURITY.md                  # Configuración de seguridad
📄 DEPLOYMENT.md                # Guía de deployment
📄 DOCKER_ARCHITECTURE.md       # Arquitectura Docker
📄 MAINTENANCE.md               # Guía de mantenimiento
📄 DOCS_INDEX.md                # Este archivo
```

### Configuración Docker
```
🐳 docker-compose.yml           # Producción
🐳 docker-compose.dev.yml       # Desarrollo con hot reload
📄 .dockerignore                # Archivos ignorados por Docker
📄 .env.docker                  # Ejemplo de variables Docker
```

### Backend
```
📂 backend/
  🐳 Dockerfile                 # Container backend
  📄 .env.example               # Ejemplo de variables
  🐍 server.py                  # API FastAPI
  🐍 models.py                  # Modelos SQLAlchemy
  🐍 schemas.py                 # Schemas Pydantic
  🐍 auth.py                    # Autenticación
  🐍 payment_service.py         # Integración pagos
  📄 requirements.txt           # Dependencias Python
```

### Frontend
```
📂 frontend/
  🐳 Dockerfile                 # Container producción
  🐳 Dockerfile.dev             # Container desarrollo
  📄 nginx.conf                 # Config nginx para React
  📄 .env.example               # Ejemplo de variables
  📂 src/
    📂 pages/                   # Páginas React
    📂 components/              # Componentes React
  📄 package.json               # Dependencias Node
```

### Nginx
```
📂 nginx/
  📄 nginx.conf                 # Configuración principal
  📂 conf.d/
    📄 guarani.conf             # Configuración del sitio
  📂 ssl/                       # Certificados SSL
  📂 logs/                      # Logs de acceso/error
```

### Scripts
```
📂 scripts/
  📜 deploy.sh                  # Deploy automatizado
  📜 backup.sh                  # Backup de BD
  📜 restore.sh                 # Restore de BD
  📜 check_security.sh          # Verificación de seguridad
  📜 pre-deploy-check.sh        # Verificación pre-deployment
  📜 docker-cleanup.sh          # Limpieza Docker
```

---

## 🔗 Enlaces Rápidos

### Comandos Más Usados
```bash
# Desarrollo local
docker compose -f docker-compose.dev.yml up -d

# Deployment
./scripts/deploy.sh

# Ver logs
docker compose logs -f

# Backup
./scripts/backup.sh

# Verificar seguridad
./scripts/check_security.sh
```

### URLs Importantes (Desarrollo Local)
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- PostgreSQL: localhost:5432

---

## 📝 Flujo de Trabajo Típico

### 1️⃣ Setup Inicial
```bash
git clone <repo>
cd guarani-appstore
cp .env.docker .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Editar archivos .env
```

### 2️⃣ Desarrollo
```bash
docker compose -f docker-compose.dev.yml up -d
# Hacer cambios en código (hot reload automático)
docker compose logs -f backend
```

### 3️⃣ Testing
```bash
# Verificar funcionalidad
curl http://localhost:8001/health
# Abrir http://localhost:3000 en navegador
```

### 4️⃣ Deployment
```bash
./scripts/pre-deploy-check.sh
./scripts/backup.sh  # Si ya hay datos
./scripts/deploy.sh
```

### 5️⃣ Mantenimiento
```bash
# Diario: Ver logs
docker compose logs --tail=100 backend

# Semanal: Backup
./scripts/backup.sh

# Mensual: Actualizar y limpiar
git pull
./scripts/deploy.sh
./scripts/docker-cleanup.sh
```

---

## ❓ FAQs Rápidas

**Q: ¿Dónde configuro las API keys?**
A: En `backend/.env` - Ver [SECURITY.md](./SECURITY.md)

**Q: ¿Cómo hago deployment en VPS?**
A: Sigue [DEPLOYMENT.md](./DEPLOYMENT.md) paso a paso

**Q: ¿Cómo activo hot reload para desarrollo?**
A: Usa `docker compose -f docker-compose.dev.yml up -d`

**Q: ¿Cómo hago backup de la base de datos?**
A: Ejecuta `./scripts/backup.sh`

**Q: ¿Dónde veo los logs?**
A: `docker compose logs -f [servicio]`

**Q: ¿Cómo configuro SSL?**
A: Ver sección SSL en [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 📞 Ayuda y Soporte

- **Documentación**: Empieza con [QUICKSTART.md](./QUICKSTART.md)
- **Problemas**: Ver secciones de Troubleshooting
- **Email**: admin@guaraniappstore.com
- **Issues**: GitHub Issues

---

**💡 Tip**: Guarda este archivo como referencia rápida!
