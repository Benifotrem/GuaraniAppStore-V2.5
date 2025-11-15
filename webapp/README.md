# GuaraniAppStore V2.5 - Laravel Edition

> Plataforma de automatización empresarial con 11 servicios de IA y suscripciones

[![Laravel](https://img.shields.io/badge/Laravel-12-red.svg)](https://laravel.com)
[![PHP](https://img.shields.io/badge/PHP-8.4-blue.svg)](https://php.net)
[![License](https://img.shields.io/badge/License-Proprietary-yellow.svg)]()

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Servicios Disponibles](#-servicios-disponibles)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Deployment en Hostinger](#-deployment-en-hostinger)
- [Telegram Bots](#-telegram-bots)
- [Pasarelas de Pago](#-pasarelas-de-pago)
- [Comandos Útiles](#-comandos-útiles)

## 🚀 Características

- ✅ **11 Servicios** (8 con trial de 7 días, 3 de pago único)
- ✅ **Sistema de Suscripciones** con trial gratuito
- ✅ **4 Pasarelas de Pago**: PayPal, Pagopar, Bancard, Criptomonedas
- ✅ **7 Bots de Telegram** integrados
- ✅ **Panel de Administración** completo
- ✅ **Google OAuth** para autenticación
- ✅ **SEO Optimizado** (Sitemap, Robots.txt, Schema.org)
- ✅ **Diseño Glass Morphism** responsive

## 📦 Servicios Disponibles

### Servicios de Pago Único
1. **Ruptura del Hielo** (₲150,000) - Prospección comercial con IA
2. **Preselección Curricular** (₲200,000) - Análisis de CVs con OCR
3. **Consultoría Técnica** (₲500,000) - Análisis empresarial profundo

### Servicios de Suscripción (Trial 7 días)
4. **Asistente Personal** (₲300,000/mes) - Asistente ejecutivo 24/7
5. **Organizador de Facturas** (₲250,000/mes) - OCR de facturas
6. **Organizador de Agenda** (₲200,000/mes) - Agendamiento automático
7. **Suite Crypto** (₲400,000/mes) - 3 bots para trading

### Servicios Próximamente
8. **Agente de Ventas IA** (₲350,000/mes)
9. **Generador de Blogs** (₲280,000/mes)
10. **Automatización E-commerce** (₲320,000/mes)
11. **Automatización Redes** (₲300,000/mes)

## 💻 Requisitos del Sistema

- **PHP**: 8.2+ (recomendado 8.4)
- **Composer**: 2.6+
- **Node.js**: 18.x+
- **MySQL**: 5.7+ o MariaDB 10.3+
- **Servidor**: Compatible con Hostinger

## 📥 Instalación

### 1. Clonar y Dependencias

```bash
git clone <repo-url>
cd webapp
composer install --optimize-autoloader --no-dev
npm install && npm run build
```

### 2. Configurar Entorno

```bash
cp .env.example .env
php artisan key:generate
```

### 3. Base de Datos

```bash
# Configurar credenciales en .env
php artisan migrate --seed
```

### 4. Storage

```bash
php artisan storage:link
```

## ⚙️ Configuración

### Variables Críticas

```env
# App
APP_NAME="GuaraniAppStore"
APP_URL=https://tudominio.com

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# OpenRouter (IA)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# PayPal
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=

# Telegram (7 bots)
TELEGRAM_BOT_ASSISTANT_TOKEN=
TELEGRAM_BOT_AGENDA_TOKEN=
TELEGRAM_BOT_CRYPTOSHIELD_TOKEN=
TELEGRAM_BOT_PULSE_TOKEN=
TELEGRAM_BOT_MOMENTUM_TOKEN=
TELEGRAM_BOT_SALES_TOKEN=
TELEGRAM_BOT_SOCIAL_TOKEN=
```

## 🌐 Deployment en Hostinger

### Paso 1: Preparación
1. Adquirir plan Business/Premium
2. Crear base de datos MySQL
3. Configurar dominio y SSL

### Paso 2: Subir Archivos
```bash
# Via SSH
cd public_html
git clone <repo-url> .
cd webapp
composer install --optimize-autoloader --no-dev
npm install && npm run build
```

### Paso 3: Configurar
```bash
cp .env.example .env
php artisan key:generate
php artisan migrate --seed --force
chmod -R 755 storage bootstrap/cache
```

### Paso 4: Optimizar
```bash
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### Paso 5: Cron Job
```
* * * * * cd /home/usuario/public_html/webapp && php artisan schedule:run >> /dev/null 2>&1
```

## 🤖 Telegram Bots

### Crear Bots
1. Contactar @BotFather en Telegram
2. Crear 7 bots:
   - @AsistentePersonalBot
   - @OrganizadorAgendaBot
   - @CryptoShieldBot
   - @PulseIABot
   - @MomentumPredictorBot
   - @AgenteVentasIABot
   - @GuaraniSupportBot

### Configurar Webhooks
```bash
# Agregar tokens a .env
php artisan telegram:setup-webhooks

# Verificar estado
php artisan telegram:info
```

## 💳 Pasarelas de Pago

- **PayPal**: Developer Dashboard
- **Pagopar**: https://pagopar.com
- **Bancard**: Contacto directo
- **Crypto**: Wallets BTC/ETH/USDT

## 🛠️ Comandos Útiles

```bash
# Telegram
php artisan telegram:setup-webhooks
php artisan telegram:info [bot]

# Caché
php artisan cache:clear
php artisan config:cache

# Database
php artisan migrate
php artisan db:seed

# Mantenimiento
php artisan down
php artisan up
```

## 📁 Estructura

```
webapp/
├── app/
│   ├── Console/Commands/      # Telegram commands
│   ├── Http/Controllers/
│   │   ├── Admin/             # Panel admin
│   │   ├── Services/          # 11 servicios
│   │   └── TelegramWebhookController.php
│   ├── Models/
│   └── Services/
│       └── TelegramService.php
├── config/
│   └── telegram.php
├── resources/views/
│   ├── admin/
│   ├── legal/
│   └── services/
├── .env.example
└── README.md
```

## 🔒 Seguridad

- ✅ CSRF Protection
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ Password Hashing (bcrypt)
- ✅ HTTPS Obligatorio
- ✅ Input Validation

## 📧 Soporte

Email: soporte@guaraniappstore.com  
Telegram: @GuaraniSupportBot

## 📄 Licencia

Propietaria. Todos los derechos reservados.

---

**Desarrollado con ❤️ en Paraguay** 🇵🇾
