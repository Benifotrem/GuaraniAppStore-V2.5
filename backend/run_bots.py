#!/usr/bin/env python3
"""
Script to run Telegram Bots
Usage: python run_bots.py [bot_name]
       python run_bots.py all

Available bots:
- cryptoshield: CryptoShield IA Bot
- pulse: Pulse IA Bot
- momentum: Momentum Predictor IA Bot
- agente_ventas: Agente Ventas IA Bot
- asistente: Asistente Directivos Bot
- all: Run all bots
"""
import sys
import os
from bot_manager import start_bot, start_all_bots, stop_all_bots, signal_handler
import signal

# Available bots mapping
BOTS = {
    'cryptoshield': ('CryptoShield IA', 'cryptoshield'),
    'pulse': ('Pulse IA', 'pulse'),
    'momentum': ('Momentum Predictor IA', 'momentum'),
    'agente_ventas': ('Agente Ventas IA', 'agente_ventas'),
    'asistente': ('Asistente Directivos', 'asistente')
}


def show_help():
    """Show help message"""
    print(__doc__)
    print("\nExamples:")
    print("  python run_bots.py cryptoshield")
    print("  python run_bots.py all")


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    bot_arg = sys.argv[1].lower()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if bot_arg == 'all':
        print("🚀 Starting all Telegram bots...")
        from bot_manager import main as run_manager
        run_manager()
    elif bot_arg in BOTS:
        bot_name, bot_module = BOTS[bot_arg]
        print(f"🚀 Starting {bot_name}...")
        start_bot(bot_name, bot_module)
        
        # Keep running
        print(f"✅ {bot_name} is running. Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n⏹️ Stopping {bot_name}...")
    elif bot_arg in ['help', '-h', '--help']:
        show_help()
    else:
        print(f"❌ Unknown bot: {bot_arg}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
