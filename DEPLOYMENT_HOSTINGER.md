# 🚀 GUÍA DE DEPLOYMENT - HOSTINGER SHARED HOSTING

**GuaraniAppStore V2.5**
**Fecha:** 2025-11-15
**Plataforma:** Hostinger Hosting Compartido
**Nivel:** Paso a paso (Principiante-Intermedio)

---

## 📋 ÍNDICE

1. [Requisitos Previos](#requisitos-previos)
2. [Preparación del Entorno Hostinger](#preparación-del-entorno-hostinger)
3. [Subir Archivos al Servidor](#subir-archivos-al-servidor)
4. [Configurar Base de Datos](#configurar-base-de-datos)
5. [Ejecutar Script de Deployment](#ejecutar-script-de-deployment)
6. [Configurar Document Root](#configurar-document-root)
7. [Configurar Webhooks de Telegram](#configurar-webhooks-de-telegram)
8. [Verificación Final](#verificación-final)
9. [Solución de Problemas](#solución-de-problemas)

---

## ✅ REQUISITOS PREVIOS

Antes de comenzar, asegúrate de tener:

- [x] **Cuenta de Hostinger activa** con plan de hosting compartido
- [x] **Dominio configurado** y apuntando a Hostinger
- [x] **Acceso al Panel de Hostinger** (hPanel)
- [x] **Cliente SSH** instalado (PuTTY para Windows, Terminal para Mac/Linux)
- [x] **Credenciales SSH** (las obtienes del panel de Hostinger)
- [x] **Tokens de Telegram Bots** (al menos el bot de soporte)
- [x] **API Key de OpenRouter** (para servicios de IA)

### Requisitos del Servidor (verificar en Hostinger):

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| **PHP** | 8.1 | 8.2 o 8.3 |
| **MySQL** | 5.7 | 8.0 |
| **Espacio en disco** | 500 MB | 1 GB |
| **RAM** | 512 MB | 1 GB |
| **SSL/HTTPS** | ✅ Requerido | ✅ Incluido |

---

## 🔧 PREPARACIÓN DEL ENTORNO HOSTINGER

### Paso 1: Configurar PHP

1. Accede al **hPanel de Hostinger**
2. Ve a **Advanced** > **PHP Configuration**
3. Selecciona **PHP 8.2** o superior
4. Activa las siguientes extensiones:
   - ✅ `pdo_mysql`
   - ✅ `mbstring`
   - ✅ `openssl`
   - ✅ `tokenizer`
   - ✅ `xml`
   - ✅ `ctype`
   - ✅ `json`
   - ✅ `bcmath`
   - ✅ `curl`
   - ✅ `fileinfo`
5. Click en **Save**

### Paso 2: Activar Acceso SSH

1. En el hPanel, ve a **Advanced** > **SSH Access**
2. Click en **Enable SSH Access**
3. Anota las credenciales:
   ```
   Host: ssh.hostinger.com (o tu servidor específico)
   Port: 65002 (o el que te indique)
   Username: u123456789 (tu usuario)
   Password: (configura una contraseña SSH)
   ```

### Paso 3: Activar SSL/HTTPS

1. Ve a **SSL** en el hPanel
2. Si no está activo, click en **Install SSL**
3. Hostinger instala SSL gratuito automáticamente
4. Verifica que tu dominio carga con `https://`

---

## 📤 SUBIR ARCHIVOS AL SERVIDOR

### Opción A: Via SSH + Git (Recomendado)

**Conectarse por SSH:**

```bash
# Desde terminal (Mac/Linux) o PuTTY (Windows)
ssh u123456789@ssh.hostinger.com -p 65002
```

**Clonar el repositorio:**

```bash
# Navegar al directorio correcto
cd domains/tudominio.com/public_html

# Clonar el proyecto
git clone https://github.com/Benifotrem/GuaraniAppStore-V2.5.git webapp

# Entrar al directorio
cd webapp
```

### Opción B: Via FileZilla (FTP)

1. Descarga el proyecto en tu computadora
2. Conecta via FTP con FileZilla:
   - Host: `ftp.tudominio.com`
   - Usuario: Tu usuario de Hostinger
   - Contraseña: Tu contraseña de Hostinger
   - Puerto: 21
3. Sube toda la carpeta `webapp` a `public_html/`

---

## 🗄️ CONFIGURAR BASE DE DATOS

### Paso 1: Crear Base de Datos MySQL

1. En hPanel, ve a **Databases** > **MySQL Databases**
2. Click en **Create Database**
3. Configura:
   ```
   Database name: u123456789_guarani
   Database username: u123456789_admin
   Password: [genera una contraseña segura]
   ```
4. Click en **Create**
5. **⚠️ IMPORTANTE:** Anota estos datos, los necesitarás para el `.env`

### Paso 2: Importar el Schema SQL

1. En hPanel, ve a **Databases** > **phpMyAdmin**
2. En el panel izquierdo, selecciona la base de datos recién creada (`u123456789_guarani`)
3. Click en la pestaña **Import**
4. Click en **Choose File**
5. Selecciona el archivo `database.sql` (lo puedes subir via FTP primero o copiar su contenido)
6. Click en **Go** (abajo)
7. Espera a que termine (deberías ver "Import has been successfully finished")

### Paso 3: Verificar las Tablas

1. En phpMyAdmin, click en la base de datos
2. Deberías ver **14 tablas**:
   ```
   ✅ users
   ✅ services
   ✅ subscriptions
   ✅ payments
   ✅ payment_gateways
   ✅ api_credentials
   ✅ password_reset_tokens
   ✅ sessions
   ✅ cache
   ✅ cache_locks
   ✅ jobs
   ✅ job_batches
   ✅ failed_jobs
   ✅ telegram_logs
   ```
3. Verifica que la tabla `services` tenga **11 filas** (los 11 servicios)
4. Verifica que la tabla `users` tenga **1 fila** (el admin)

---

## ⚙️ EJECUTAR SCRIPT DE DEPLOYMENT

### Conectarse por SSH

```bash
ssh u123456789@ssh.hostinger.com -p 65002
cd domains/tudominio.com/public_html/webapp
```

### Ejecutar el Script de Deployment

```bash
# Dar permisos de ejecución
chmod +x deploy-hostinger.sh

# Ejecutar el script
./deploy-hostinger.sh
```

### Qué hace el script automáticamente:

1. ✅ Verifica PHP y Composer
2. ✅ Instala dependencias de Laravel
3. ✅ Crea el archivo `.env` (si no existe)
4. ✅ Genera la `APP_KEY`
5. ✅ Configura permisos de directorios
6. ✅ Crea symlink de storage
7. ✅ Optimiza Laravel para producción

### Durante la ejecución, te pedirá:

**1. Configurar el .env:**

Cuando veas este mensaje:
```
⚠️  IMPORTANTE: Configura tu .env AHORA
```

Presiona `Ctrl+C`, edita el `.env` y configura:

```bash
nano .env
```

Configura estas variables críticas:

```env
APP_NAME="GuaraniAppStore"
APP_ENV=production
APP_DEBUG=false
APP_URL=https://tudominio.com

DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=u123456789_guarani
DB_USERNAME=u123456789_admin
DB_PASSWORD=tu_contraseña_mysql

# Telegram Bots (mínimo el de soporte)
TELEGRAM_BOT_SUPPORT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_BOT_SALES_TOKEN=
TELEGRAM_BOT_ASSISTANT_TOKEN=
TELEGRAM_BOT_CRYPTOSHIELD_TOKEN=
TELEGRAM_BOT_PULSE_TOKEN=
TELEGRAM_BOT_MOMENTUM_TOKEN=
TELEGRAM_BOT_AGENDA_TOKEN=

# OpenRouter (para servicios de IA)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx

# Google (opcional por ahora)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# PayPal (opcional por ahora)
PAYPAL_CLIENT_ID=
PAYPAL_CLIENT_SECRET=
```

Guarda con `Ctrl+O`, Enter, `Ctrl+X`

Ejecuta el script de nuevo:
```bash
./deploy-hostinger.sh
```

**2. Confirmar importación de database.sql:**

Cuando veas:
```
¿Ya importaste database.sql en phpMyAdmin? (s/N):
```

Escribe `s` y presiona Enter (porque ya lo hiciste en el paso anterior)

---

## 🌐 CONFIGURAR DOCUMENT ROOT

**⚠️ CRÍTICO:** Si no haces esto, la aplicación NO funcionará.

### En el hPanel de Hostinger:

1. Ve a **Websites** > selecciona tu dominio
2. Click en **Manage**
3. En el menú lateral, ve a **Advanced** > **Document Root**
4. Cambia el Document Root de:
   ```
   /public_html
   ```
   A:
   ```
   /public_html/webapp/public
   ```
5. Click en **Save**
6. Espera 1-2 minutos para que se aplique el cambio

### Verificar .htaccess

Conéctate por SSH y verifica:

```bash
cd domains/tudominio.com/public_html/webapp/public
cat .htaccess
```

Deberías ver el contenido del `.htaccess` de Laravel. Si no existe, créalo:

```bash
nano .htaccess
```

Pega este contenido:

```apache
<IfModule mod_rewrite.c>
    <IfModule mod_negotiation.c>
        Options -MultiViews -Indexes
    </IfModule>

    RewriteEngine On

    # Handle Authorization Header
    RewriteCond %{HTTP:Authorization} .
    RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]

    # Redirect Trailing Slashes If Not A Folder...
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_URI} (.+)/$
    RewriteRule ^ %1 [L,R=301]

    # Send Requests To Front Controller...
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^ index.php [L]
</IfModule>
```

Guarda y cierra.

---

## 🤖 CONFIGURAR WEBHOOKS DE TELEGRAM

### Paso 1: Obtener Tokens de Telegram Bots

Para cada bot que quieras activar:

1. Habla con **@BotFather** en Telegram
2. Usa `/newbot` para crear un bot nuevo
3. Sigue las instrucciones
4. Copia el **token** (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. Añade el token al `.env` en la variable correspondiente

**Bots necesarios:**

| Bot | Variable en .env | Propósito |
|-----|------------------|-----------|
| **Soporte** | `TELEGRAM_BOT_SUPPORT_TOKEN` | ⚠️ Mínimo requerido |
| Ventas | `TELEGRAM_BOT_SALES_TOKEN` | Para Agente de Ventas IA |
| Asistente | `TELEGRAM_BOT_ASSISTANT_TOKEN` | Para Asistente Personal |
| CryptoShield | `TELEGRAM_BOT_CRYPTOSHIELD_TOKEN` | Para Suite Crypto |
| Pulse IA | `TELEGRAM_BOT_PULSE_TOKEN` | Para Suite Crypto |
| Momentum | `TELEGRAM_BOT_MOMENTUM_TOKEN` | Para Suite Crypto |
| Agenda | `TELEGRAM_BOT_AGENDA_TOKEN` | Para Organizador Agenda |

### Paso 2: Configurar los Webhooks

Conéctate por SSH:

```bash
ssh u123456789@ssh.hostinger.com -p 65002
cd domains/tudominio.com/public_html/webapp
```

Ejecuta el comando de configuración:

```bash
php artisan telegram:setup-webhooks
```

**Salida esperada:**

```
🔧 Configurando Webhooks de Telegram...
═══════════════════════════════════════

✅ Bot 'sales' - Webhook configurado: https://tudominio.com/telegram/webhook/agente-ventas
✅ Bot 'assistant' - Webhook configurado: https://tudominio.com/telegram/webhook/asistente-personal
✅ Bot 'support' - Webhook configurado: https://tudominio.com/telegram/webhook/soporte
✅ Bot 'cryptoshield' - Webhook configurado: https://tudominio.com/telegram/webhook/cryptoshield
✅ Bot 'pulse' - Webhook configurado: https://tudominio.com/telegram/webhook/pulse
✅ Bot 'momentum' - Webhook configurado: https://tudominio.com/telegram/webhook/momentum
✅ Bot 'agenda' - Webhook configurado: https://tudominio.com/telegram/webhook/agenda

🎉 Webhooks configurados exitosamente!
```

### Paso 3: Verificar Estado de los Bots

```bash
php artisan telegram:info
```

**Salida esperada:**

```
📊 Estado de Bots de Telegram
═══════════════════════════════════════

Bot: sales
  ✅ Token configurado
  ✅ Webhook activo: https://tudominio.com/telegram/webhook/agente-ventas
  ✅ Pending updates: 0

Bot: assistant
  ✅ Token configurado
  ✅ Webhook activo: https://tudominio.com/telegram/webhook/asistente-personal
  ✅ Pending updates: 0

[... resto de bots ...]
```

### Paso 4: Probar un Bot

1. Busca tu bot en Telegram (el nombre que le diste a @BotFather)
2. Envía `/start`
3. Deberías recibir una respuesta del bot
4. Si no responde, revisa los logs:
   ```bash
   tail -f storage/logs/laravel.log
   ```

---

## ✅ VERIFICACIÓN FINAL

### Checklist de Deployment

- [ ] **1. Website carga correctamente**
  - Visita: `https://tudominio.com`
  - Deberías ver la página de inicio con los servicios

- [ ] **2. Login funciona**
  - Ve a: `https://tudominio.com/login`
  - Credenciales:
    - Email: `admin@guaraniappstore.com`
    - Password: `admin123`
  - ⚠️ **Cambia la contraseña inmediatamente**

- [ ] **3. Dashboard carga**
  - Después del login, deberías ver el dashboard del admin

- [ ] **4. Panel admin funciona**
  - Ve a: `https://tudominio.com/admin/dashboard`
  - Deberías ver las estadísticas

- [ ] **5. Base de datos conectada**
  - En el dashboard, deberías ver:
    - Total de servicios: 11
    - Total de usuarios: 1
    - Pasarelas de pago: 4

- [ ] **6. Bots de Telegram responden**
  - Envía `/start` a cada bot configurado
  - Todos deben responder

- [ ] **7. HTTPS activo**
  - El candado verde debe aparecer en el navegador
  - No debe haber advertencias de seguridad

- [ ] **8. SEO configurado**
  - Visita: `https://tudominio.com/sitemap.xml`
  - Deberías ver el XML del sitemap

### Comandos de Verificación (SSH)

```bash
# Ver estado de Laravel
php artisan about

# Ver rutas configuradas
php artisan route:list

# Ver estado de la base de datos
php artisan db:show

# Ver estado de los bots
php artisan telegram:info

# Ver logs en tiempo real
tail -f storage/logs/laravel.log
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Problema: "500 Internal Server Error"

**Causa:** Permisos incorrectos o .env mal configurado

**Solución:**

```bash
cd /home/uXXXXXXXXX/domains/tudominio.com/public_html/webapp

# Verificar permisos
chmod -R 755 storage bootstrap/cache
chmod -R 775 storage/logs

# Limpiar caché
php artisan config:clear
php artisan cache:clear
php artisan view:clear

# Re-cachear
php artisan config:cache
php artisan route:cache
php artisan view:cache
```

### Problema: "Base de datos no conecta"

**Verificar credenciales:**

```bash
nano .env
```

Asegúrate de que:
- `DB_HOST=localhost` (no 127.0.0.1)
- Usuario y contraseña son correctos
- Base de datos existe en phpMyAdmin

**Probar conexión:**

```bash
php artisan tinker
```

Luego en tinker:
```php
DB::connection()->getPdo();
exit
```

Si da error, las credenciales están mal.

### Problema: "Class not found" o "Target class does not exist"

**Solución:**

```bash
# Regenerar autoload
composer dump-autoload

# Limpiar caché
php artisan config:clear
php artisan cache:clear

# Re-cachear
php artisan config:cache
```

### Problema: Bots de Telegram no responden

**Verificar webhook:**

```bash
php artisan telegram:info
```

**Re-configurar webhooks:**

```bash
# Borrar webhooks actuales
php artisan telegram:setup-webhooks --delete

# Configurar de nuevo
php artisan telegram:setup-webhooks
```

**Verificar que HTTPS funciona:**

Los webhooks de Telegram **requieren HTTPS**. Verifica que tu sitio carga con `https://` y sin errores de certificado.

### Problema: "Permission denied" al ejecutar comandos

**Causa:** Algunos directorios no tienen permisos de escritura

**Solución:**

```bash
# Desde SSH
cd /home/uXXXXXXXXX/domains/tudominio.com/public_html/webapp

# Arreglar permisos
find storage -type d -exec chmod 755 {} \;
find storage -type f -exec chmod 644 {} \;
find bootstrap/cache -type d -exec chmod 755 {} \;
find bootstrap/cache -type f -exec chmod 644 {} \;
```

### Problema: "Composer command not found"

**Solución:**

```bash
# Descargar composer localmente
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"

# Usar composer.phar
php composer.phar install --optimize-autoloader --no-dev
```

### Problema: El sitio carga pero sin estilos CSS

**Causa:** El Document Root no está configurado correctamente

**Solución:**

1. Ve al hPanel > Advanced > Document Root
2. Asegúrate de que apunta a: `/public_html/webapp/public`
3. Espera 2-3 minutos
4. Limpia caché del navegador (Ctrl+Shift+R)

---

## 📞 SOPORTE Y RECURSOS

### Documentación Oficial:

- **Laravel:** https://laravel.com/docs/11.x
- **Hostinger:** https://support.hostinger.com
- **Telegram Bot API:** https://core.telegram.org/bots/api

### Logs Útiles:

```bash
# Log de Laravel
tail -f storage/logs/laravel.log

# Log de PHP (Hostinger)
tail -f ~/logs/error_log

# Log de acceso
tail -f ~/logs/access_log
```

### Comandos Útiles de Laravel:

```bash
# Ver información del sistema
php artisan about

# Limpiar TODA la caché
php artisan optimize:clear

# Optimizar TODO para producción
php artisan optimize

# Ver rutas
php artisan route:list

# Ver configuración actual
php artisan config:show

# Entrar al REPL de Laravel
php artisan tinker
```

---

## 🎉 DEPLOYMENT COMPLETADO

Si llegaste hasta aquí y todos los checks están ✅, ¡felicidades!

Tu **GuaraniAppStore V2.5** está corriendo en producción en Hostinger.

### Próximos Pasos:

1. ✅ **Cambiar password del admin** (muy importante)
2. ✅ **Configurar backup automático** de la base de datos
3. ✅ **Activar todas las APIs externas** (Google, PayPal, OpenRouter)
4. ✅ **Configurar los 7 bots de Telegram**
5. ✅ **Probar cada servicio individualmente**
6. ✅ **Configurar sistema de pagos**
7. ✅ **Hacer testing en producción**

---

**Generado:** 2025-11-15
**Versión:** 2.5
**Soporte:** GuaraniAppStore Team
