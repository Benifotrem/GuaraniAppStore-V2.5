"""
Bot de Telegram para Momentum Predictor
Señales de trading con LSTM
"""
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
from motor.motor_asyncio import AsyncIOMotorClient

from momentum_service import MomentumPredictorService

# Cargar variables de entorno
load_dotenv()

# Configuración
BOT_TOKEN = os.environ.get('MOMENTUM_BOT_TOKEN', os.environ.get('TELEGRAM_BOT_TOKEN'))
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')

# Servicio
momentum_service = None

class MomentumTelegramBot:
    def __init__(self):
        self.db_client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.db_client.get_database()
        global momentum_service
        if momentum_service is None:
            momentum_service = MomentumPredictorService(use_mock=True)
        self.momentum = momentum_service
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Registrar usuario
        await self.register_user(chat_id, user.username)
        
        keyboard = [
            [
                InlineKeyboardButton("🎯 BTC Signal", callback_data='momentum_BTC'),
                InlineKeyboardButton("🎯 ETH Signal", callback_data='momentum_ETH')
            ],
            [
                InlineKeyboardButton("📊 My Signals", callback_data='momentum_history'),
                InlineKeyboardButton("❓ Help", callback_data='momentum_help')
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        mock_notice = "\n⚠️ *Actualmente en modo MOCK* (modelo no entrenado)\n" if self.momentum.use_mock else ""
        
        welcome_text = f"""🎯 *¡Bienvenido a Momentum Predictor!*

Hola {user.first_name}, soy tu asistente de señales de trading con IA.
{mock_notice}
*¿Qué puedo hacer?*
• Predecir señales BUY/SELL/HOLD
• Proporcionar niveles de entrada/salida
• Calcular stop loss y targets
• Evaluar nivel de riesgo

*Comandos disponibles:*
/signal <SYMBOL> - Obtener señal
/history - Ver mis señales
/stats <SYMBOL> - Estadísticas
/help - Ayuda

¡Selecciona una opción para empezar! 👇
        """
        
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def signal_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /signal <SYMBOL>"""
        symbol = context.args[0].upper() if context.args else 'BTC'
        
        processing_msg = await update.message.reply_text(
            f"🎯 Generando señal para {symbol}...\n⏳ Analizando 60 días de datos..."
        )
        
        try:
            # Generar señal
            prediction = self.momentum.predict_signal(symbol)
            
            # Guardar en base de datos
            await self.save_signal(prediction, update.effective_chat.id)
            
            # Formatear mensaje
            message = self.momentum.format_telegram_message(prediction)
            
            # Enviar señal
            await processing_msg.edit_text(
                message,
                parse_mode=ParseMode.MARKDOWN
            )
            
        except Exception as e:
            await processing_msg.edit_text(
                f"❌ Error al generar señal para {symbol}: {str(e)}"
            )
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /history - Ver señales anteriores"""
        chat_id = update.effective_chat.id
        
        # Obtener últimas 5 señales del usuario
        signals = await self.db.momentum_signals.find(
            {'requested_by_chat_id': chat_id}
        ).sort('predicted_at', -1).limit(5).to_list(length=5)
        
        if not signals:
            await update.message.reply_text(
                "📊 No tienes señales previas.\n\nUsa `/signal BTC` para obtener tu primera señal.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        message = "📊 *Tus Últimas Señales*\n\n"
        
        for sig in signals:
            emoji = '🟢' if sig['signal'] == 'BUY' else '🔴' if sig['signal'] == 'SELL' else '🟡'
            message += f"{emoji} *{sig['symbol']}*: {sig['signal']} ({sig['confidence']:.0f}%) - ${sig['current_price']:.2f}\n"
            message += f"   _{sig['predicted_at'][:10]}_\n\n"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats <SYMBOL>"""
        if not context.args:
            await update.message.reply_text(
                "Por favor especifica un símbolo: `/stats BTC`",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        symbol = context.args[0].upper()
        
        # Obtener estadísticas
        total = await self.db.momentum_signals.count_documents({'symbol': symbol})
        
        if total == 0:
            await update.message.reply_text(
                f"📊 No hay señales registradas para *{symbol}*",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        buy_count = await self.db.momentum_signals.count_documents({'symbol': symbol, 'signal': 'BUY'})
        sell_count = await self.db.momentum_signals.count_documents({'symbol': symbol, 'signal': 'SELL'})
        hold_count = await self.db.momentum_signals.count_documents({'symbol': symbol, 'signal': 'HOLD'})
        
        last_signal = await self.db.momentum_signals.find_one(
            {'symbol': symbol},
            sort=[('predicted_at', -1)]
        )
        
        message = f"""📊 *Estadísticas de {symbol}*

*Total Señales:* {total}

*Distribución:*
🟢 BUY: {buy_count} ({buy_count/total*100:.1f}%)
🔴 SELL: {sell_count} ({sell_count/total*100:.1f}%)
🟡 HOLD: {hold_count} ({hold_count/total*100:.1f}%)

*Última Señal:*
{last_signal['signal']} ({last_signal['confidence']:.0f}%)
${last_signal['current_price']:.2f}
_{last_signal['predicted_at'][:10]}_
        """
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_text = """📚 *Ayuda - Momentum Predictor*

*Comandos:*
/signal <SYMBOL> - Obtener señal de trading
  Ejemplo: `/signal BTC`

/history - Ver tus señales anteriores

/stats <SYMBOL> - Ver estadísticas de un símbolo

/help - Mostrar esta ayuda

*Sobre las Señales:*
• *BUY* 🟢: Señal de compra
• *SELL* 🔴: Señal de venta
• *HOLD* 🟡: Mantener posición

*Niveles de Trading:*
• *Entry*: Precio de entrada sugerido
• *Target 1/2*: Objetivos de ganancia
• *Stop Loss*: Límite de pérdida

*Timeframes:*
• Short: 1-3 días
• Mid: 3-7 días
• Long: 7+ días

*Nivel de Riesgo:*
🟢 Low | 🟠 Medium | 🔴 High

⚠️ *Disclaimer:* Las señales son orientativas y no constituyen asesoramiento financiero.
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar botones inline"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith('momentum_'):
            action = data.split('_')[1]
            
            if action in ['BTC', 'ETH', 'BNB', 'SOL']:
                await query.message.reply_text(f"🎯 Generando señal para {action}...")
                
                try:
                    prediction = self.momentum.predict_signal(action)
                    await self.save_signal(prediction, query.message.chat_id)
                    
                    message = self.momentum.format_telegram_message(prediction)
                    await query.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
                except Exception as e:
                    await query.message.reply_text(f"❌ Error: {str(e)}")
            
            elif action == 'history':
                await self.show_history(query)
            
            elif action == 'help':
                await self.help_command(query, None)
    
    async def show_history(self, query):
        """Mostrar historial (desde callback)"""
        chat_id = query.message.chat_id
        
        signals = await self.db.momentum_signals.find(
            {'requested_by_chat_id': chat_id}
        ).sort('predicted_at', -1).limit(5).to_list(length=5)
        
        if not signals:
            await query.message.edit_text("📊 No tienes señales previas.")
            return
        
        message = "📊 *Tus Últimas Señales*\n\n"
        
        for sig in signals:
            emoji = '🟢' if sig['signal'] == 'BUY' else '🔴' if sig['signal'] == 'SELL' else '🟡'
            message += f"{emoji} {sig['symbol']}: {sig['signal']} ({sig['confidence']:.0f}%)\n"
        
        await query.message.edit_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def register_user(self, chat_id, username):
        """Registrar usuario"""
        await self.db.momentum_subscriptions.update_one(
            {'telegram_chat_id': chat_id},
            {
                '$set': {
                    'telegram_username': username,
                    'status': 'active'
                },
                '$setOnInsert': {
                    'tracked_symbols': ['BTC', 'ETH'],
                    'notifications_enabled': True
                }
            },
            upsert=True
        )
    
    async def save_signal(self, prediction, chat_id):
        """Guardar señal"""
        await self.db.momentum_signals.insert_one({
            **prediction,
            'requested_by_chat_id': chat_id
        })
    
    async def run(self):
        """Iniciar bot"""
        if not BOT_TOKEN:
            print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado")
            return
        
        print("🤖 Inicializando Momentum Predictor Bot...")
        
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Comandos
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("signal", self.signal_command))
        app.add_handler(CommandHandler("history", self.history_command))
        app.add_handler(CommandHandler("stats", self.stats_command))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # Callbacks
        app.add_handler(CallbackQueryHandler(self.callback_handler))
        
        print("✅ Momentum Predictor Bot iniciado!")
        
        await app.run_polling()

async def main():
    bot = MomentumTelegramBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
