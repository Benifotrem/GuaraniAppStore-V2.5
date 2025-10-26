# 🚀 GuaraniAppStore V2.5 Pro

**Full-Stack Application con Agente Developer RAG Integrado**

Una plataforma completa de servicios de IA con sistema de soporte inteligente integrado.

---

## 🎯 Stack Completo

**App Principal:** React + FastAPI + MongoDB  
**Agente RAG:** FastAPI + PostgreSQL + OpenRouter  
**Infraestructura:** Docker Compose + Nginx + Cloudflare  

---

## ⚡ Quick Start

```bash
# 1. Clonar
git clone https://github.com/tu-usuario/GuaraniAppStore-V2.5.git
cd GuaraniAppStore-V2.5

# 2. Configurar variables
./generate_env.sh

# 3. Deployment
docker-compose up -d

# 4. Migración (una vez)
docker-compose --profile migration up --build --exit-code-from migration_tool
```

---

## 📦 Servicios (8 contenedores)

1. **MongoDB** - Base de datos principal
2. **Backend** - API FastAPI (puerto 8001)
3. **Frontend** - React App (puerto 3000)
4. **PostgreSQL** - Base de conocimiento RAG
5. **Agente Backend** - Soporte inteligente (puerto 8002)
6. **Model Watcher** - Monitoreo de modelos
7. **Migration Tool** - Migración de datos
8. **Nginx** - Reverse proxy

---

## 🌐 URLs

- **App:** https://tudominio.com
- **API:** https://tudominio.com/api
- **Agente:** https://agente.tudominio.com/api

---

## 📚 Documentación Completa

- **[VARIABLES_COMPLETAS.md](VARIABLES_COMPLETAS.md)** ⭐ Lista de TODAS las variables
- **[CHECKLIST_REPOSITORIO.md](CHECKLIST_REPOSITORIO.md)** ⭐ Verificar el repo
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía de deployment
- **[INSTALACION_AGENTE.md](INSTALACION_AGENTE.md)** - Instalación agente
- **[GITHUB_SECRETS.md](GITHUB_SECRETS.md)** - GitHub Secrets
- **[CLAVES_REALES_QUICKSTART.md](CLAVES_REALES_QUICKSTART.md)** - Quick start

---

## 🔑 Variables Obligatorias

```bash
REACT_APP_BACKEND_URL=https://tudominio.com
OPENROUTER_API_KEY=sk-or-v1-xxx
JWT_SECRET=[generar]
SECRET_KEY=[generar]
POSTGRES_PASSWORD=[generar]
```

**Generar secrets:**
```bash
openssl rand -hex 32  # JWT_SECRET
openssl rand -hex 32  # SECRET_KEY
openssl rand -base64 24  # POSTGRES_PASSWORD
```

---

## ✅ Checklist Pre-Deployment

- [ ] Todas las variables configuradas
- [ ] .env NO está en Git
- [ ] docker-compose config sin errores
- [ ] Cloudflare DNS configurado
- [ ] Firewall permite puertos 80, 443

---

## 🆘 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Backup MongoDB
docker exec guarani_mongodb mongodump --out /data/db/backup

# Backup PostgreSQL
docker exec soporte_postgres_rag pg_dump -U soporte_user_seguro soporte_db_rag > backup.sql
```

---

**Versión:** 2.5 Pro con Agente Developer  
**Stack:** 8 servicios Docker | MongoDB + PostgreSQL | React + FastAPI  
**Docs:** Ver archivos VARIABLES_COMPLETAS.md y CHECKLIST_REPOSITORIO.md
