# Guía de Seguridad - GuaraniAppStore V2.5 Pro

## 🔐 Configuración de Variables de Entorno

### Backend (.env)

1. **Copia el archivo de ejemplo:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Configura las siguientes variables críticas:**

#### Base de Datos
- `POSTGRES_URL`: Cadena de conexión PostgreSQL
- `DB_NAME`: Nombre de la base de datos

#### Seguridad JWT
- `JWT_SECRET`: Clave secreta para tokens JWT (genera una nueva con: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- `SECRET_KEY`: Clave secreta general de la aplicación

#### Bots de Telegram
- Obtén los tokens desde [@BotFather](https://t.me/botfather) en Telegram
- `GUARANI_ASSISTANT_BOT_TOKEN`
- `STOPFRAUDE_BOT_TOKEN`
- `PULSEBOT_TOKEN`
- `MOMENTUM_BOT_TOKEN`
- `ROCIO_BOT_TOKEN`

#### Pasarelas de Pago
- **Pagopar**: Obtén credenciales en [pagopar.com/developers](https://pagopar.com/developers)
  - `PAGOPAR_PUBLIC_KEY`
  - `PAGOPAR_PRIVATE_KEY`
  - `PAGOPAR_ENV` (sandbox/production)

- **Stripe**: Obtén credenciales en [dashboard.stripe.com](https://dashboard.stripe.com/apikeys)
  - `STRIPE_SECRET_KEY`
  - `STRIPE_WEBHOOK_SECRET`

#### Criptomonedas
- `BTC_WALLET`: Dirección de wallet Bitcoin
- `ETH_WALLET`: Dirección de wallet Ethereum
- `USDT_ETH_WALLET`: Dirección de wallet USDT (ERC-20)
- `ETHERSCAN_API_KEY`: API key de [etherscan.io](https://etherscan.io/myapikey)

#### APIs de IA
- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  - `OPENAI_API_KEY`

- **Anthropic Claude**: [console.anthropic.com](https://console.anthropic.com/)
  - `CLAUDE_API_KEY`

- **OpenRouter**: [openrouter.ai/keys](https://openrouter.ai/keys)
  - `OPENROUTER_API_KEY`
  - `OPENROUTER_EXTENDED_API_KEY`

#### Web Scraping
- **Outscraper**: [outscraper.com](https://outscraper.com/)
  - `OUTSCRAPER_API_KEY`

- **Apify**: [apify.com](https://apify.com/)
  - `APIFY_TOKEN`

- **CoinMarketCap**: [coinmarketcap.com/api](https://coinmarketcap.com/api/)
  - `COINMARKETCAP_API_KEY`

#### Email (Brevo/Sendinblue)
- Regístrate en [brevo.com](https://www.brevo.com/)
- `BREVO_SMTP_USER`
- `BREVO_SMTP_PASSWORD`
- `BREVO_FROM_EMAIL`
- `BREVO_FROM_NAME`

#### Google OAuth
- Obtén credenciales en [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`

### Frontend (.env)

1. **Copia el archivo de ejemplo:**
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. **Configura:**
   - `REACT_APP_BACKEND_URL`: URL del backend (producción o desarrollo)

## 🚨 Reglas de Seguridad Importantes

### ❌ NUNCA HAGAS ESTO:
1. **No subas archivos `.env` a Git** - Ya están en `.gitignore`
2. **No compartas claves en mensajes, emails o documentación**
3. **No hardcodees claves directamente en el código**
4. **No uses claves de producción en desarrollo**
5. **No commits archivos con claves expuestas**

### ✅ SIEMPRE HAZ ESTO:
1. **Usa variables de entorno** para todas las claves sensibles
2. **Rota las claves periódicamente** (cada 3-6 meses)
3. **Usa diferentes claves** para desarrollo y producción
4. **Revisa commits** antes de push para evitar leaks
5. **Mantén `.env.example` actualizado** (sin valores reales)

## 🔍 Verificación de Seguridad

### Verificar que no hay claves expuestas:
```bash
# Buscar posibles claves en el código
grep -r "sk-" --include="*.py" --include="*.js" .
grep -r "api_key.*=" --include="*.py" --include="*.js" .
```

### Verificar .gitignore:
```bash
# Asegurarse que .env está ignorado
cat .gitignore | grep ".env"
```

## 🛡️ Mejores Prácticas

### Para Desarrollo:
- Usa el modo `sandbox` para pagos
- Usa tokens de prueba cuando sea posible
- Documenta qué servicios están en modo prueba

### Para Producción:
- Cambia TODAS las claves a producción
- Activa `PAGOPAR_ENV=production`
- Configura webhooks con URLs HTTPS
- Implementa rate limiting
- Habilita logs de auditoría

## 📞 Soporte

Si necesitas ayuda con la configuración de seguridad:
- Email: security@guaraniappstore.com
- Documentación: [docs.guaraniappstore.com](https://docs.guaraniappstore.com)

---
**Última actualización:** Enero 2025
