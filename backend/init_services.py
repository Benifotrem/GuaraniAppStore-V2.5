"""
Script to initialize services in the database
Run this after database is created
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models import Service, ServiceStatus

SERVICES_DATA = [
    {
        'name': 'Suite Cripto (CryptoShield + Pulse + Momentum)',
        'slug': 'prospeccion-comercial',
        'description': 'Sistema IA de prospección automática que identifica y contacta clientes potenciales mediante análisis de datos comerciales.',
        'short_description': 'Prospección automática con IA',
        'price_monthly': 299.00,
        'price_annual': 2990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '🎯',
        'features': [
            'Extracción de datos con Outscraper',
            'Análisis y scoring con Claude IA',
            'Seguimiento automatizado',
            'Dashboard de leads'
        ],
        'ai_model': 'Claude 3.5 Sonnet',
        'category': 'automation',
        'order': 1
    },
    {
        'name': 'Agente de Ventas IA',
        'slug': 'agente-ventas-ia',
        'description': 'Agente conversacional IA que califica leads, responde consultas y cierra ventas automáticamente.',
        'short_description': 'Ventas automatizadas 24/7',
        'price_monthly': 499.00,
        'price_annual': 4990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '💼',
        'features': [
            'Conversaciones naturales con IA',
            'Calificación de leads',
            'Integración CRM',
            'Reportes de conversión'
        ],
        'ai_model': 'GPT-4o',
        'category': 'automation',
        'order': 2
    },
    {
        'name': 'Asistente Personal para Directivos',
        'slug': 'asistente-directivos',
        'description': 'Asistente IA que gestiona agenda, emails, reuniones y tareas para ejecutivos y directivos.',
        'short_description': 'Productividad ejecutiva con IA',
        'price_monthly': 399.00,
        'price_annual': 3990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '👔',
        'features': [
            'Gestión de calendario Google',
            'Priorización de emails',
            'Preparación de reuniones',
            'Resúmenes ejecutivos'
        ],
        'ai_model': 'Claude 3.5 Sonnet',
        'category': 'productivity',
        'order': 3
    },
    {
        'name': 'Generador de Blogs Automatizado',
        'slug': 'generador-blogs',
        'description': 'Sistema que genera artículos de blog profesionales automáticamente con IA de última generación.',
        'short_description': 'Contenido SEO automático',
        'price_monthly': 199.00,
        'price_annual': 1990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '📝',
        'features': [
            'Generación con Claude 3.5',
            'Imágenes con Gemini',
            'Optimización SEO',
            'Publicación programada'
        ],
        'ai_model': 'Claude 3.5 Sonnet + Gemini',
        'category': 'content',
        'order': 4
    },
    {
        'name': 'Automatización de E-commerce',
        'slug': 'ecommerce-automation',
        'description': 'Automatización completa de operaciones de e-commerce: inventario, pedidos, atención al cliente.',
        'short_description': 'E-commerce en piloto automático',
        'price_monthly': 599.00,
        'price_annual': 5990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '🛒',
        'features': [
            'Gestión de inventario',
            'Procesamiento de pedidos',
            'Chatbot de soporte',
            'Análisis de ventas'
        ],
        'ai_model': 'GPT-4o',
        'category': 'automation',
        'order': 5
    },
    {
        'name': 'Agente de Preselección Curricular',
        'slug': 'preseleccion-curricular',
        'description': 'IA que analiza CVs, evalúa candidatos y programa entrevistas automáticamente.',
        'short_description': 'Reclutamiento inteligente',
        'price_monthly': 349.00,
        'price_annual': 3490.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '👥',
        'features': [
            'Análisis de CVs con IA',
            'Scoring de candidatos',
            'Entrevistas automatizadas',
            'Integración con ATS'
        ],
        'ai_model': 'Claude 3.5 Sonnet',
        'category': 'hr',
        'order': 6
    },
    {
        'name': 'Automatización de Redes Sociales',
        'slug': 'redes-sociales',
        'description': 'Gestión automática de redes sociales: creación de contenido, publicación y análisis.',
        'short_description': 'Social media en automático',
        'price_monthly': 249.00,
        'price_annual': 2490.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '📱',
        'features': [
            'Generación de posts con IA',
            'Publicación multi-plataforma',
            'Análisis de engagement',
            'Respuestas automáticas'
        ],
        'ai_model': 'GPT-4o',
        'category': 'marketing',
        'order': 7
    },
    {
        'name': 'Organizador de Facturas (OCR)',
        'slug': 'organizador-facturas',
        'description': 'Sistema OCR con IA que extrae, organiza y categoriza facturas automáticamente.',
        'short_description': 'Contabilidad automatizada',
        'price_monthly': 149.00,
        'price_annual': 1490.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '🧾',
        'features': [
            'OCR con Tesseract + Google Vision',
            'Validación de RUC',
            'Categorización automática',
            'Exportación a Excel'
        ],
        'ai_model': 'Google Cloud Vision + Claude',
        'category': 'finance',
        'order': 8
    },
    {
        'name': 'Organizador de Agenda',
        'slug': 'organizador-agenda',
        'description': 'Asistente IA que gestiona tu calendario, programa reuniones y envía recordatorios.',
        'short_description': 'Calendario inteligente',
        'price_monthly': 99.00,
        'price_annual': 990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '📅',
        'features': [
            'Integración Google Calendar',
            'Programación inteligente',
            'Recordatorios automáticos',
            'Detección de conflictos'
        ],
        'ai_model': 'GPT-4o',
        'category': 'productivity',
        'order': 9
    },
    {
        'name': 'Consultoría Técnica Personalizada',
        'slug': 'consultoria-tecnica',
        'description': 'Asesoría personalizada para implementar IA y automatización en tu empresa.',
        'short_description': 'Transformación digital con IA',
        'price_monthly': 999.00,
        'price_annual': 9990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '🎓',
        'features': [
            'Auditoría de procesos',
            'Plan de implementación',
            'Desarrollo personalizado',
            'Soporte dedicado'
        ],
        'ai_model': 'Consultoría Humana + IA',
        'category': 'consulting',
        'order': 10
    },
    {
        'name': 'Suite Cripto (3 Bots Telegram)',
        'slug': 'suite-cripto',
        'description': 'Suite completa de bots IA para análisis crypto: detección de fraude, sentimiento y señales de trading.',
        'short_description': 'Análisis crypto con IA',
        'price_monthly': 699.00,
        'price_annual': 6990.00,
        'status': ServiceStatus.COMING_SOON,
        'icon': '₿',
        'features': [
            'CryptoShield (anti-fraude)',
            'Pulse IA (sentimiento)',
            'Momentum Predictor (señales)',
            'Análisis blockchain en tiempo real'
        ],
        'ai_model': 'Claude 3.5 Sonnet + ML Models',
        'category': 'crypto',
        'order': 11
    }
]

async def init_services():
    """Initialize services in database"""
    async with AsyncSessionLocal() as db:
        print('Initializing services...')
        
        for service_data in SERVICES_DATA:
            # Check if service already exists
            from sqlalchemy import select
            result = await db.execute(
                select(Service).filter(Service.slug == service_data['slug'])
            )
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f'Service {service_data["name"]} already exists, skipping...')
                continue
            
            # Create service
            service = Service(**service_data)
            db.add(service)
            print(f'Created service: {service_data["name"]}')
        
        await db.commit()
        print('Services initialized successfully!')

if __name__ == '__main__':
    asyncio.run(init_services())
