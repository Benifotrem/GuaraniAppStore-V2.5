# 🔐 Guía Rápida: Claves Reales para VPS

## 🎯 Dos Opciones Disponibles

### Opción A: Manual con SCP (⭐ Recomendado para empezar)
### Opción B: Automático con GitHub Secrets (⭐ Para CI/CD)

---

## ⚡ Opción A: Manual (5 minutos)

### 1. Generar .env localmente

```bash
# Ejecutar script interactivo
./generate_env.sh

# Te pedirá todas las claves y generará:
# - .env (raíz)
# - .env.backend (para backend/)
```

### 2. Transferir al VPS

```bash
# Copiar .env raíz
scp .env usuario@ip-vps:/opt/GuaraniAppStore-V2.5/.env

# Copiar backend/.env
scp backend/.env usuario@ip-vps:/opt/GuaraniAppStore-V2.5/backend/.env
```

### 3. Deploy

```bash
ssh usuario@ip-vps
cd /opt/GuaraniAppStore-V2.5
docker-compose up -d
```

**✅ LISTO!** Tu app está corriendo con claves reales.

---

## ⚡ Opción B: GitHub Secrets (15 minutos)

### 1. Configurar Secrets en GitHub

**Ve a:** Repo → Settings → Secrets and variables → Actions

**Agrega estos secrets:**

```
OPENROUTER_API_KEY       = tu_clave_openrouter
POSTGRES_PASSWORD        = contraseña_segura_16chars
JWT_SECRET              = [ejecuta: openssl rand -hex 32]
SECRET_KEY              = [ejecuta: openssl rand -hex 32]
REACT_APP_BACKEND_URL   = https://tudominio.com
VPS_HOST                = ip.de.tu.vps
VPS_USER                = tu_usuario_ssh
VPS_SSH_KEY             = [tu private key SSH completa]
```

**Más secrets (opcionales):**
- PULSEBOT_TOKEN
- MOMENTUM_BOT_TOKEN
- BREVO_SMTP_USER
- BREVO_SMTP_PASSWORD
- BTC_WALLET
- ETH_WALLET
- etc.

### 2. Push tu código

```bash
git add .
git commit -m "Add deployment workflow"
git push origin main
```

### 3. GitHub Actions hace todo automáticamente

- Genera .env con tus secrets
- Los transfiere al VPS
- Ejecuta docker-compose
- Verifica el deployment

**Ver progreso:** GitHub → Actions → Deploy to VPS

---

## 📋 Claves que Necesitas Obtener

### Obligatorias (Agente Developer):
- [ ] **OpenRouter API Key** → https://openrouter.ai/keys
- [ ] **PostgreSQL Password** → Genera con: `openssl rand -base64 24`

### Obligatorias (App Principal):
- [ ] **JWT Secret** → Genera con: `openssl rand -hex 32`
- [ ] **Secret Key** → Genera con: `openssl rand -hex 32`

### Opcionales (Funcionalidades Extra):
- [ ] Anthropic API Key → https://console.anthropic.com/
- [ ] Telegram Bot Tokens → @BotFather en Telegram
- [ ] Brevo SMTP → https://www.brevo.com/
- [ ] Twitter API → https://developer.twitter.com/
- [ ] Reddit API → https://www.reddit.com/prefs/apps

---

## 🚨 IMPORTANTE: Seguridad

### ✅ HACER:
- ✅ Usar GitHub Secrets o SCP
- ✅ Verificar .env está en .gitignore
- ✅ Permisos 600 en .env (`chmod 600 .env`)
- ✅ Rotar claves cada 3-6 meses

### ❌ NO HACER:
- ❌ NUNCA commitear .env a Git
- ❌ NUNCA compartir claves por email/chat
- ❌ NUNCA usar claves de prueba en producción

---

## 🔧 Scripts Disponibles

### 1. Generador de .env
```bash
./generate_env.sh
```
**Hace:** Te guía paso a paso para crear .env con todas tus claves

### 2. GitHub Actions Workflow
```
.github/workflows/deploy.yml
```
**Hace:** Deployment automático usando GitHub Secrets

---

## 📚 Documentación Completa

- **GITHUB_SECRETS.md** → Guía detallada de GitHub Secrets
- **generate_env.sh** → Script para generar .env localmente
- **.github/workflows/deploy.yml** → Workflow de CI/CD

---

## 🆘 Ayuda Rápida

### ¿Olvidé una clave?

```bash
# Editar manualmente
nano .env
# O re-generar
./generate_env.sh
```

### ¿Cómo actualizar claves en VPS?

```bash
# Opción A: SCP
scp .env usuario@ip-vps:/opt/GuaraniAppStore-V2.5/.env
ssh usuario@ip-vps "cd /opt/GuaraniAppStore-V2.5 && docker-compose restart"

# Opción B: GitHub Actions
# Actualiza el secret en GitHub y haz push
```

### ¿Cómo verificar que funcionan?

```bash
ssh usuario@ip-vps
cd /opt/GuaraniAppStore-V2.5
docker-compose logs -f soporte_backend
# Busca: "✅" o "connected successfully"
```

---

## ✅ Checklist Final

- [ ] Decidí método (SCP Manual o GitHub Secrets)
- [ ] Obtuve todas las API keys necesarias
- [ ] Generé .env con claves reales
- [ ] Transferí .env al VPS (o configuré GitHub Secrets)
- [ ] Verifiqué permisos (chmod 600)
- [ ] .env está en .gitignore
- [ ] Hice deployment y funciona

---

**💡 Recomendación Final:**

1. **Para tu primer deployment:** Usa **Opción A (SCP Manual)**
2. **Una vez funcione:** Migra a **Opción B (GitHub Secrets)** para automatizar

**🎉 ¡Tu proyecto estará corriendo con claves reales en menos de 10 minutos!**
