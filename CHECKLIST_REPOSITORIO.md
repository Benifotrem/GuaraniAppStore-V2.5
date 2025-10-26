# ✅ Checklist de Estructura del Repositorio GitHub

## 📋 Verificación Pre-Deployment

Este documento te ayuda a verificar que el repositorio está completo antes de deployar.

---

## 🗂️ Estructura del Repositorio

### Raíz del Proyecto
```
GuaraniAppStore-V2.5/
├── .github/
│   └── workflows/
│       └── deploy.yml                 ✅ Workflow de CI/CD
│
├── backend/                            ✅ Backend FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── server.py
│   ├── database.py
│   ├── database_mongo.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── ai_service.py
│   ├── blog_generator_service.py
│   ├── momentum_*.py
│   ├── cryptoshield_*.py
│   ├── pulse_*.py
│   └── (otros archivos backend)
│
├── frontend/                           ✅ Frontend React
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── yarn.lock
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── pages/
│       ├── components/
│       ├── context/
│       │   └── AuthContext.js
│       └── (otros archivos frontend)
│
├── soporte_agent/                      ✅ Agente Developer RAG
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── migration_scripts/                  ✅ Scripts de Migración
│   ├── Dockerfile
│   └── migrate.py
│
├── watcher_script/                     ✅ Model Watcher
│   ├── Dockerfile
│   └── check_models.py
│
├── nginx/                              ✅ Configuración Nginx
│   ├── nginx.conf
│   └── ssl/                            (opcional, para certificados)
│
├── docker-compose.yml                  ✅ Orquestación completa
├── .env.example                        ✅ Template de variables
├── .gitignore                          ✅ Protección de secrets
├── .dockerignore                       ✅ Optimización builds
│
├── generate_env.sh                     ✅ Script generador
├── deploy.sh                           ✅ Script de deployment
│
└── Documentación/
    ├── README.md
    ├── DEPLOYMENT.md                   ✅ Guía de deployment
    ├── INSTALACION_AGENTE.md           ✅ Instalación del agente
    ├── GITHUB_SECRETS.md               ✅ Configuración secrets
    ├── CLAVES_REALES_QUICKSTART.md     ✅ Quick start
    ├── VARIABLES_COMPLETAS.md          ✅ Lista de variables
    ├── SECURITY.md                     ✅ Seguridad
    ├── COMANDOS_DEPLOYMENT.md          ✅ Comandos útiles
    └── AGREGAR_CONTENEDORES.md         ✅ Guía contenedores
```

---

## ✅ Checklist de Verificación

### 1. Backend (FastAPI)

**Archivos críticos:**
- [ ] `backend/Dockerfile` existe
- [ ] `backend/requirements.txt` existe y tiene todas las dependencias
- [ ] `backend/server.py` existe (punto de entrada)
- [ ] `backend/database_mongo.py` existe (conexión MongoDB)
- [ ] `backend/auth.py` existe (autenticación)

**Servicios implementados:**
- [ ] Pulse IA (pulse_*.py)
- [ ] Momentum Predictor (momentum_*.py)
- [ ] CryptoShield (cryptoshield_*.py)
- [ ] Blog Generator (blog_*.py)
- [ ] User Authentication (/auth/login, /auth/register)
- [ ] Admin endpoints (/admin/*)

**Dependencias principales en requirements.txt:**
```
fastapi
uvicorn
motor (MongoDB async)
pymongo
pydantic
python-jose (JWT)
passlib (hashing)
tensorflow (para modelos ML)
ccxt (para crypto)
httpx (HTTP client)
```

### 2. Frontend (React)

**Archivos críticos:**
- [ ] `frontend/Dockerfile` existe
- [ ] `frontend/nginx.conf` existe
- [ ] `frontend/package.json` existe
- [ ] `frontend/src/App.js` existe
- [ ] `frontend/src/context/AuthContext.js` existe

**Páginas principales:**
- [ ] LandingPage.js
- [ ] Dashboard.js
- [ ] ClientDashboard.js
- [ ] AdminDashboard.js
- [ ] SuiteCryptoDashboard.js
- [ ] Blog.js

**Dependencias principales en package.json:**
```json
{
  "dependencies": {
    "react": "^18.x",
    "react-dom": "^18.x",
    "react-router-dom": "^6.x",
    "axios": "^1.x",
    "recharts": "^2.x",
    "antd": "^5.x"
  }
}
```

### 3. Agente Developer

**Archivos del agente:**
- [ ] `soporte_agent/Dockerfile` existe
- [ ] `soporte_agent/main.py` existe
- [ ] `soporte_agent/requirements.txt` existe

**Endpoints implementados:**
- [ ] GET /health (health check)
- [ ] POST /api/query (consultar agente)
- [ ] POST /api/knowledge/add (agregar conocimiento)
- [ ] GET /api/stats (estadísticas)

**Dependencias principales:**
```
fastapi
uvicorn
sqlalchemy
asyncpg (PostgreSQL async)
psycopg2-binary
httpx
openai (para OpenRouter)
```

### 4. Migration Scripts

**Archivos de migración:**
- [ ] `migration_scripts/Dockerfile` existe
- [ ] `migration_scripts/migrate.py` existe

**Funcionalidades:**
- [ ] Conecta a MongoDB
- [ ] Conecta a PostgreSQL
- [ ] Migra servicios
- [ ] Migra estadísticas de usuarios

### 5. Model Watcher

**Archivos del watcher:**
- [ ] `watcher_script/Dockerfile` existe
- [ ] `watcher_script/check_models.py` existe

**Funcionalidades:**
- [ ] Verifica modelos de OpenRouter
- [ ] Log de disponibilidad
- [ ] Intervalo configurable

### 6. Configuración Docker

**docker-compose.yml debe tener:**
- [ ] Servicio `mongodb`
- [ ] Servicio `backend`
- [ ] Servicio `frontend`
- [ ] Servicio `postgres_rag`
- [ ] Servicio `soporte_backend`
- [ ] Servicio `model_watcher`
- [ ] Servicio `migration_tool` (profile)
- [ ] Servicio `nginx`

**Volúmenes definidos:**
- [ ] `mongodb_data`
- [ ] `postgres_rag_data`
- [ ] `backend_logs`
- [ ] `soporte_logs`
- [ ] `nginx_logs`

**Red definida:**
- [ ] `guarani_network`

### 7. Nginx Configuration

**nginx/nginx.conf debe tener:**
- [ ] Upstream `backend` (puerto 8001)
- [ ] Upstream `frontend` (puerto 80)
- [ ] Upstream `soporte_backend` (puerto 8002)
- [ ] Server block para dominio principal
- [ ] Server block para subdominio agente (agente.* o soporte.*)
- [ ] Configuración de Cloudflare IPs
- [ ] Rate limiting
- [ ] Security headers

### 8. Archivos de Configuración

**Archivos esenciales:**
- [ ] `.gitignore` incluye `.env` y `backend/.env`
- [ ] `.dockerignore` optimiza builds
- [ ] `.env.example` tiene todas las variables
- [ ] `generate_env.sh` es ejecutable
- [ ] `deploy.sh` es ejecutable

### 9. GitHub Actions

**Workflow de CI/CD:**
- [ ] `.github/workflows/deploy.yml` existe
- [ ] Workflow tiene todos los secrets necesarios
- [ ] Workflow ejecuta build y deployment
- [ ] Workflow verifica health checks

### 10. Documentación

**Archivos de documentación:**
- [ ] `README.md` con descripción general
- [ ] `DEPLOYMENT.md` con guía completa
- [ ] `INSTALACION_AGENTE.md` con instalación del agente
- [ ] `GITHUB_SECRETS.md` con configuración de secrets
- [ ] `VARIABLES_COMPLETAS.md` con todas las variables
- [ ] `SECURITY.md` con seguridad
- [ ] `CLAVES_REALES_QUICKSTART.md` con quick start

---

## 🔍 Comandos de Verificación

### Verificar estructura localmente

```bash
# Ver estructura del repositorio
tree -L 2 -I 'node_modules|venv|__pycache__'

# Verificar que .gitignore funciona
git status

# Verificar Dockerfiles
find . -name "Dockerfile" -type f

# Verificar requirements
cat backend/requirements.txt
cat soporte_agent/requirements.txt

# Verificar docker-compose
docker-compose config
```

### Verificar en GitHub

```bash
# Clonar en temporal
git clone https://github.com/tu-usuario/GuaraniAppStore-V2.5.git /tmp/test-repo
cd /tmp/test-repo

# Verificar estructura
ls -la
ls -la backend/
ls -la frontend/
ls -la soporte_agent/

# Verificar que .env NO está
ls -la .env
ls -la backend/.env
# Debería dar "No such file or directory"

# Limpiar
cd /
rm -rf /tmp/test-repo
```

---

## ⚠️ Problemas Comunes

### 1. Archivo .env en Git

**Problema:** El archivo .env con claves reales está en GitHub

**Solución:**
```bash
git rm --cached .env
git rm --cached backend/.env
echo ".env" >> .gitignore
echo "backend/.env" >> .gitignore
git commit -m "Remove .env files"
git push
```

**Luego:** Rotar TODAS las claves expuestas

### 2. Dependencias faltantes

**Problema:** requirements.txt o package.json incompletos

**Solución:**
```bash
# Python
cd backend
pip freeze > requirements.txt

# Node
cd frontend
yarn install
# package.json se actualiza automáticamente
```

### 3. Dockerfiles incorrectos

**Problema:** Dockerfiles no construyen

**Solución:**
```bash
# Probar build localmente
docker build -t test-backend ./backend
docker build -t test-frontend ./frontend
docker build -t test-agent ./soporte_agent
```

### 4. docker-compose.yml con errores

**Problema:** Sintaxis incorrecta

**Solución:**
```bash
# Validar sintaxis
docker-compose config

# Si hay errores, corregir y re-validar
```

---

## ✅ Checklist Final Pre-Push

Antes de hacer `git push`:

- [ ] Ejecuté `git status` y NO veo `.env` o `backend/.env`
- [ ] Verifiqué `.gitignore` incluye archivos sensibles
- [ ] Probé `docker-compose config` sin errores
- [ ] Todos los Dockerfiles construyen correctamente
- [ ] La documentación está actualizada
- [ ] Los scripts tienen permisos de ejecución
- [ ] No hay secrets hardcodeados en el código

---

## 📝 Comando de Verificación Rápida

```bash
#!/bin/bash
# quick-check.sh

echo "🔍 Verificando estructura del repositorio..."

# Archivos críticos
files=(
  "docker-compose.yml"
  "backend/Dockerfile"
  "backend/server.py"
  "frontend/Dockerfile"
  "frontend/src/App.js"
  "soporte_agent/Dockerfile"
  "soporte_agent/main.py"
  "nginx/nginx.conf"
  ".env.example"
  ".gitignore"
)

for file in "${files[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file"
  else
    echo "❌ $file FALTANTE"
  fi
done

# Verificar .env NO está en Git
if git ls-files | grep -q "\.env$"; then
  echo "⚠️  ADVERTENCIA: .env está en Git!"
else
  echo "✅ .env NO está en Git"
fi

echo ""
echo "✅ Verificación completada"
```

---

**🎯 Si todos los checks pasan, el repositorio está listo para deployment!**
