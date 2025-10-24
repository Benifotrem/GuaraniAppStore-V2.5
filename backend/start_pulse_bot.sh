#!/bin/bash
# Script para iniciar el bot de Telegram de Pulse IA

echo "🤖 Iniciando Pulse IA Telegram Bot..."

# Cargar variables de entorno
export $(cat /app/backend/.env | xargs)

# Iniciar bot
cd /app/backend
python3 pulse_telegram_bot.py
