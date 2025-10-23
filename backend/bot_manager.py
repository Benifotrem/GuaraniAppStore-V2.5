"""
Bot Manager - Gestión centralizada de Telegram Bots
Permite iniciar/detener los bots de forma controlada
"""
import os
import asyncio
import logging
from multiprocessing import Process
import signal
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot processes
bot_processes = {}


def run_bot(bot_name, bot_module):
    """Run a specific bot in a separate process"""
    try:
        logger.info(f"🚀 Starting {bot_name}...")
        
        # Import and run the bot
        if bot_module == 'cryptoshield':
            from bots.cryptoshield_bot import main
        elif bot_module == 'pulse':
            from bots.pulse_bot import main
        elif bot_module == 'momentum':
            from bots.momentum_bot import main
        elif bot_module == 'agente_ventas':
            from bots.agente_ventas_bot import main
        elif bot_module == 'asistente':
            from bots.asistente_bot import main
        else:
            logger.error(f"❌ Unknown bot module: {bot_module}")
            return
        
        # Run the bot
        main()
        
    except KeyboardInterrupt:
        logger.info(f"⏹️ {bot_name} stopped by user")
    except Exception as e:
        logger.error(f"❌ Error in {bot_name}: {e}")


def start_bot(bot_name, bot_module):
    """Start a bot in a separate process"""
    if bot_name in bot_processes and bot_processes[bot_name].is_alive():
        logger.warning(f"⚠️ {bot_name} is already running")
        return False
    
    process = Process(target=run_bot, args=(bot_name, bot_module), daemon=True)
    process.start()
    bot_processes[bot_name] = process
    logger.info(f"✅ {bot_name} started (PID: {process.pid})")
    return True


def stop_bot(bot_name):
    """Stop a specific bot"""
    if bot_name not in bot_processes:
        logger.warning(f"⚠️ {bot_name} is not running")
        return False
    
    process = bot_processes[bot_name]
    if process.is_alive():
        process.terminate()
        process.join(timeout=5)
        if process.is_alive():
            process.kill()
        logger.info(f"⏹️ {bot_name} stopped")
        del bot_processes[bot_name]
        return True
    else:
        logger.warning(f"⚠️ {bot_name} process is not alive")
        del bot_processes[bot_name]
        return False


def start_all_bots():
    """Start all configured bots"""
    bots = [
        ("CryptoShield IA", "cryptoshield"),
        ("Pulse IA", "pulse"),
        ("Momentum Predictor IA", "momentum"),
        ("Agente Ventas IA", "agente_ventas"),
        ("Asistente Directivos", "asistente")
    ]
    
    logger.info("🚀 Starting all Telegram Bots...")
    
    for bot_name, bot_module in bots:
        # Check if token is configured
        token_var = None
        if bot_module == 'cryptoshield':
            token_var = 'STOPFRAUDE_BOT_TOKEN'
        elif bot_module == 'pulse':
            token_var = 'PULSEBOT_TOKEN'
        elif bot_module == 'momentum':
            token_var = 'MOMENTUM_BOT_TOKEN'
        elif bot_module == 'agente_ventas':
            token_var = 'ROCIO_BOT_TOKEN'
        elif bot_module == 'asistente':
            token_var = 'GUARANI_ASSISTANT_BOT_TOKEN'
        
        token = os.getenv(token_var)
        if not token or token.startswith('your_') or token == 'YOUR_BOT_TOKEN_HERE':
            logger.warning(f"⚠️ Skipping {bot_name} - No valid token configured ({token_var})")
            continue
        
        start_bot(bot_name, bot_module)
    
    logger.info(f"✅ Bot Manager: {len(bot_processes)} bots started")


def stop_all_bots():
    """Stop all running bots"""
    logger.info("⏹️ Stopping all bots...")
    for bot_name in list(bot_processes.keys()):
        stop_bot(bot_name)
    logger.info("✅ All bots stopped")


def get_bot_status():
    """Get status of all bots"""
    status = {}
    for bot_name, process in bot_processes.items():
        status[bot_name] = {
            'running': process.is_alive(),
            'pid': process.pid if process.is_alive() else None
        }
    return status


def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("\n🛑 Shutting down Bot Manager...")
    stop_all_bots()
    sys.exit(0)


def main():
    """Main function to run bot manager"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("=" * 60)
    logger.info("🤖 GuaraniAppStore Bot Manager v1.0")
    logger.info("=" * 60)
    
    # Start all bots
    start_all_bots()
    
    # Keep the main process running
    logger.info("✅ Bot Manager is running. Press Ctrl+C to stop.")
    logger.info("=" * 60)
    
    try:
        while True:
            # Check bot health every 60 seconds
            asyncio.run(asyncio.sleep(60))
            
            # Check if any bot has died
            for bot_name, process in list(bot_processes.items()):
                if not process.is_alive():
                    logger.warning(f"⚠️ {bot_name} has stopped unexpectedly")
                    del bot_processes[bot_name]
    
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down...")
        stop_all_bots()


if __name__ == '__main__':
    main()
