"""
Bot de Telegram para Pulse IA
Análisis de sentimiento del mercado crypto
"""
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient

from pulse_service import PulseIAService

# Configuración
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', os.environ.get('CRYPTO_BOTS_TOKEN'))
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')

# Servicio de Pulse IA
pulse_service = None

class PulseTelegramBot:
    def __init__(self):
        self.db_client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.db_client.get_database()
        global pulse_service
        if pulse_service is None:
            pulse_service = PulseIAService()
        self.pulse = pulse_service
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Registrar usuario
        await self.register_user(chat_id, user.username)
        
        keyboard = [
            [
                InlineKeyboardButton("📊 BTC Analysis", callback_data='pulse_BTC'),
                InlineKeyboardButton("📊 ETH Analysis", callback_data='pulse_ETH')
            ],
            [
                InlineKeyboardButton("⚙️ Configuración", callback_data='pulse_config'),
                InlineKeyboardButton("📈 Trending", callback_data='pulse_trending')
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""📊 *¡Bienvenido a Pulse IA!*

Hola {user.first_name}, soy tu asistente de análisis de sentimiento del mercado crypto.

*¿Qué puedo hacer?*
• Analizar sentimiento de cualquier crypto
• Detectar FOMO y FUD en tiempo real
• Monitorear 15+ fuentes de noticias
• Rastrear Twitter y Reddit
• Proporcionar recomendaciones

*Comandos disponibles:*
/pulse <SYMBOL> - Analizar sentimiento
/trending - Ver cryptos trending
/track <SYMBOL> - Trackear símbolo
/config - Configurar alertas
/help - Ayuda

¡Selecciona una opción para empezar! 👇
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def pulse_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /pulse <SYMBOL>"""
        symbol = context.args[0].upper() if context.args else 'BTC'
        
        processing_msg = await update.message.reply_text(
            f"📊 Analizando sentimiento de {symbol}...\n⏳ Esto puede tomar 30-60 segundos..."
        )
        
        try:
            # Analizar sentimiento
            analysis = await self.pulse.analyze_crypto_sentiment(symbol)
            
            # Guardar en base de datos
            await self.save_analysis(analysis, update.effective_chat.id)
            
            # Formatear mensaje
            message = self.pulse.format_telegram_message(analysis)
            
            # Enviar resultado
            await processing_msg.edit_text(
                message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            await processing_msg.edit_text(
                f"❌ Error al analizar {symbol}: {str(e)}\n\nIntenta nuevamente en unos minutos."
            )
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar botones inline"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith('pulse_'):
            symbol = data.split('_')[1]
            
            await query.message.reply_text(
                f"📊 Analizando {symbol}...\n⏳ Esto puede tomar 30-60 segundos..."
            )
            
            try:
                analysis = await self.pulse.analyze_crypto_sentiment(symbol)
                await self.save_analysis(analysis, query.message.chat_id)
                
                message = self.pulse.format_telegram_message(analysis)
                await query.message.reply_text(
                    message,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                await query.message.reply_text(f"❌ Error: {str(e)}")
        
        elif data == 'pulse_config':
            await self.show_config(query)
        
        elif data == 'pulse_trending':
            await self.show_trending(query)
    
    async def trending_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /trending - Mostrar cryptos trending"""
        await update.message.reply_text(
            "📈 *Cryptos Trending*\n\nAnalizando las cryptos más populares...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Analizar múltiples cryptos populares
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA']
        
        results = []
        for symbol in symbols:
            try:
                analysis = await self.pulse.analyze_crypto_sentiment(symbol)
                results.append(analysis)
            except:
                pass
        
        if results:
            message = "📈 *Top Cryptos - Sentiment Analysis*\n\n"
            
            for analysis in results:
                emoji = '🟢' if analysis['overall_sentiment'] > 20 else '🟡' if analysis['overall_sentiment'] > -20 else '🔴'
                message += f"{emoji} *{analysis['symbol']}*: {analysis['overall_sentiment']:+d}/100 - {analysis['recommendation']}\n"
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def track_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /track <SYMBOL> - Trackear símbolo"""
        if not context.args:
            await update.message.reply_text(
                "Por favor especifica un símbolo: `/track BTC`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbol = context.args[0].upper()
        chat_id = update.effective_chat.id
        
        # Agregar símbolo a tracked_symbols
        await self.db.pulse_subscriptions.update_one(
            {'telegram_chat_id': chat_id},
            {
                '$addToSet': {'tracked_symbols': symbol},
                '$set': {'updated_at': asyncio.get_event_loop().time()}
            },
            upsert=True
        )
        
        await update.message.reply_text(
            f"✅ Ahora estás trackeando *{symbol}*\n\nRecibirás alertas cuando haya cambios significativos en el sentimiento.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def config_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /config - Mostrar configuración"""
        chat_id = update.effective_chat.id
        
        # Obtener configuración actual
        subscription = await self.db.pulse_subscriptions.find_one({'telegram_chat_id': chat_id})
        
        if subscription:
            tracked = subscription.get('tracked_symbols', [])
            notifications = subscription.get('notifications_enabled', True)
        else:
            tracked = []
            notifications = True
        
        keyboard = [
            [InlineKeyboardButton(
                f"🔔 Notificaciones: {'ON' if notifications else 'OFF'}",
                callback_data='toggle_notif'
            )],
            [InlineKeyboardButton("📊 Ver Tracked Symbols", callback_data='show_tracked')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_main')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        config_text = f"""⚙️ *Configuración Pulse IA*

*Símbolos Trackeados:* {len(tracked)}
{', '.join(tracked) if tracked else 'Ninguno'}

*Notificaciones:* {'Activadas ✅' if notifications else 'Desactivadas ❌'}

Usa `/track <SYMBOL>` para agregar símbolos.
        """
        
        await update.message.reply_text(
            config_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """📚 *Ayuda - Pulse IA*

*Comandos Principales:*
/pulse <SYMBOL> - Analizar sentimiento de una crypto
  Ejemplo: `/pulse BTC`

/trending - Ver cryptos más populares

/track <SYMBOL> - Trackear símbolo para alertas
  Ejemplo: `/track ETH`

/config - Ver y modificar configuración

/help - Mostrar esta ayuda

*¿Qué analizamos?*
• 15+ fuentes de noticias RSS
• Twitter/X (300+ cuentas crypto)
• Reddit (5 subreddits principales)
• Análisis con IA (FinBERT)

*Métricas:*
• Sentiment Score (-100 a +100)
• FOMO/FUD Detection
• Trending Keywords
• Recommendation (Bullish/Bearish/Neutral)

¿Preguntas? Escribe a @GuaraniAppStore
        """
        
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def show_config(self, query):
        """Mostrar configuración (desde callback)"""
        keyboard = [
            [InlineKeyboardButton("🔔 Toggle Notificaciones", callback_data='toggle_notif')],
            [InlineKeyboardButton("📊 Ver Tracked", callback_data='show_tracked')],
            [InlineKeyboardButton("🔙 Volver", callback_data='back_main')]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.edit_text(
            "⚙️ *Configuración*\n\nAjusta tus preferencias:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def show_trending(self, query):
        """Mostrar trending (desde callback)"""
        await query.message.edit_text("📈 Analizando cryptos trending...")
        
        symbols = ['BTC', 'ETH', 'BNB']
        results = []
        
        for symbol in symbols:
            try:
                analysis = await self.pulse.analyze_crypto_sentiment(symbol)
                results.append(analysis)
            except:
                pass
        
        if results:
            message = "📈 *Top Cryptos*\n\n"
            for analysis in results:
                emoji = '🟢' if analysis['overall_sentiment'] > 20 else '🟡'
                message += f"{emoji} {analysis['symbol']}: {analysis['overall_sentiment']:+d}/100\n"
            
            await query.message.edit_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def register_user(self, chat_id, username):
        """Registrar usuario en base de datos"""
        await self.db.pulse_subscriptions.update_one(
            {'telegram_chat_id': chat_id},
            {
                '$set': {
                    'telegram_username': username,
                    'status': 'active'
                },
                '$setOnInsert': {
                    'tracked_symbols': ['BTC', 'ETH'],
                    'notifications_enabled': True,
                    'created_at': asyncio.get_event_loop().time()
                }
            },
            upsert=True
        )
    
    async def save_analysis(self, analysis, chat_id):
        """Guardar análisis en base de datos"""
        await self.db.pulse_sentiment_analysis.insert_one({
            **analysis,
            'requested_by_chat_id': chat_id
        })
    
    async def run(self):
        """Iniciar bot"""
        if not BOT_TOKEN:
            print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado")
            print("   Configura la variable de entorno TELEGRAM_BOT_TOKEN")
            return
        
        print("🤖 Inicializando Pulse IA Bot...")
        
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Comandos
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("pulse", self.pulse_command))
        app.add_handler(CommandHandler("trending", self.trending_command))
        app.add_handler(CommandHandler("track", self.track_command))
        app.add_handler(CommandHandler("config", self.config_command))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # Callbacks
        app.add_handler(CallbackQueryHandler(self.callback_handler))
        
        print("✅ Pulse IA Bot iniciado!")
        print(f"   Token: {BOT_TOKEN[:10]}...")
        
        await app.run_polling()

async def main():
    bot = PulseTelegramBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
