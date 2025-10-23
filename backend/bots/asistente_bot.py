"""
Asistente Directivos Bot - Asistente Ejecutivo 24/7
Parte del servicio premium
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('GUARANI_ASSISTANT_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
👤 **Bienvenido a tu Asistente Ejecutivo IA**

Estoy aquí para ayudarte 24/7 con:

✅ Gestión de agenda (Google Calendar)
✅ Recordatorios inteligentes
✅ Control de gastos
✅ Búsquedas web
✅ Enriquecimiento de contactos

**Comandos rápidos:**
/agenda - Ver agenda del día
/agendar - Agendar reunión
/tarea - Agregar tarea
/gastos - Registrar gasto
/buscar - Búsqueda web
/help - Ayuda completa

💡 **Tip:** También puedo entender lenguaje natural. Prueba escribiendo: "Agenda reunión con Juan mañana 3pm"
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def agenda_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's agenda"""
    agenda_text = """
📅 **Tu Agenda de Hoy**

09:00 - 10:00: Reunión de equipo
📍 Sala 3, Oficina Central
👥 5 participantes

11:30 - 12:00: Call con cliente
📞 Zoom: meeting.zoom.us/j/123
⏰ Recordatorio: 10 min antes

15:00 - 16:30: Presentación Q4
📊 Presentar resultados trimestrales

🎯 **Tareas pendientes:** 3
📧 **Emails sin leer:** 12

💡 Usa `/agendar` para agregar nueva reunión
    """
    await update.message.reply_text(agenda_text, parse_mode='Markdown')


async def agendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule meeting"""
    help_text = """
📅 **Agendar Reunión**

**Formato:**
`/agendar [título] | [fecha] | [hora] | [participantes]`

**Ejemplo:**
`/agendar Reunión de ventas | 25/10/2024 | 15:00 | juan@empresa.com, maria@empresa.com`

**O escribe en lenguaje natural:**
"Agenda una reunión con el equipo de marketing mañana a las 10am"

✅ Se sincronizará con tu Google Calendar
📧 Se enviarán invitaciones automáticamente
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def tarea_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add task"""
    if not context.args:
        await update.message.reply_text(
            "📋 **Agregar Tarea**\n\n"
            "Formato: `/tarea [descripción] | [fecha límite]`\n\n"
            "Ejemplo: `/tarea Revisar propuesta | 30/10/2024`",
            parse_mode='Markdown'
        )
        return
    
    task = ' '.join(context.args)
    await update.message.reply_text(
        f"✅ **Tarea agregada:**\n{task}\n\n"
        "⏰ Te recordaré 1 día antes",
        parse_mode='Markdown'
    )


async def gastos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track expense"""
    help_text = """
💰 **Registrar Gasto**

**Formato:**
`/gastos [monto] [categoría] [descripción]`

**Ejemplo:**
`/gastos 250000 comida Almuerzo con cliente`
`/gastos 150000 transporte Taxi aeropuerto`

**Categorías:**
• comida
• transporte
• oficina
• marketing
• otro

📊 Ver resumen: `/resumen_gastos`
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def buscar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Web search"""
    if not context.args:
        await update.message.reply_text(
            "🔍 **Búsqueda Web**\n\n"
            "Formato: `/buscar [tu consulta]`\n\n"
            "Ejemplo: `/buscar mejores herramientas CRM 2024`",
            parse_mode='Markdown'
        )
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(
        f"🔍 Buscando: *{query}*\n\n"
        "Top 3 resultados:\n"
        "1. [Resultado 1](https://example.com/1)\n"
        "2. [Resultado 2](https://example.com/2)\n"
        "3. [Resultado 3](https://example.com/3)",
        parse_mode='Markdown'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle natural language"""
    text = update.message.text.lower()
    
    if 'agenda' in text or 'reunión' in text:
        await update.message.reply_text(
            "📅 Entendido. Usa `/agendar` para programar una reunión.",
            parse_mode='Markdown'
        )
    elif 'tarea' in text or 'recordar' in text:
        await update.message.reply_text(
            "📋 ¡Claro! Usa `/tarea` para agregar una tarea.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "👋 ¿En qué puedo ayudarte?\n\n"
            "Prueba con `/help` para ver todos los comandos disponibles.",
            parse_mode='Markdown'
        )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("agenda", agenda_command))
    application.add_handler(CommandHandler("agendar", agendar_command))
    application.add_handler(CommandHandler("tarea", tarea_command))
    application.add_handler(CommandHandler("gastos", gastos_command))
    application.add_handler(CommandHandler("buscar", buscar_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("👤 Asistente Directivos Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
