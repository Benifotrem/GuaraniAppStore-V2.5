# ✅ CHECKLIST POST-DEPLOYMENT

**GuaraniAppStore V2.5** - Verificación de Producción
**Deployment en:** Hostinger Shared Hosting

---

## 🎯 USO DE ESTE CHECKLIST

1. Marca cada item con `[x]` cuando lo completes
2. Ejecuta los comandos de verificación proporcionados
3. Si algo falla, ve a la sección "Solución" del item
4. NO continues al siguiente paso hasta resolver problemas

---

## 1️⃣ VERIFICACIÓN DE INFRAESTRUCTURA

### [ ] 1.1 Servidor y Dominio

**Verificar:**
- [ ] El dominio carga con HTTPS (candado verde)
- [ ] No hay advertencias de certificado SSL
- [ ] El dominio redirige de HTTP a HTTPS automáticamente

**Comandos de verificación:**
```bash
# Test SSL
curl -I https://tudominio.com | grep "HTTP"

# Debería mostrar: HTTP/2 200
```

**Solución si falla:**
- Ve a Hostinger Panel > SSL
- Verifica que SSL esté activado
- Espera 10-15 minutos para propagación DNS

---

### [ ] 1.2 PHP y Extensiones

**Verificar:**
- [ ] PHP versión 8.1 o superior
- [ ] Extensiones PHP requeridas activas

**Comandos de verificación:**
```bash
# Via SSH
php -v

# Ver extensiones
php -m | grep -E "pdo_mysql|mbstring|openssl|xml|curl"
```

**Salida esperada:**
```
PHP 8.2.x (o 8.3.x)
pdo_mysql
mbstring
openssl
xml
curl
```

**Solución si falla:**
- Hostinger Panel > PHP Configuration
- Selecciona PHP 8.2 o 8.3
- Activa extensiones faltantes

---

### [ ] 1.3 Document Root

**Verificar:**
- [ ] Document Root apunta a `/public_html/webapp/public`
- [ ] Archivo `.htaccess` existe en `public/`

**Comandos de verificación:**
```bash
# Via SSH
cd /home/uXXXXXXXXX/domains/tudominio.com/public_html/webapp/public
ls -la .htaccess

# Debería mostrar el archivo .htaccess
```

**Solución si falla:**
1. Hostinger Panel > Advanced > Document Root
2. Cambiar a: `/public_html/webapp/public`
3. Guardar y esperar 2-3 minutos

---

## 2️⃣ VERIFICACIÓN DE ARCHIVOS Y PERMISOS

### [ ] 2.1 Archivos Críticos

**Verificar que existen:**
- [ ] `.env` configurado
- [ ] `composer.json`
- [ ] `artisan`
- [ ] `public/index.php`

**Comandos de verificación:**
```bash
# Via SSH
cd /home/uXXXXXXXXX/domains/tudominio.com/public_html/webapp

ls -la .env composer.json artisan public/index.php

# Todos deben existir
```

**Solución si falla:**
- Re-subir archivos faltantes via FTP
- Verificar que subiste TODO el contenido de la carpeta `webapp`

---

### [ ] 2.2 Permisos de Directorios

**Verificar:**
- [ ] `storage/` tiene permisos 755
- [ ] `bootstrap/cache/` tiene permisos 755
- [ ] Laravel puede escribir logs

**Comandos de verificación:**
```bash
# Via SSH
cd /home/uXXXXXXXXX/domains/tudominio.com/public_html/webapp

# Ver permisos
ls -ld storage bootstrap/cache

# Debería mostrar: drwxr-xr-x
```

**Comandos de corrección:**
```bash
chmod -R 755 storage bootstrap/cache
chmod -R 775 storage/logs
```

---

### [ ] 2.3 Storage Link

**Verificar:**
- [ ] Symlink `public/storage` existe y apunta a `../storage/app/public`

**Comandos de verificación:**
```bash
# Via SSH
ls -la public/storage

# Debería mostrar: public/storage -> ../storage/app/public
```

**Solución si falla:**
```bash
php artisan storage:link
```

---

## 3️⃣ VERIFICACIÓN DE BASE DE DATOS

### [ ] 3.1 Conexión a MySQL

**Verificar:**
- [ ] Laravel puede conectar a MySQL
- [ ] Credenciales en `.env` son correctas

**Comandos de verificación:**
```bash
# Via SSH
php artisan db:show

# Debería mostrar información de MySQL
```

**Salida esperada:**
```
MySQL ............... 8.0.x
Database ............ u123456789_guarani
Host ................ localhost
Username ............ u123456789_admin
```

**Solución si falla:**
1. Verifica credenciales en `.env`:
   ```bash
   nano .env
   ```
2. Asegúrate de que:
   - `DB_HOST=localhost` (NO 127.0.0.1)
   - Usuario y contraseña correctos
   - Base de datos existe en phpMyAdmin

---

### [ ] 3.2 Tablas Importadas

**Verificar:**
- [ ] 14 tablas existen en la base de datos
- [ ] Tabla `services` tiene 11 servicios
- [ ] Tabla `users` tiene 1 admin

**Comandos de verificación:**
```bash
# Via SSH
php artisan tinker
```

Luego en tinker:
```php
// Contar tablas (indirecto)
\DB::table('services')->count(); // Debería ser 11
\DB::table('users')->count();    // Debería ser 1
\DB::table('payment_gateways')->count(); // Debería ser 4
exit
```

**Solución si falla:**
- Ve a phpMyAdmin
- Selecciona la base de datos
- Importa `database.sql` nuevamente

---

## 4️⃣ VERIFICACIÓN DE LARAVEL

### [ ] 4.1 APP_KEY Generada

**Verificar:**
- [ ] `APP_KEY` en `.env` tiene un valor
- [ ] Formato: `base64:XXXXXXXXXXXX`

**Comandos de verificación:**
```bash
# Via SSH
grep APP_KEY .env

# Debería mostrar: APP_KEY=base64:xxxxxxxxxxxxxxxxxxx
```

**Solución si falla:**
```bash
php artisan key:generate --force
```

---

### [ ] 4.2 Cache y Optimizaciones

**Verificar:**
- [ ] Config cache generada
- [ ] Routes cache generada
- [ ] Views cache generada

**Comandos de verificación:**
```bash
# Via SSH
ls -la bootstrap/cache/config.php
ls -la bootstrap/cache/routes*.php

# Ambos deben existir
```

**Regenerar si falla:**
```bash
php artisan config:clear
php artisan route:clear
php artisan view:clear

php artisan config:cache
php artisan route:cache
php artisan view:cache
```

---

### [ ] 4.3 Laravel Funciona

**Verificar:**
- [ ] Comando `php artisan about` funciona sin errores

**Comandos de verificación:**
```bash
# Via SSH
php artisan about
```

**Salida esperada:**
```
Environment .............. production
Debug Mode ............... OFF
URL ...................... https://tudominio.com
Database ................. mysql (connected)
Cache Driver ............. database
Session Driver ........... database
Queue Driver ............. database
```

**Solución si falla:**
- Revisa `.env` línea por línea
- Ejecuta `php artisan config:clear`

---

## 5️⃣ VERIFICACIÓN WEB (FRONTEND)

### [ ] 5.1 Página de Inicio

**Verificar:**
- [ ] `https://tudominio.com` carga sin errores
- [ ] Se ven los 11 servicios
- [ ] Diseño glass morphism funciona
- [ ] No hay errores 404 de assets (CSS/JS)

**Test manual:**
1. Abre en navegador: `https://tudominio.com`
2. Verifica que carga la landing page
3. Presiona F12 > Console
4. NO debe haber errores en rojo

**Solución si falla:**
- Verifica Document Root en Hostinger Panel
- Limpia caché del navegador (Ctrl+Shift+R)
- Revisa `storage/logs/laravel.log`

---

### [ ] 5.2 Login de Admin

**Verificar:**
- [ ] Página de login carga: `https://tudominio.com/login`
- [ ] Puedes hacer login con credenciales por defecto

**Test manual:**
1. Ve a: `https://tudominio.com/login`
2. Usa:
   - Email: `admin@guaraniappstore.com`
   - Password: `admin123`
3. Deberías ser redirigido al dashboard

**Solución si falla:**
- Verifica que la tabla `users` tiene el admin
- En phpMyAdmin, ejecuta:
  ```sql
  SELECT * FROM users WHERE email = 'admin@guaraniappstore.com';
  ```
- Si no existe, re-importa `database.sql`

---

### [ ] 5.3 Dashboard de Admin

**Verificar:**
- [ ] Dashboard carga: `https://tudominio.com/admin/dashboard`
- [ ] Muestra estadísticas correctas
- [ ] Todos los menús funcionan

**Test manual:**
1. Después de login, ve a: `https://tudominio.com/admin/dashboard`
2. Verifica que se ven:
   - Total de usuarios
   - Total de servicios (debe ser 11)
   - Total de pagos
   - Pasarelas activas (debe ser 4)

**Solución si falla:**
- Revisa permisos del usuario admin
- Verifica middleware en `routes/web.php`

---

### [ ] 5.4 Páginas Legales y SEO

**Verificar:**
- [ ] `/faq` carga correctamente
- [ ] `/terms` carga correctamente
- [ ] `/privacy` carga correctamente
- [ ] `/sitemap.xml` genera XML correcto

**Test manual:**
1. Visita cada URL y verifica que cargan
2. Para sitemap: `https://tudominio.com/sitemap.xml`
   - Debe mostrar XML válido
   - Debe incluir los 11 servicios

**Solución si falla:**
- Verifica rutas en `routes/web.php`
- Ejecuta `php artisan route:list | grep -E "faq|terms|privacy|sitemap"`

---

## 6️⃣ VERIFICACIÓN DE TELEGRAM BOTS

### [ ] 6.1 Tokens Configurados

**Verificar:**
- [ ] Al menos 1 bot tiene token en `.env`
- [ ] Formato del token es correcto

**Comandos de verificación:**
```bash
# Via SSH
grep TELEGRAM_BOT .env | grep -v "^#"

# Debería mostrar al menos 1 token configurado
```

**Formato correcto:**
```
TELEGRAM_BOT_SUPPORT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**Solución si falla:**
1. Obtén tokens de @BotFather en Telegram
2. Añade al `.env`
3. Ejecuta `php artisan config:clear`

---

### [ ] 6.2 Webhooks Configurados

**Verificar:**
- [ ] Webhooks de Telegram están configurados
- [ ] Apuntan a URLs correctas

**Comandos de verificación:**
```bash
# Via SSH
php artisan telegram:info
```

**Salida esperada:**
```
Bot: support
  ✅ Token configurado
  ✅ Webhook activo: https://tudominio.com/telegram/webhook/soporte
  ✅ Pending updates: 0
```

**Solución si falla:**
```bash
# Configurar webhooks
php artisan telegram:setup-webhooks

# Si da error, primero borra y luego configura
php artisan telegram:setup-webhooks --delete
php artisan telegram:setup-webhooks
```

---

### [ ] 6.3 Bots Responden

**Verificar:**
- [ ] Bot responde a mensajes en Telegram

**Test manual:**
1. Abre Telegram
2. Busca tu bot
3. Envía: `/start`
4. Debería responder en menos de 5 segundos

**Solución si falla:**
1. Verifica que webhook esté activo (`telegram:info`)
2. Verifica que HTTPS funciona (bots requieren HTTPS)
3. Revisa logs:
   ```bash
   tail -f storage/logs/laravel.log
   ```
4. Envía un mensaje al bot y verifica que aparece en el log

---

## 7️⃣ VERIFICACIÓN DE APIS EXTERNAS

### [ ] 7.1 OpenRouter (IA)

**Verificar:**
- [ ] `OPENROUTER_API_KEY` está configurada
- [ ] API responde correctamente

**Comandos de verificación:**
```bash
# Via SSH
php artisan tinker
```

Luego:
```php
// Test simple de API
$key = env('OPENROUTER_API_KEY');
echo strlen($key) > 10 ? "✅ API Key configurada" : "❌ API Key faltante";
exit
```

**Solución si falla:**
1. Obtén API key en: https://openrouter.ai/keys
2. Añade a `.env`: `OPENROUTER_API_KEY=sk-or-v1-xxxxx`
3. Ejecuta: `php artisan config:clear`

---

### [ ] 7.2 Google APIs (Opcional)

**Verificar:**
- [ ] Si usas Calendar/Drive, credenciales configuradas

**Comandos de verificación:**
```bash
# Via SSH
grep GOOGLE .env | grep -v "^#"
```

**Solución:**
- Configura solo si vas a usar servicios que requieren Google
- Ver guía: https://console.cloud.google.com

---

## 8️⃣ VERIFICACIÓN DE PASARELAS DE PAGO

### [ ] 8.1 Gateways en Base de Datos

**Verificar:**
- [ ] 4 pasarelas existen en la tabla `payment_gateways`

**Comandos de verificación:**
```bash
# Via SSH
php artisan tinker
```

Luego:
```php
\App\Models\PaymentGateway::all()->pluck('gateway_name');
// Debería mostrar: ["paypal", "pagopar", "bancard", "crypto"]
exit
```

**Solución si falla:**
- Re-importa `database.sql` en phpMyAdmin

---

### [ ] 8.2 Panel de Gateways Funciona

**Verificar:**
- [ ] Panel de pasarelas carga: `https://tudominio.com/admin/gateways`
- [ ] Puedes activar/desactivar gateways

**Test manual:**
1. Login como admin
2. Ve a: `https://tudominio.com/admin/gateways`
3. Verifica que se ven las 4 pasarelas
4. Intenta activar/desactivar una

**Solución si falla:**
- Verifica que estás logueado como admin
- Revisa `app/Http/Controllers/AdminController.php`

---

## 9️⃣ VERIFICACIÓN DE SEGURIDAD

### [ ] 9.1 Configuración de Producción

**Verificar:**
- [ ] `APP_ENV=production`
- [ ] `APP_DEBUG=false`
- [ ] `APP_URL` es HTTPS

**Comandos de verificación:**
```bash
# Via SSH
grep -E "APP_ENV|APP_DEBUG|APP_URL" .env
```

**Debe mostrar:**
```
APP_ENV=production
APP_DEBUG=false
APP_URL=https://tudominio.com
```

**Solución si falla:**
- Edita `.env`
- Ejecuta `php artisan config:clear && php artisan config:cache`

---

### [ ] 9.2 Cambiar Password del Admin

**Verificar:**
- [ ] Password del admin cambió de `admin123`

**Test manual:**
1. Login como admin
2. Ve a perfil o settings
3. Cambia password a algo seguro
4. Logout y login con nuevo password

**Solución si falla (cambiar manualmente):**
```bash
# Via SSH
php artisan tinker
```

Luego:
```php
$admin = \App\Models\User::where('email', 'admin@guaraniappstore.com')->first();
$admin->password = bcrypt('TuNuevoPasswordSeguro123!');
$admin->save();
exit
```

---

### [ ] 9.3 Archivos Sensibles Protegidos

**Verificar:**
- [ ] `.env` NO es accesible via web
- [ ] `storage/` NO es accesible via web

**Test manual:**
1. Intenta acceder a: `https://tudominio.com/.env`
   - Debe dar error 404 o 403
2. Intenta acceder a: `https://tudominio.com/storage/logs/laravel.log`
   - Debe dar error 404 o 403

**Solución si falla:**
- Verifica que Document Root apunta a `/public`
- Verifica que `.htaccess` existe en `public/`

---

## 🔟 VERIFICACIÓN DE LOGGING Y MONITOREO

### [ ] 10.1 Logs Funcionan

**Verificar:**
- [ ] Laravel puede escribir logs
- [ ] No hay errores críticos en logs

**Comandos de verificación:**
```bash
# Via SSH
tail -20 storage/logs/laravel.log

# No debe haber líneas con "ERROR" o "CRITICAL"
```

**Solución si falla:**
- Verifica permisos: `chmod -R 775 storage/logs`
- Verifica espacio en disco: `df -h`

---

### [ ] 10.2 Monitoreo de Errores

**Verificar:**
- [ ] Puedes ver errores 500 si ocurren

**Test manual:**
1. Causa un error intencional:
   - Ve a una URL que no existe: `https://tudominio.com/ruta-inexistente`
   - Debería mostrar página 404 personalizada (si la configuraste)
   - O página 404 por defecto de Laravel
2. Revisa el log:
   ```bash
   tail -20 storage/logs/laravel.log
   ```

**Solución si falla:**
- Configura páginas de error personalizadas en `resources/views/errors/`

---

## ✅ CHECKLIST FINAL

Marca los puntos principales:

- [ ] ✅ Website carga correctamente
- [ ] ✅ Login funciona
- [ ] ✅ Dashboard funciona
- [ ] ✅ Base de datos conectada
- [ ] ✅ Telegram bots responden
- [ ] ✅ HTTPS activo
- [ ] ✅ Password de admin cambiado
- [ ] ✅ `.env` configurado correctamente
- [ ] ✅ Logs funcionan
- [ ] ✅ Permisos correctos

---

## 🎉 SI TODOS LOS CHECKS ESTÁN MARCADOS

**¡FELICITACIONES!** Tu GuaraniAppStore V2.5 está completamente deployado y funcionando en producción.

### Próximos pasos:

1. **Backup de base de datos:**
   - En phpMyAdmin > Export > SQL
   - Guarda el backup en lugar seguro
   - Configura backups automáticos en Hostinger Panel

2. **Configurar APIs externas:**
   - PayPal credentials (producción)
   - OpenRouter API key
   - Google APIs según necesites

3. **Testing de servicios:**
   - Prueba cada uno de los 11 servicios
   - Verifica que las funcionalidades críticas funcionan

4. **Monitoreo:**
   - Revisa logs diariamente al principio
   - Configura alertas de errores

5. **Marketing:**
   - Anuncia el lanzamiento
   - Configura bots de Telegram para soporte

---

## 📝 NOTAS Y OBSERVACIONES

Usa este espacio para anotar problemas encontrados y soluciones:

```
Fecha: _____________
Problema: ___________________________________________________________
Solución: ___________________________________________________________

Fecha: _____________
Problema: ___________________________________________________________
Solución: ___________________________________________________________

Fecha: _____________
Problema: ___________________________________________________________
Solución: ___________________________________________________________
```

---

**Última actualización:** 2025-11-15
**Versión del checklist:** 1.0
**Plataforma:** Hostinger Shared Hosting
