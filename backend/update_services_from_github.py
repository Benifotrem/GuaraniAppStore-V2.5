"""
Script para actualizar servicios en MongoDB con precios del repositorio GitHub
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

MONGO_URL = "mongodb://localhost:27017/guarani_appstore"

# Precios exactos del repositorio GitHub (init_services_v2.py)
SERVICES_DATA = [
    {
        'name': 'Suite Cripto (CryptoShield + Pulse + Momentum)',
        'slug': 'suite-cripto',
        'description': 'Suite completa de herramientas de IA para inversores en criptomonedas. Incluye 3 servicios vía Telegram: CryptoShield IA (escáner de fraude GRATIS), Pulse IA (análisis de sentimiento), y Momentum Predictor IA (señales diarias de trading).',
        'short_description': 'CryptoShield GRATIS + Pulse IA + Momentum IA',
        'price': 0,  # Mensual
        'price_monthly': 0,
        'price_annual': 600000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '₿',
        'features': [
            '🛡️ CryptoShield IA: Escáner de fraude GRATIS',
            '📊 Pulse IA: Indicador de sentimiento',
            '📈 Momentum Predictor IA: Señales diarias',
            '🤖 Acceso vía Telegram 24/7',
            '🪙 Gs. 450.000/año con BTC/ETH (25% OFF)'
        ],
        'ai_model': 'Claude 3.5 Sonnet + ML',
        'category': 'crypto',
        'order': 1
    },
    {
        'name': 'Asistente Personal para Directivos',
        'slug': 'asistente-directivos',
        'description': 'Asistente ejecutivo inteligente disponible 24/7 vía WhatsApp/Telegram. Gestiona tu agenda con integración Google Calendar, organiza tareas y recordatorios, controla ingresos y gastos empresariales, realiza búsquedas web automatizadas, enriquece contactos con datos de LinkedIn.',
        'short_description': 'Asistente ejecutivo 24/7 con Google Calendar',
        'price': 299000,
        'price_monthly': 299000,
        'price_annual': 2990000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '👔',
        'features': [
            'Asistente 24/7 vía WhatsApp/Telegram',
            'Integración Google Calendar',
            'Gestión de tareas y recordatorios',
            'Control de finanzas (ingresos/gastos)',
            'Búsquedas web automatizadas',
            'Enriquecimiento de contactos LinkedIn',
            '✈️ Telegram 20% más barato',
            '💰 2 meses gratis con plan anual'
        ],
        'ai_model': 'GPT-4o',
        'category': 'productivity',
        'order': 2
    },
    {
        'name': 'Agente de Preselección Curricular',
        'slug': 'preseleccion-curricular',
        'description': 'Automatiza completamente tu proceso de RRHH. Analiza CVs automáticamente con IA (PDF, Word, imágenes), genera scoring inteligente de candidatos, valida emails y perfiles de LinkedIn automáticamente, integración directa con Google Drive y Sheets.',
        'short_description': 'Análisis automático de CVs con IA',
        'price': 249000,
        'price_monthly': 249000,
        'price_annual': 2490000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '👥',
        'features': [
            'Análisis automático de CVs con IA',
            'Sistema de scoring inteligente',
            'Validación de emails y LinkedIn',
            'Integración Google Drive/Sheets',
            'Recepción automática por email',
            '✈️ Telegram 20% más barato',
            '💰 2 meses gratis con plan anual'
        ],
        'ai_model': 'Claude 3.5 Sonnet',
        'category': 'hr',
        'order': 3
    },
    {
        'name': 'Organizador de Facturas para Contadores',
        'slug': 'organizador-facturas',
        'description': 'OCR avanzado con IA para extracción automática de datos. Procesa facturas, contratos, formularios y documentos complejos, extrae campos específicos con alta precisión, soporta PDF, imágenes (JPG, PNG) y documentos escaneados.',
        'short_description': 'OCR con IA para facturas y documentos',
        'price': 199000,
        'price_monthly': 199000,
        'price_annual': 1990000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '🧾',
        'features': [
            'OCR avanzado multi-formato',
            'Extracción automática de datos',
            'Soporte PDF, JPG, PNG',
            'Integración Google Drive/Sheets',
            '🖥️ Acceso vía Panel Web',
            '💰 2 meses gratis con plan anual'
        ],
        'ai_model': 'Google Cloud Vision + Claude',
        'category': 'finance',
        'order': 4
    },
    {
        'name': 'Organizador de Agenda',
        'slug': 'organizador-agenda',
        'description': 'Gestión profesional de citas y contactos empresariales. Administra contactos y citas en una interfaz intuitiva, sincronización bidireccional con Google Calendar, envío automático de invitaciones por email con Brevo, emails personalizables con tu logo y branding.',
        'short_description': 'Gestión de citas con Google Calendar',
        'price': 99000,
        'price_monthly': 99000,
        'price_annual': 990000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '📅',
        'features': [
            'Gestión de contactos y citas',
            'Sincronización Google Calendar',
            'Invitaciones automáticas por email',
            'Personalización con tu branding',
            '🖥️ Acceso vía Panel Web',
            '💰 2 meses gratis con plan anual'
        ],
        'ai_model': 'GPT-4o',
        'category': 'productivity',
        'order': 5
    },
    {
        'name': 'Consultoría Técnica Personalizada',
        'slug': 'consultoria-tecnica',
        'description': 'Servicio premium de consultoría técnica one-on-one. Análisis profundo de tus procesos empresariales, estrategia personalizada de automatización con IA, implementación de soluciones custom adaptadas a tu negocio, acceso a información técnica confidencial de la plataforma.',
        'short_description': 'Consultoría premium one-on-one',
        'price': 750000,
        'price_monthly': 750000,
        'price_annual': 750000,
        'currency': 'PYG',
        'status': 'active',
        'active': True,
        'icon': '🎓',
        'features': [
            'Análisis profundo empresarial',
            'Estrategia personalizada de automatización',
            'Soluciones custom',
            'Información técnica confidencial',
            'Consultoría directa con equipo técnico',
            '💎 Pago único - No caduca',
            '🪙 Gs. 562.500 con BTC/ETH (25% OFF)'
        ],
        'ai_model': 'Consultoría Humana + IA',
        'category': 'consulting',
        'order': 6
    },
    {
        'name': 'Generador de Blogs Automatizado y SEO',
        'slug': 'generador-blogs',
        'description': 'Sistema de generación automática de contenido optimizado para SEO. Genera 1 artículo diario de 800-1500 palabras con IA avanzada, crea imágenes profesionales automáticamente, publica directamente en WordPress/Ghost/Medium, incluye análisis de tendencias y competencia.',
        'short_description': '1 artículo SEO diario con IA',
        'price': 149000,
        'price_monthly': 149000,
        'price_annual': 1490000,
        'currency': 'PYG',
        'status': 'coming_soon',
        'active': False,
        'icon': '📝',
        'features': [
            '1 artículo diario SEO-optimizado',
            'Generación con IA avanzada',
            'Imágenes profesionales incluidas',
            'Publicación directa en CMS',
            'Análisis de tendencias',
            '🔢 Múltiples instancias disponibles',
            '🖥️ Acceso vía Panel Web'
        ],
        'ai_model': 'Claude 3.5 + Gemini',
        'category': 'content',
        'order': 7
    },
    {
        'name': 'Automatización y Gestión de E-commerce',
        'slug': 'ecommerce-automation',
        'description': 'Gestión centralizada multi-plataforma de tu tienda online. Integración completa con Shopify (100% operativo), WooCommerce, BigCommerce y más, administra productos, inventario y pedidos desde un solo lugar, búsqueda inteligente de proveedores con IA.',
        'short_description': 'Gestión multi-plataforma Shopify, WooCommerce',
        'price': 399000,
        'price_monthly': 399000,
        'price_annual': 3990000,
        'currency': 'PYG',
        'status': 'coming_soon',
        'active': False,
        'icon': '🛒',
        'features': [
            'Integración Shopify (100% operativo)',
            'Soporte WooCommerce, BigCommerce',
            'Gestión de productos e inventario',
            'Administración de pedidos',
            'Búsqueda inteligente de proveedores',
            '🔢 Múltiples instancias para varias tiendas',
            '🖥️ Acceso vía Panel Web'
        ],
        'ai_model': 'GPT-4o',
        'category': 'automation',
        'order': 8
    },
    {
        'name': 'Automatización de Contenidos en Redes Sociales',
        'slug': 'redes-sociales',
        'description': 'Crea contenido viral optimizado para cada red social. Genera posts automáticamente desde videos de YouTube o artículos web, optimización específica para LinkedIn, Twitter/X, Instagram y Facebook, análisis automático de trending topics.',
        'short_description': 'Contenido viral optimizado por plataforma',
        'price': 249000,
        'price_monthly': 249000,
        'price_annual': 2490000,
        'currency': 'PYG',
        'status': 'coming_soon',
        'active': False,
        'icon': '📱',
        'features': [
            'Generación desde YouTube y artículos',
            'Optimización para 4 redes sociales',
            'Análisis de trending topics',
            'Adaptación de tono por plataforma',
            'Auto-publicación o borradores',
            '🔢 Múltiples instancias para varios perfiles',
            '🖥️ Acceso vía Panel Web'
        ],
        'ai_model': 'GPT-4o',
        'category': 'marketing',
        'order': 9
    },
    {
        'name': 'Ruptura del Hielo y Prospección Comercial Automatizada',
        'slug': 'prospeccion-comercial',
        'description': 'Sistema de prospección comercial automatizada con IA. Prueba GRATIS con 5 leads para descubrir cómo obtenemos contactos reales de Google Maps. Búsqueda automática de leads, extracción y validación de emails, generación de mensajes Ice Breaker personalizados con IA.',
        'short_description': 'Prospección en Google Maps con IA',
        'price': 0,
        'price_monthly': 0,
        'price_annual': 499000,
        'currency': 'PYG',
        'status': 'coming_soon',
        'active': False,
        'icon': '🎯',
        'features': [
            'Búsqueda automática en Google Maps',
            'Extracción y validación de emails',
            'Mensajes Ice Breaker personalizados con IA',
            'Exportación a Google Sheets',
            '⏰ Usos no caducan - Usa bajo demanda',
            '💎 Pago único por paquete',
            '🎁 Prueba GRATIS con 5 leads'
        ],
        'ai_model': 'Claude 3.5 Sonnet',
        'category': 'automation',
        'order': 10
    },
    {
        'name': 'Agente de Ventas IA',
        'slug': 'agente-ventas-ia',
        'description': 'Agente de ventas con IA que revoluciona tu proceso comercial. Base vectorizada de productos, búsqueda inteligente, envío automático de catálogos y fotos, cualificación automática de clientes (1-5 estrellas), seguimientos automáticos a las 6 y 23 horas, conversaciones naturales que replican vendedores humanos.',
        'short_description': 'Agente de ventas conversacional con IA',
        'price': 499000,
        'price_monthly': 499000,
        'price_annual': 4990000,
        'currency': 'PYG',
        'status': 'coming_soon',
        'active': False,
        'icon': '💼',
        'features': [
            'Base vectorizada con IA (hasta 200+ productos)',
            'Búsqueda inteligente de productos',
            'Envío automático de catálogos y fotos',
            'Cualificación de clientes (1-5 estrellas)',
            'Seguimientos automáticos (6h y 23h)',
            'Conversaciones naturales como humano',
            '✈️ Telegram 20% más barato',
            'Integración WhatsApp Business'
        ],
        'ai_model': 'GPT-4o + RAG',
        'category': 'automation',
        'order': 11
    }
]

async def update_services():
    """Update services in MongoDB with correct prices from GitHub"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.get_database()
    
    print('🔄 Actualizando servicios con precios de GitHub...\n')
    
    # Delete existing services
    await db.services.delete_many({})
    print('✓ Servicios anteriores eliminados')
    
    # Insert services with correct prices
    for service_data in SERVICES_DATA:
        service_data['created_at'] = datetime.utcnow()
        await db.services.insert_one(service_data)
        print(f'✓ {service_data["name"]}: Gs. {service_data["price_monthly"]:,}/mes')
    
    print(f'\n✅ {len(SERVICES_DATA)} servicios actualizados exitosamente desde GitHub!')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_services())
