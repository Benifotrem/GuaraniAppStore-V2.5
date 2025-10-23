#!/usr/bin/env python3
"""
Script de limpieza automática de mensajes de chat antiguos.
Ejecutar diariamente vía cron para mantener la retención de 30 días.

Uso:
    python cleanup_chat_messages.py

Crontab sugerido (ejecutar diariamente a las 2 AM):
    0 2 * * * cd /app/backend && python cleanup_chat_messages.py >> /var/log/chat_cleanup.log 2>&1
"""

import asyncio
import sys
import logging
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, '/app/backend')

from chat_memory_service import chat_memory_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Ejecuta la limpieza de mensajes antiguos"""
    logger.info("=" * 50)
    logger.info("Iniciando limpieza de mensajes de chat antiguos")
    logger.info(f"Fecha: {datetime.now().isoformat()}")
    logger.info("=" * 50)
    
    try:
        # Limpiar mensajes antiguos
        logger.info("Eliminando mensajes con más de 30 días...")
        deleted_messages = await chat_memory_service.cleanup_old_messages()
        logger.info(f"✅ {deleted_messages} mensajes eliminados")
        
        # Marcar sesiones inactivas
        logger.info("Marcando sesiones inactivas...")
        inactive_sessions = await chat_memory_service.cleanup_inactive_sessions(days_inactive=30)
        logger.info(f"✅ {inactive_sessions} sesiones marcadas como inactivas")
        
        logger.info("=" * 50)
        logger.info("Limpieza completada exitosamente")
        logger.info("=" * 50)
        
        return 0
    
    except Exception as e:
        logger.error(f"❌ Error durante la limpieza: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
