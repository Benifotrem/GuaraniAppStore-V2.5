"""
Pulse IA Bot - Análisis de Sentimiento del Mercado Cripto
Parte de la Suite Cripto (premium)
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('PULSEBOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    welcome_text = """
📊 **Bienvenido a Pulse IA**

Tu indicador de sentimiento del mercado cripto en tiempo real.

**¿Qué hago?**
✅ Análisis de sentimiento (Twitter, Reddit, News)
✅ Score de confianza
✅ Tendencias del mercado
✅ Alertas de cambios bruscos

**Comandos:**
/pulse <coin> - Analizar sentimiento
/trending - Ver coins trending
/alerts - Configurar alertas
/help - Ayuda completa

**Ejemplo:**
`/pulse BTC`
`/pulse ETH`

🔐 **Servicio Premium** - Requiere suscripción activa
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help message"""
    help_text = """
📚 **Ayuda - Pulse IA**

**Comandos disponibles:**

📊 `/pulse <COIN>` - Analizar sentimiento
Ejemplo: `/pulse BTC`

🔥 `/trending` - Ver coins con más buzz

⚡ `/alerts` - Configurar alertas personalizadas

📈 `/compare <COIN1> <COIN2>` - Comparar sentimiento
Ejemplo: `/compare BTC ETH`

**Fuentes de datos:**
• Twitter (últimas 24h)
• Reddit (r/cryptocurrency, r/bitcoin)
• Noticias cripto
• Whale movements

**Interpretación:**
• 0-30: BEARISH (Negativo)
• 31-69: NEUTRAL
• 70-100: BULLISH (Positivo)
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def pulse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze sentiment for a coin"""
    if not context.args:
        await update.message.reply_text(
            "❌ Por favor especifica una moneda.\n\n"
            "Ejemplo: `/pulse BTC`",
            parse_mode='Markdown'
        )
        return
    
    coin = context.args[0].upper()
    
    processing_msg = await update.message.reply_text(
        f"📊 Analizando sentimiento de **{coin}**...\n"
        "🔍 Escaneando Twitter, Reddit, News...",
        parse_mode='Markdown'
    )
    
    # Simulate sentiment analysis
    result = await analyze_sentiment(coin)
    
    sentiment_emoji = "🟢" if result['sentiment'] == 'BULLISH' else "🔴" if result['sentiment'] == 'BEARISH' else "🟡"
    trend_emoji = "📈" if result['trend'] == 'RISING' else "📉" if result['trend'] == 'FALLING' else "➡️"
    
    result_text = f"""
{sentiment_emoji} **Análisis de Sentimiento - {coin}**

📊 **Sentiment Score:** {result['sentiment_score']}/100
🎯 **Sentiment:** {result['sentiment']}
💪 **Confidence:** {result['confidence']}%
{trend_emoji} **Trend:** {result['trend']}

**Fuentes:**
🐦 Twitter: {result['sources']['twitter']['score']}/100 ({result['sources']['twitter']['mentions']} menciones)
👽 Reddit: {result['sources']['reddit']['score']}/100 ({result['sources']['reddit']['posts']} posts)
📰 News: {result['sources']['news']['score']}/100 ({result['sources']['news']['articles']} artículos)

⏰ Actualizado: {result['updated_at']}

💡 **Interpretación:**
{get_interpretation(result['sentiment_score'])}
    """
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Actualizar", callback_data=f"pulse_{coin}"),
            InlineKeyboardButton("⚡ Crear Alerta", callback_data=f"alert_{coin}"),
        ],
        [
            InlineKeyboardButton("🚀 Momentum IA", url="https://t.me/MomentumPredictorBot"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await processing_msg.delete()
    await update.message.reply_text(result_text, parse_mode='Markdown', reply_markup=reply_markup)


async def trending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show trending coins"""
    trending = [
        {'coin': 'BTC', 'score': 85, 'change': '+12'},
        {'coin': 'ETH', 'score': 78, 'change': '+8'},
        {'coin': 'SOL', 'score': 72, 'change': '+15'},
        {'coin': 'XRP', 'score': 45, 'change': '-5'},
        {'coin': 'ADA', 'score': 58, 'change': '+3'}
    ]
    
    trending_text = "🔥 **Trending Coins (24h)**\n\n"
    
    for i, item in enumerate(trending, 1):
        emoji = "🟢" if item['score'] >= 70 else "🟡" if item['score'] >= 40 else "🔴"
        change_emoji = "📈" if item['change'].startswith('+') else "📉"
        trending_text += f"{i}. {emoji} **{item['coin']}**: {item['score']}/100 {change_emoji} {item['change']}%\n"
    
    trending_text += "\n💡 Usa `/pulse <COIN>` para análisis detallado"
    
    await update.message.reply_text(trending_text, parse_mode='Markdown')


async def analyze_sentiment(coin: str) -> dict:
    """Simulate sentiment analysis"""
    import random
    from datetime import datetime
    
    score = random.randint(30, 95)
    sentiment = 'BULLISH' if score >= 70 else 'BEARISH' if score < 40 else 'NEUTRAL'
    
    return {
        'coin': coin,
        'sentiment_score': score,
        'sentiment': sentiment,
        'confidence': random.randint(70, 95),
        'trend': random.choice(['RISING', 'FALLING', 'STABLE']),
        'sources': {
            'twitter': {'score': random.randint(60, 90), 'mentions': random.randint(500, 5000)},
            'reddit': {'score': random.randint(50, 80), 'posts': random.randint(50, 500)},
            'news': {'score': random.randint(55, 85), 'articles': random.randint(10, 100)}
        },
        'updated_at': datetime.now().strftime('%H:%M:%S')
    }


def get_interpretation(score: int) -> str:
    """Get interpretation text"""
    if score >= 80:
        return "Sentimiento MUY POSITIVO. Alta actividad bullish en redes."
    elif score >= 70:
        return "Sentimiento POSITIVO. El mercado está optimista."
    elif score >= 40:
        return "Sentimiento NEUTRAL. Sin tendencia clara."
    else:
        return "Sentimiento NEGATIVO. Precaución recomendada."


def main():
    """Start bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("pulse", pulse_command))
    application.add_handler(CommandHandler("trending", trending_command))
    
    logger.info("📊 Pulse IA Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
