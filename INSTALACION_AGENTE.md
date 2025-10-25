# 🚀 Guía de Instalación - Stack Unificado con Agente Developer

## 📋 Descripción del Stack

Este stack incluye:
- **Aplicación Principal**: GuaraniAppStore (MongoDB, FastAPI, React)
- **Agente Developer**: Sistema de soporte inteligente con RAG
- **PostgreSQL**: Base de datos para RAG del agente
- **OpenRouter Integration**: Routing inteligente de modelos (Claude Sonnet 4.5 / GPT-4o-mini)
- **Migration Tool**: Migración de datos MongoDB → PostgreSQL
- **Model Watcher**: Monitoreo de disponibilidad de modelos

---

## 📁 Estructura de Archivos Creada

```
GuaraniAppStore-V2.5/
├── docker-compose.yml          # Stack unificado completo
├── .env                        # Variables de entorno
│
├── soporte_agent/              # Agente Developer
│   ├── Dockerfile
│   ├── main.py                 # Backend FastAPI
│   └── requirements.txt
│
├── migration_scripts/          # Herramienta de migración
│   ├── Dockerfile
│   └── migrate.py              # Script Python
│
├── watcher_script/             # Vigilancia de modelos
│   ├── Dockerfile
│   └── check_models.py
│
├── nginx/
│   └── nginx.conf              # Actualizado con soporte para subdominio agente
│
└── (archivos existentes backend/frontend/)
```

---

## 🔧 Paso A: Preparación de Variables de Entorno

### 1. Copiar el template

```bash
cp .env.example .env
cp .env.example backend/.env
```

### 2. Editar .env en la raíz

```bash
nano .env
```

**Variables CRÍTICAS del Agente Developer:**

```bash
# ==================================
# AGENTE DEVELOPER - CONFIGURACIÓN
# ==================================

# OpenRouter API (OBLIGATORIO)
OPENROUTER_API_KEY="sk-or-v1-XXXXXXXXXXXXXXXXXXXXXXXX"
OPENROUTER_MODEL_ID_HIGH="anthropic/claude-sonnet-4.5"
OPENROUTER_MODEL_ID_LOW="openai/gpt-4o-mini"
OPENROUTER_EMBEDDING_MODEL="text-embedding-ada-002"

# Anthropic Fallback (OPCIONAL)
ANTHROPIC_API_KEY_FALLBACK="sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXX"

# PostgreSQL RAG (CAMBIAR CONTRASEÑA)
POSTGRES_USER="soporte_user_seguro"
POSTGRES_PASSWORD="Genera_Una_Contraseña_Segura_Aqui_Min16Chars"
POSTGRES_DB="soporte_db_rag"

# Watcher
WATCHER_CHECK_INTERVAL="3600"

# ==================================
# APP PRINCIPAL
# ==================================

# URL del Backend
REACT_APP_BACKEND_URL="https://tudominio.com"
```

### 3. Generar contraseña segura para PostgreSQL

```bash
openssl rand -base64 24
# Copiar el resultado como POSTGRES_PASSWORD
```

---

## 🚀 Paso B: Instalación Inicial (Sin Migración)

### 1. Construir e iniciar servicios

```bash
# Construir todas las imágenes
docker-compose build

# Iniciar servicios (sin migración)
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 2. Verificar que todos los servicios están corriendo

```bash
docker-compose ps
```

**Deberías ver:**
- `guarani_mongodb` - Running
- `guarani_backend` - Running
- `guarani_frontend` - Running
- `soporte_postgres_rag` - Running
- `soporte_backend` - Running
- `model_watcher` - Running
- `guarani_nginx` - Running

### 3. Verificar salud de servicios

```bash
# Backend principal
curl http://localhost:8001/health

# Agente Developer
curl http://localhost:8002/health

# PostgreSQL
docker exec soporte_postgres_rag pg_isready -U soporte_user_seguro
```

---

## 📊 Paso C: Ejecución de la Migración (UNA SOLA VEZ)

⚠️ **IMPORTANTE**: La migración solo se ejecuta UNA VEZ cuando los servicios estén estables.

### 1. Ejecutar migración con profile

```bash
docker-compose --profile migration up --build --exit-code-from migration_tool
```

### 2. Verificar migración exitosa

Deberías ver en los logs:
```
✅ Conectado a MongoDB: guarani_appstore
✅ Conectado a PostgreSQL
✅ Tablas PostgreSQL creadas/verificadas
✅ Migrados X servicios
✅ Estadísticas de usuarios migradas
✅ ¡Migración completada exitosamente!
```

### 3. Verificar datos en PostgreSQL

```bash
# Conectar a PostgreSQL
docker exec -it soporte_postgres_rag psql -U soporte_user_seguro -d soporte_db_rag

# Ver tablas
\dt

# Ver datos migrados
SELECT COUNT(*) FROM knowledge_base;
SELECT * FROM knowledge_base LIMIT 5;

# Salir
\q
```

---

## 🌐 Paso D: Configuración de Cloudflare (DNS)

### 1. DNS Records en Cloudflare

**Dominio Principal:**
```
Type: A
Name: @
Content: [IP-VPS]
Proxy: ✅ Proxied (Naranja)
```

**Subdominio del Agente:**
```
Type: A
Name: agente
Content: [IP-VPS]
Proxy: ✅ Proxied (Naranja)
```

O puedes usar:
```
Type: A
Name: soporte
Content: [IP-VPS]
Proxy: ✅ Proxied (Naranja)
```

### 2. SSL/TLS Settings

- Modo: **Full**
- Always Use HTTPS: ✅ Enabled
- Automatic HTTPS Rewrites: ✅ Enabled

---

## ✅ Paso E: Verificación Final

### 1. Verificar App Principal

```bash
# Desde internet
curl https://tudominio.com/api/health
curl https://tudominio.com
```

### 2. Verificar Agente Developer

```bash
# Desde internet
curl https://agente.tudominio.com/health
curl https://agente.tudominio.com/api/stats
```

### 3. Probar query al agente

```bash
curl -X POST https://agente.tudominio.com/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué servicios ofrece GuaraniAppStore?", "use_high_model": false}'
```

### 4. Ver logs del Model Watcher

```bash
docker-compose logs -f model_watcher
```

Deberías ver verificaciones periódicas de modelos:
```
🔍 Iniciando verificación de modelos...
✅ anthropic/claude-sonnet-4.5: Disponible
✅ openai/gpt-4o-mini: Disponible
```

---

## 🔄 Comandos de Mantenimiento

### Ver logs de todos los servicios

```bash
docker-compose logs -f
```

### Ver logs específicos

```bash
# Agente Developer
docker-compose logs -f soporte_backend

# Model Watcher
docker-compose logs -f model_watcher

# PostgreSQL
docker-compose logs -f postgres_rag
```

### Reiniciar servicios

```bash
# Todos
docker-compose restart

# Solo agente
docker-compose restart soporte_backend

# Solo watcher
docker-compose restart model_watcher
```

### Backup de PostgreSQL (RAG)

```bash
# Crear backup
docker exec soporte_postgres_rag pg_dump -U soporte_user_seguro soporte_db_rag > rag_backup_$(date +%Y%m%d).sql

# Restaurar backup
cat rag_backup_20250124.sql | docker exec -i soporte_postgres_rag psql -U soporte_user_seguro -d soporte_db_rag
```

---

## 🆘 Troubleshooting

### Agente Developer no inicia

```bash
# Ver logs detallados
docker-compose logs soporte_backend

# Verificar variables de entorno
docker exec soporte_backend env | grep OPENROUTER

# Verificar conexión a PostgreSQL
docker exec soporte_backend psql postgresql://soporte_user_seguro:PASSWORD@postgres_rag:5432/soporte_db_rag -c "SELECT 1"
```

### Migración falla

```bash
# Ver logs de migración
docker-compose --profile migration logs migration_tool

# Re-ejecutar migración
docker-compose --profile migration up --build --force-recreate migration_tool
```

### Model Watcher reporta errores

```bash
# Ver logs
docker-compose logs model_watcher

# Verificar API key de OpenRouter
echo $OPENROUTER_API_KEY

# Reiniciar watcher
docker-compose restart model_watcher
```

### PostgreSQL no acepta conexiones

```bash
# Verificar estado
docker-compose ps postgres_rag

# Ver logs
docker-compose logs postgres_rag

# Reiniciar
docker-compose restart postgres_rag
```

---

## 📊 URLs de Acceso

Después de la instalación completa:

**App Principal:**
- Frontend: https://tudominio.com
- Backend API: https://tudominio.com/api
- Health: https://tudominio.com/api/health

**Agente Developer:**
- Backend API: https://agente.tudominio.com/api
- Health: https://agente.tudominio.com/health
- Stats: https://agente.tudominio.com/api/stats

---

## 🔒 Checklist de Seguridad

- [ ] `OPENROUTER_API_KEY` configurado
- [ ] `POSTGRES_PASSWORD` cambiado (mínimo 16 caracteres)
- [ ] Cloudflare SSL en modo "Full"
- [ ] DNS Records configurados (@ y agente)
- [ ] Firewall permite puertos 80, 443
- [ ] Backup automático de PostgreSQL configurado
- [ ] Variables sensibles no committed a Git

---

## 🎉 ¡Instalación Completada!

Tu stack unificado está listo con:
- ✅ Aplicación principal operativa
- ✅ Agente Developer con RAG funcionando
- ✅ Routing inteligente de modelos configurado
- ✅ Model Watcher monitoreando
- ✅ Datos migrados a PostgreSQL
- ✅ Subdominio para agente configurado

**Próximos pasos:**
1. Agregar más contenido a la base de conocimiento del agente
2. Crear frontend específico para el agente (opcional)
3. Configurar alertas de monitoring
4. Implementar autenticación para el agente (si es necesario)
