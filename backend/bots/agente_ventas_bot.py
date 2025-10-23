"""
Agente Ventas IA Bot - Agente de ventas conversacional
Base vectorizada de productos + Cualificación automática
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('ROCIO_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Simulación de base vectorizada de productos
PRODUCTS_DB = [
    {'name': 'Laptop HP ProBook', 'price': 4500000, 'category': 'Electrónica'},
    {'name': 'Mouse Logitech MX', 'price': 350000, 'category': 'Accesorios'},
    {'name': 'Teclado Mecánico RGB', 'price': 650000, 'category': 'Accesorios'},
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
👋 **Hola! Soy tu Agente de Ventas IA**

Estoy aquí para ayudarte a encontrar el producto perfecto.

**¿Qué puedo hacer?**
✅ Buscar productos en catálogo (200+)
✅ Responder preguntas
✅ Enviar fotos y detalles
✅ Procesar pedidos

**Comandos:**
/catalogo - Ver catálogo completo
/buscar - Buscar producto
/pedido - Hacer un pedido
/ayuda - Más información

💡 **O simplemente escríbeme lo que buscas:**
"Busco una laptop para diseño gráfico"
"Cuánto cuesta el mouse Logitech?"
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def catalogo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product catalog"""
    catalog_text = "📋 **Catálogo de Productos**\n\n"
    
    for i, product in enumerate(PRODUCTS_DB, 1):
        catalog_text += f"{i}. **{product['name']}**\n"
        catalog_text += f"   💵 Gs. {product['price']:,}\n"
        catalog_text += f"   🏷️ {product['category']}\n\n"
    
    catalog_text += "🔍 Usa `/buscar [producto]` para más detalles"
    
    await update.message.reply_text(catalog_text, parse_mode='Markdown')


async def buscar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search products"""
    if not context.args:
        await update.message.reply_text(
            "🔍 **Buscar Producto**\n\n"
            "Formato: `/buscar [nombre]`\n\n"
            "Ejemplo: `/buscar laptop`",
            parse_mode='Markdown'
        )
        return
    
    query = ' '.join(context.args).lower()
    results = [p for p in PRODUCTS_DB if query in p['name'].lower()]
    
    if results:
        result_text = f"🎯 **Encontré {len(results)} producto(s):**\n\n"
        for product in results:
            result_text += f"**{product['name']}**\n"
            result_text += f"💵 Gs. {product['price']:,}\n"
            result_text += f"📷 [Ver foto] 📦 En stock\n\n"
        result_text += "💬 ¿Te interesa alguno? Escríbeme para más detalles."
    else:
        result_text = "❌ No encontré productos con ese nombre.\n\nIntenta con otra búsqueda o usa `/catalogo`"
    
    await update.message.reply_text(result_text, parse_mode='Markdown')


async def pedido_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Make order"""
    order_text = """
📦 **Hacer un Pedido**

¡Perfecto! Para procesar tu pedido necesito:

1️⃣ Producto(s) que deseas
2️⃣ Cantidad
3️⃣ Dirección de entrega
4️⃣ Forma de pago

💬 Escríbeme toda la información y procesaré tu pedido.

**Ejemplo:**
"Quiero 2 laptops HP ProBook, envío a Asunción, pago con tarjeta"
    """
    await update.message.reply_text(order_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversational messages"""
    text = update.message.text.lower()
    
    # Simulate AI conversation
    if 'precio' in text or 'costo' in text or 'cuánto' in text:
        await update.message.reply_text(
            "💰 Los precios varían según el producto.\n\n"
            "Usa `/catalogo` para ver todos los precios o `/buscar` para un producto específico."
        )
    elif 'comprar' in text or 'pedido' in text:
        await update.message.reply_text(
            "📦 ¡Excelente! Usa `/pedido` para procesar tu compra."
        )
    elif 'gracias' in text:
        await update.message.reply_text(
            "😊 ¡De nada! ¿Hay algo más en lo que pueda ayudarte?"
        )
    else:
        # Generic AI response
        await update.message.reply_text(
            f"🤔 Interesante... \"{text[:50]}...\"\n\n"
            "💡 Puedo ayudarte con:\n"
            "• Ver catálogo: `/catalogo`\n"
            "• Buscar productos: `/buscar`\n"
            "• Hacer pedido: `/pedido`\n\n"
            "¿Qué te gustaría hacer?"
        )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("catalogo", catalogo_command))
    application.add_handler(CommandHandler("buscar", buscar_command))
    application.add_handler(CommandHandler("pedido", pedido_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("👋 Agente Ventas IA Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
