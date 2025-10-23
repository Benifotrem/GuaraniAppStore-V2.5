"""
GuaraniAppStore V2.5 Pro - Sistema de Webhooks para Telegram Bots
Gestiona webhooks para los 5 bots de Telegram de forma eficiente y escalable
"""

import os
import logging
import asyncio
import hmac
import hashlib
from typing import Dict, Any, Optional
import httpx
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Configuración de bots
TELEGRAM_BOTS = {
    'asistente': {
        'token': os.environ.get('GUARANI_ASSISTANT_BOT_TOKEN'),
        'username': '@GuaraniAssistantBot',
        'name': 'GuaraniAppStore Assistant',
        'description': 'Asistente ejecutivo 24/7'
    },
    'cryptoshield': {
        'token': os.environ.get('STOPFRAUDE_BOT_TOKEN'),
        'username': '@stopfraudebot',
        'name': 'CryptoShield IA',
        'description': 'Detector de fraudes en criptomonedas'
    },
    'pulse': {
        'token': os.environ.get('PULSEBOT_TOKEN'),
        'username': '@Rojiverdebot',
        'name': 'Pulse IA',
        'description': 'Análisis de sentimiento crypto'
    },
    'momentum': {
        'token': os.environ.get('MOMENTUM_BOT_TOKEN'),
        'username': '@Mejormomentobot',
        'name': 'Momentum Predictor IA',
        'description': 'Señales de trading'
    },
    'rocio': {
        'token': os.environ.get('ROCIO_BOT_TOKEN'),
        'username': '@RocioAlmeidaBot',
        'name': 'Rocío Almeida - Agente Ventas',
        'description': 'Agente de ventas autónomo'
    }
}


class TelegramWebhookManager:
    """Gestor centralizado de webhooks para Telegram bots"""
    
    def __init__(self):
        self.webhook_base_url = os.environ.get('TELEGRAM_WEBHOOK_URL', '')
        self.webhook_secret = os.environ.get('TELEGRAM_WEBHOOK_SECRET', 'guarani_webhook_secret_2025_secure')
        self.bots_config = TELEGRAM_BOTS
        
        if not self.webhook_base_url:
            logger.warning("⚠️ TELEGRAM_WEBHOOK_URL no configurada. Los webhooks no se establecerán.")
            logger.info("💡 Para producción con Cloudflare, configurar: TELEGRAM_WEBHOOK_URL=https://tudominio.com/api/telegram/webhook")
    
    async def setup_webhook(self, bot_id: str) -> Dict[str, Any]:
        """
        Configurar webhook para un bot específico
        
        Args:
            bot_id: ID del bot (asistente, cryptoshield, pulse, momentum, rocio)
        
        Returns:
            Dict con resultado de la configuración
        """
        if bot_id not in self.bots_config:
            return {
                'success': False,
                'error': f'Bot {bot_id} no encontrado'
            }
        
        bot_config = self.bots_config[bot_id]
        token = bot_config['token']
        
        if not token:
            return {
                'success': False,
                'error': f'Token no configurado para bot {bot_id}'
            }
        
        if not self.webhook_base_url:
            return {
                'success': False,
                'error': 'TELEGRAM_WEBHOOK_URL no configurada'
            }
        
        # Construir URL del webhook específica para este bot
        webhook_url = f"{self.webhook_base_url}/{bot_id}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Configurar webhook en Telegram
                response = await client.post(
                    f"https://api.telegram.org/bot{token}/setWebhook",
                    json={
                        'url': webhook_url,
                        'secret_token': self.webhook_secret,
                        'allowed_updates': ['message', 'callback_query', 'inline_query'],
                        'drop_pending_updates': True,
                        'max_connections': 40
                    }
                )
                
                data = response.json()
                
                if data.get('ok'):
                    logger.info(f"✅ Webhook configurado para {bot_config['name']}: {webhook_url}")
                    return {
                        'success': True,
                        'bot_id': bot_id,
                        'bot_name': bot_config['name'],
                        'webhook_url': webhook_url,
                        'message': f"Webhook establecido exitosamente"
                    }
                else:
                    logger.error(f"❌ Error configurando webhook para {bot_id}: {data.get('description')}")
                    return {
                        'success': False,
                        'error': data.get('description', 'Error desconocido')
                    }
        
        except Exception as e:
            logger.error(f"❌ Excepción configurando webhook para {bot_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def setup_all_webhooks(self) -> Dict[str, Any]:
        """Configurar webhooks para todos los bots"""
        results = {}
        
        for bot_id in self.bots_config.keys():
            result = await self.setup_webhook(bot_id)
            results[bot_id] = result
            
            # Pequeña pausa entre configuraciones para evitar rate limits
            await asyncio.sleep(0.5)
        
        successful = sum(1 for r in results.values() if r.get('success'))
        total = len(results)
        
        logger.info(f"📊 Webhooks configurados: {successful}/{total} exitosos")
        
        return {
            'success': successful == total,
            'successful_count': successful,
            'total_count': total,
            'results': results,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def delete_webhook(self, bot_id: str) -> Dict[str, Any]:
        """
        Eliminar webhook de un bot (útil para testing o cambio a polling)
        
        Args:
            bot_id: ID del bot
        """
        if bot_id not in self.bots_config:
            return {
                'success': False,
                'error': f'Bot {bot_id} no encontrado'
            }
        
        bot_config = self.bots_config[bot_id]
        token = bot_config['token']
        
        if not token:
            return {
                'success': False,
                'error': f'Token no configurado para bot {bot_id}'
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{token}/deleteWebhook",
                    json={'drop_pending_updates': True}
                )
                
                data = response.json()
                
                if data.get('ok'):
                    logger.info(f"✅ Webhook eliminado para {bot_config['name']}")
                    return {
                        'success': True,
                        'bot_id': bot_id,
                        'message': 'Webhook eliminado exitosamente'
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('description', 'Error desconocido')
                    }
        
        except Exception as e:
            logger.error(f"❌ Error eliminando webhook para {bot_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_webhook_info(self, bot_id: str) -> Dict[str, Any]:
        """
        Obtener información del webhook configurado
        
        Args:
            bot_id: ID del bot
        """
        if bot_id not in self.bots_config:
            return {
                'success': False,
                'error': f'Bot {bot_id} no encontrado'
            }
        
        bot_config = self.bots_config[bot_id]
        token = bot_config['token']
        
        if not token:
            return {
                'success': False,
                'error': f'Token no configurado para bot {bot_id}'
            }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.telegram.org/bot{token}/getWebhookInfo"
                )
                
                data = response.json()
                
                if data.get('ok'):
                    webhook_info = data.get('result', {})
                    
                    return {
                        'success': True,
                        'bot_id': bot_id,
                        'bot_name': bot_config['name'],
                        'webhook_url': webhook_info.get('url', ''),
                        'has_custom_certificate': webhook_info.get('has_custom_certificate', False),
                        'pending_update_count': webhook_info.get('pending_update_count', 0),
                        'last_error_date': webhook_info.get('last_error_date'),
                        'last_error_message': webhook_info.get('last_error_message'),
                        'max_connections': webhook_info.get('max_connections', 40),
                        'allowed_updates': webhook_info.get('allowed_updates', [])
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('description', 'Error desconocido')
                    }
        
        except Exception as e:
            logger.error(f"❌ Error obteniendo info webhook para {bot_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook_request(self, secret_token: str) -> bool:
        """
        Verificar que la request viene de Telegram
        
        Args:
            secret_token: Token secreto enviado en headers
        """
        return hmac.compare_digest(secret_token, self.webhook_secret)
    
    async def process_update(self, bot_id: str, update: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar update recibido vía webhook
        
        Args:
            bot_id: ID del bot que recibió el update
            update: Objeto Update de Telegram
        
        Returns:
            Respuesta procesada
        """
        try:
            # Extraer información del update
            update_id = update.get('update_id')
            message = update.get('message', {})
            callback_query = update.get('callback_query', {})
            inline_query = update.get('inline_query', {})
            
            # Log del update
            if message:
                user = message.get('from', {})
                text = message.get('text', '')
                logger.info(f"📨 [{bot_id}] Mensaje de {user.get('username', 'unknown')}: {text[:50]}")
            
            elif callback_query:
                user = callback_query.get('from', {})
                data = callback_query.get('data', '')
                logger.info(f"🔘 [{bot_id}] Callback de {user.get('username', 'unknown')}: {data}")
            
            elif inline_query:
                user = inline_query.get('from', {})
                query = inline_query.get('query', '')
                logger.info(f"🔍 [{bot_id}] Inline query de {user.get('username', 'unknown')}: {query}")
            
            # Aquí iría la lógica específica de cada bot
            # Por ahora, solo registramos el update
            
            return {
                'success': True,
                'update_id': update_id,
                'bot_id': bot_id,
                'processed': True,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Error procesando update para {bot_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# Instancia global del webhook manager
webhook_manager = TelegramWebhookManager()
