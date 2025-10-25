"""
Model Watcher - Verificación de Modelos OpenRouter
Monitorea la disponibilidad y estado de los modelos configurados
"""
import os
import time
import httpx
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "3600"))  # Default: 1 hora
MODELS_TO_CHECK = [
    os.getenv("OPENROUTER_MODEL_ID_HIGH", "anthropic/claude-sonnet-4.5"),
    os.getenv("OPENROUTER_MODEL_ID_LOW", "openai/gpt-4o-mini")
]

async def check_model_availability(model_id: str) -> dict:
    """Verifica la disponibilidad de un modelo"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Obtener lista de modelos disponibles
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers
            )
            
            if response.status_code == 200:
                models = response.json().get("data", [])
                model_info = next((m for m in models if m["id"] == model_id), None)
                
                if model_info:
                    return {
                        "model_id": model_id,
                        "available": True,
                        "status": "operational",
                        "context_length": model_info.get("context_length"),
                        "pricing": model_info.get("pricing"),
                        "checked_at": datetime.utcnow().isoformat()
                    }
                else:
                    return {
                        "model_id": model_id,
                        "available": False,
                        "status": "not_found",
                        "checked_at": datetime.utcnow().isoformat()
                    }
            else:
                return {
                    "model_id": model_id,
                    "available": False,
                    "status": "api_error",
                    "error": response.text,
                    "checked_at": datetime.utcnow().isoformat()
                }
                
    except Exception as e:
        logger.error(f"❌ Error verificando modelo {model_id}: {str(e)}")
        return {
            "model_id": model_id,
            "available": False,
            "status": "error",
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat()
        }

async def run_health_check():
    """Ejecuta verificación de salud de modelos"""
    logger.info("🔍 Iniciando verificación de modelos...")
    
    for model_id in MODELS_TO_CHECK:
        result = await check_model_availability(model_id)
        
        if result["available"]:
            logger.info(f"✅ {model_id}: Disponible")
            logger.info(f"   Context: {result.get('context_length', 'N/A')}")
        else:
            logger.warning(f"⚠️ {model_id}: No disponible - {result['status']}")
    
    logger.info(f"✅ Verificación completada. Próxima verificación en {CHECK_INTERVAL} segundos")

async def main():
    """Función principal del watcher"""
    logger.info("🚀 Model Watcher iniciado")
    logger.info(f"📋 Modelos a monitorear: {MODELS_TO_CHECK}")
    logger.info(f"⏱️ Intervalo de verificación: {CHECK_INTERVAL} segundos")
    
    while True:
        try:
            await run_health_check()
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("🛑 Watcher detenido por el usuario")
            break
            
        except Exception as e:
            logger.error(f"❌ Error en el watcher: {str(e)}")
            time.sleep(60)  # Esperar 1 minuto antes de reintentar

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
