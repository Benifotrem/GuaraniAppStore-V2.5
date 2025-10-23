# GuaraniAppStore V2.5 Pro

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](./DOCKER_ARCHITECTURE.md)
[![Deployment](https://img.shields.io/badge/Deployment-VPS-green)](./DEPLOYMENT.md)
[![Security](https://img.shields.io/badge/Security-Configured-orange)](./SECURITY.md)

## 🚀 Descripción

GuaraniAppStore V2.5 Pro es una plataforma modular de servicios empresariales que integra IA, automatización, criptomonedas y servicios especializados para empresas en Paraguay y América Latina.

## ⚡ Inicio Rápido

¿Primera vez? Ver **[QUICKSTART.md](./QUICKSTART.md)** para empezar en minutos.

📚 **[Ver índice completo de documentación](./DOCS_INDEX.md)** - Navegación por rol y tarea

## 📋 Características Principales

- **11 Servicios Empresariales**: Desde prospección con IA hasta automatización de e-commerce
- **Suite Crypto**: 5 bots de Telegram para análisis y trading de criptomonedas
- **Panel de Administración**: Gestión completa de usuarios, pagos y servicios
- **Dashboard de Usuario**: Panel personalizado con timezone específico
- **Múltiples Métodos de Pago**: Pagopar, Stripe, BTC, ETH, USDT (ERC-20)
- **Autenticación Avanzada**: JWT, 2FA, Google OAuth
- **Blog con IA**: Sistema de generación automática de contenido

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI (Python), PostgreSQL, SQLAlchemy, Alembic
- **Frontend**: React, Tailwind CSS
- **IA**: Claude 3.5 Sonnet, OpenAI, OpenRouter
- **Blockchain**: Etherscan, BSCScan
- **Pagos**: Pagopar, Stripe

## 📦 Instalación

### Opción A: Docker Compose (Recomendado para VPS)

**Requisitos**: Docker 20.10+ y Docker Compose 2.0+

```bash
# 1. Configurar variables de entorno
cp .env.docker .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Editar archivos .env con tus credenciales

# 3. Deploy
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Ver **[DEPLOYMENT.md](./DEPLOYMENT.md)** para guía completa de deployment en VPS.

### Opción B: Desarrollo Local

**Requisitos**: Python 3.9+, Node.js 16+, PostgreSQL 13+, Yarn

#### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configura las variables en .env
alembic upgrade head
python server.py
```

#### Frontend
```bash
cd frontend
yarn install
cp .env.example .env
# Configura REACT_APP_BACKEND_URL en .env
yarn start
```

## 🔐 Configuración de Seguridad

**IMPORTANTE**: Antes de ejecutar la aplicación, configura correctamente las variables de entorno.

Ver **[SECURITY.md](./SECURITY.md)** para instrucciones detalladas sobre:
- Configuración de claves API
- Variables de entorno requeridas
- Mejores prácticas de seguridad
- Obtención de credenciales

## 📚 Estructura del Proyecto

```
/app/
├── backend/              # API FastAPI
│   ├── Dockerfile        # Container backend
│   ├── server.py         # Punto de entrada
│   ├── models.py         # Modelos SQLAlchemy
│   ├── schemas.py        # Schemas Pydantic
│   ├── auth.py           # Autenticación
│   └── ...
├── frontend/             # Aplicación React
│   ├── Dockerfile        # Container frontend
│   ├── nginx.conf        # Config nginx para React
│   └── src/
│       ├── pages/        # Páginas principales
│       └── components/   # Componentes reutilizables
├── nginx/                # Reverse proxy
│   ├── nginx.conf        # Config principal
│   └── conf.d/           # Configuraciones de sitio
├── scripts/              # Scripts de deployment
│   ├── deploy.sh         # Deploy automatizado
│   ├── backup.sh         # Backup de BD
│   └── restore.sh        # Restore de BD
├── docker-compose.yml    # Orquestación de servicios
├── SECURITY.md           # Guía de seguridad
├── DEPLOYMENT.md         # Guía de deployment
└── DOCKER_ARCHITECTURE.md # Arquitectura Docker
```

## 🚦 Uso

### Con Docker Compose
```bash
# Iniciar todos los servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Parar servicios
docker compose down
```

### Desarrollo Local

#### Iniciar Backend
```bash
cd backend
python server.py
# El backend estará en http://localhost:8001
```

#### Iniciar Frontend
```bash
cd frontend
yarn start
# El frontend estará en http://localhost:3000
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
yarn test
```

## 🌐 Variables de Entorno

Ver `.env.example` en cada directorio (backend/frontend) para la lista completa de variables requeridas.

## 📞 Soporte

- Email: admin@guaraniappstore.com
- Website: https://guaraniappstore.com

## 📄 Licencia

Propietario - GuaraniAppStore © 2025

---

**⚠️ IMPORTANTE**: Nunca subas archivos `.env` a repositorios públicos. Mantén tus claves API seguras.
