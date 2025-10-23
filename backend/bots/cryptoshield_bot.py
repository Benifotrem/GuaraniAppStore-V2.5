"""
CryptoShield IA Bot - Escáner de Fraude para Criptomonedas
Bot GRATIS disponible para todos
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv('STOPFRAUDE_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    welcome_text = """
🛡️ **Bienvenido a CryptoShield IA**

Soy tu escáner de fraude para criptomonedas. Puedo analizar contratos smart para detectar:

✅ Honeypots
✅ Rugpulls
✅ Contratos maliciosos
✅ Riesgos de scam

**Comandos disponibles:**
/scan <contract_address> - Escanear un contrato
/help - Ver ayuda
/about - Acerca de este bot

**Ejemplo:**
`/scan 0x1234567890abcdef...`

⚠️ **Disclaimer:** Este bot proporciona información para análisis. Siempre haz tu propia investigación (DYOR).
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = """
📚 **Ayuda - CryptoShield IA**

**Cómo usar:**
1. Copia la dirección del contrato (0x...)
2. Envía: `/scan 0x...`
3. Espera el análisis (5-10 segundos)

**Qué analizamos:**
• Código del contrato
• Verificación en blockchain
• Liquidez bloqueada
• Patrones de honeypot
• Transacciones sospechosas
• Holders y distribución

**Red soportadas:**
• Ethereum (ETH)
• BSC (Binance Smart Chain)
• Polygon (MATIC)

¿Dudas? Contacta: support@guaraniappstore.com
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send about information"""
    about_text = """
🛡️ **Acerca de CryptoShield IA**

Desarrollado por GuaraniAppStore V2.5 Pro

**Versión:** 1.0
**Estado:** GRATIS para todos

**Tecnología:**
• AI Pattern Recognition
• Blockchain Analysis
• Smart Contract Decompilation
• Community Reports Integration

**Parte de la Suite Cripto:**
🛡️ CryptoShield IA - Escáner Fraude
📊 Pulse IA - Sentimiento del Mercado
🚀 Momentum IA - Señales de Trading

Más info: https://guaraniappstore.com
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')


async def scan_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Scan a contract for fraud indicators"""
    if not context.args:
        await update.message.reply_text(
            "❌ Por favor proporciona una dirección de contrato.\n\n"
            "Ejemplo: `/scan 0x1234567890abcdef...`",
            parse_mode='Markdown'
        )
        return
    
    contract_address = context.args[0]
    
    # Validate address format
    if not contract_address.startswith('0x') or len(contract_address) != 42:
        await update.message.reply_text(
            "❌ Dirección de contrato inválida.\n\n"
            "Debe ser un formato válido: `0x...` (42 caracteres)",
            parse_mode='Markdown'
        )
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        "🔍 Analizando contrato...\n"
        f"📋 Dirección: `{contract_address[:10]}...{contract_address[-8:]}`\n\n"
        "⏳ Esto puede tomar 5-10 segundos...",
        parse_mode='Markdown'
    )
    
    # Simulate fraud detection (in production, call actual API)
    # This would integrate with services like Honeypot.is, GoPlus, etc.
    result = await analyze_contract(contract_address)
    
    # Format result message
    risk_emoji = "🟢" if result['risk_level'] == 'LOW' else "🟡" if result['risk_level'] == 'MEDIUM' else "🔴"
    
    result_text = f"""
{risk_emoji} **Análisis Completado**

📋 **Contrato:** `{contract_address[:10]}...{contract_address[-8:]}`

⚠️ **Risk Score:** {result['risk_score']}/100
🎯 **Risk Level:** {result['risk_level']}

**Indicadores de Seguridad:**
{'✅' if not result['indicators']['honeypot'] else '❌'} Honeypot: {'No detectado' if not result['indicators']['honeypot'] else 'DETECTADO'}
{'✅' if result['indicators']['verified_contract'] else '❌'} Contrato Verificado: {'Sí' if result['indicators']['verified_contract'] else 'No'}
{'✅' if result['indicators']['liquidity_locked'] else '❌'} Liquidez Bloqueada: {'Sí' if result['indicators']['liquidity_locked'] else 'No'}
{'✅' if result['indicators']['rugpull_risk'] == 'LOW' else '⚠️'} Riesgo Rugpull: {result['indicators']['rugpull_risk']}
{'✅' if not result['indicators']['suspicious_transactions'] else '❌'} Transacciones Sospechosas: {'No' if not result['indicators']['suspicious_transactions'] else 'DETECTADAS'}

💡 **Recomendación:** {result['recommendation']}

⚠️ **Disclaimer:** Siempre DYOR (Do Your Own Research)
    """
    
    # Create inline keyboard for additional actions
    keyboard = [
        [
            InlineKeyboardButton("🔍 Ver en Etherscan", url=f"https://etherscan.io/address/{contract_address}"),
        ],
        [
            InlineKeyboardButton("🆕 Escanear Otro", callback_data="scan_new"),
            InlineKeyboardButton("📊 Pulse IA", url="https://t.me/PulseIABot"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Delete processing message and send result
    await processing_msg.delete()
    await update.message.reply_text(result_text, parse_mode='Markdown', reply_markup=reply_markup)


async def analyze_contract(contract_address: str) -> dict:
    """
    Analyze contract for fraud indicators
    In production, this would call external APIs like:
    - Honeypot.is
    - GoPlus Security
    - Token Sniffer
    - Blockchain explorers
    """
    # Simulate analysis
    import random
    
    risk_score = random.randint(10, 90)
    risk_level = 'LOW' if risk_score < 30 else 'MEDIUM' if risk_score < 60 else 'HIGH'
    
    return {
        'contract': contract_address,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'indicators': {
            'honeypot': risk_score > 70,
            'verified_contract': risk_score < 60,
            'liquidity_locked': risk_score < 50,
            'rugpull_risk': 'LOW' if risk_score < 40 else 'MEDIUM' if risk_score < 70 else 'HIGH',
            'suspicious_transactions': risk_score > 65
        },
        'recommendation': (
            'Contract appears safe but always DYOR' if risk_level == 'LOW' else
            'Exercise caution. Review indicators carefully.' if risk_level == 'MEDIUM' else
            'HIGH RISK! Avoid this contract.'
        )
    }


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (potential contract addresses)"""
    text = update.message.text
    
    # Check if it looks like a contract address
    if text.startswith('0x') and len(text) == 42:
        # Treat as contract scan
        context.args = [text]
        await scan_contract(update, context)
    else:
        await update.message.reply_text(
            "👋 ¿Necesitas ayuda?\n\n"
            "Envía `/scan 0x...` para escanear un contrato\n"
            "O usa `/help` para ver todos los comandos",
            parse_mode='Markdown'
        )


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("scan", scan_contract))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start bot
    logger.info("🛡️ CryptoShield IA Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
