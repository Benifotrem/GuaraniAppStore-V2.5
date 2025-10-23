"""
Blog Scheduler - Automatización de generación de artículos
Genera 7 artículos por semana:
- Lunes a Sábado: 6 agentes especializados
- Domingo: CEO

Usa APScheduler para programación automática
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from blog_generator_service import blog_generator
from database import SessionLocal
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear scheduler
scheduler = AsyncIOScheduler()


async def generate_daily_article():
    """
    Genera el artículo del día según el día de la semana
    Ejecutado automáticamente cada día a las 08:00 AM
    """
    db = SessionLocal()
    try:
        # Obtener día de la semana (0=Monday, 6=Sunday)
        day_of_week = datetime.now().weekday()
        
        logger.info(f"🚀 Iniciando generación de artículo para día {day_of_week}")
        
        # Generar artículo
        blog_post = await blog_generator.generate_scheduled_article(
            day_of_week=day_of_week,
            db=db
        )
        
        if blog_post:
            logger.info(f"✅ Artículo generado exitosamente: {blog_post.title}")
            logger.info(f"   Autor: {blog_post.author_name}")
            logger.info(f"   Slug: {blog_post.slug}")
            logger.info(f"   Publicado: {blog_post.published}")
        else:
            logger.error(f"❌ Error al generar artículo para día {day_of_week}")
            
    except Exception as e:
        logger.error(f"❌ Error en generación de artículo diario: {str(e)}")
    finally:
        db.close()


def start_blog_scheduler():
    """
    Inicia el scheduler de artículos
    Programa generación diaria a las 08:00 AM (Paraguay timezone)
    """
    try:
        # Programar generación diaria a las 08:00 AM
        scheduler.add_job(
            generate_daily_article,
            trigger=CronTrigger(
                hour=8,
                minute=0,
                timezone='America/Asuncion'
            ),
            id='daily_blog_article',
            name='Generar artículo diario',
            replace_existing=True
        )
        
        logger.info("📅 Blog Scheduler iniciado")
        logger.info("   - Generación diaria programada: 08:00 AM (Paraguay)")
        logger.info("   - Frecuencia: 7 artículos por semana")
        logger.info("   - Lun-Sáb: Agentes especializados")
        logger.info("   - Domingo: CEO")
        
        # Iniciar scheduler
        scheduler.start()
        logger.info("✅ Scheduler activo")
        
    except Exception as e:
        logger.error(f"❌ Error iniciando scheduler: {str(e)}")


def stop_blog_scheduler():
    """Detiene el scheduler de artículos"""
    try:
        scheduler.shutdown(wait=False)
        logger.info("🛑 Blog Scheduler detenido")
    except Exception as e:
        logger.error(f"❌ Error deteniendo scheduler: {str(e)}")


def get_scheduler_status():
    """Retorna el estado del scheduler"""
    return {
        "running": scheduler.running,
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time) if job.next_run_time else None
            }
            for job in scheduler.get_jobs()
        ]
    }


# Para testing manual
async def test_generate_article(day_of_week: int = None):
    """
    Genera un artículo de prueba para un día específico
    Útil para testing sin esperar al scheduler
    """
    db = SessionLocal()
    try:
        if day_of_week is None:
            day_of_week = datetime.now().weekday()
        
        logger.info(f"🧪 TEST: Generando artículo para día {day_of_week}")
        
        blog_post = await blog_generator.generate_scheduled_article(
            day_of_week=day_of_week,
            db=db
        )
        
        if blog_post:
            logger.info(f"✅ TEST: Artículo generado: {blog_post.title}")
            return blog_post
        else:
            logger.error(f"❌ TEST: Error generando artículo")
            return None
            
    except Exception as e:
        logger.error(f"❌ TEST: Error: {str(e)}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    # Para ejecución directa (testing)
    import asyncio
    
    print("Blog Scheduler - Testing Mode")
    print("1. Iniciar scheduler")
    print("2. Generar artículo de prueba")
    choice = input("Opción: ")
    
    if choice == "1":
        start_blog_scheduler()
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            stop_blog_scheduler()
    elif choice == "2":
        day = input("Día de la semana (0-6, Enter para hoy): ")
        day = int(day) if day else None
        asyncio.run(test_generate_article(day))
