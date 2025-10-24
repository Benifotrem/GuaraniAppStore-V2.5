"""
Script para inicializar servicios EXACTOS del sitio real guaraniappstore.com
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'guarani_appstore')

async def init_services():
    print("Conectando a MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    services_collection = db['services']
    
    # Limpiar servicios existentes
    await services_collection.delete_many({})
    print("Servicios existentes eliminados")
    
    # Servicios EXACTOS del sitio real
    services = [
        {
            "name": "Suite Crypto IA",
            "slug": "suite-crypto",
            "category": "Cripto",
            "description": "Suite completa de herramientas de IA para inversores en criptomonedas. Incluye 3 servicios vía Telegram: CryptoShield IA (escáner de fraude GRATIS), Pulse IA (análisis de sentimiento), y Momentum Predictor IA (señales diarias de trading). Todo en una sola suscripción anual.",
            "short_description": "3 servicios cripto en 1 suscripción",
            "price_monthly": 0,
            "price_annual": 600000,
            "price_annual_crypto": 450000,
            "currency": "PYG",
            "billing_type": "subscription",
            "billing_period": "annual_only",
            "requires_messaging": False,
            "platform": "telegram",
            "multi_purchase": False,
            "order": 1,
            "active": True,
            "features": [
                "🛡️ CryptoShield IA: Escáner de fraude GRATIS (incluido siempre)",
                "📊 Pulse IA: Indicador de sentimiento algorítmico",
                "📈 Momentum Predictor IA: Señales diarias de trading",
                "🤖 Acceso vía Telegram 24/7",
                "📱 Integración con los 3 bots"
            ],
            "included_services": [
                {"name": "CryptoShield IA", "status": "GRATIS"},
                {"name": "Pulse IA", "status": "included"},
                {"name": "Momentum Predictor IA", "status": "included"}
            ]
        },
        {
            "name": "Asistente Personal para Directivos",
            "slug": "asistente-directivos",
            "category": "Asistencia",
            "description": "Asistente ejecutivo inteligente disponible 24/7 vía WhatsApp/Telegram. Gestiona tu agenda con integración Google Calendar, organiza tareas y recordatorios, controla ingresos y gastos empresariales, realiza búsquedas web automatizadas, enriquece contactos con datos de LinkedIn automáticamente, y procesa texto, voz e imágenes.",
            "short_description": "Asistente ejecutivo 24/7",
            "price_monthly": 299000,
            "price_annual": 2990000,
            "price_annual_crypto": 2242500,
            "price_monthly_telegram": 239200,
            "price_annual_telegram": 2392000,
            "price_annual_crypto_telegram": 1794000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,
            "platform": "whatsapp_telegram",
            "telegram_discount": 20,
            "multi_purchase": False,
            "order": 2,
            "active": True,
            "features": [
                "Asistente 24/7 vía WhatsApp/Telegram",
                "Integración Google Calendar",
                "Gestión de tareas y recordatorios",
                "Control de finanzas (ingresos/gastos)",
                "Búsquedas web automatizadas",
                "Enriquecimiento de contactos con LinkedIn",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Agente de Preselección Curricular",
            "slug": "agente-preseleccion-curricular",
            "category": "RRHH",
            "description": "Automatiza completamente tu proceso de RRHH. Analiza CVs automáticamente con IA (PDF, Word, imágenes), genera scoring inteligente de candidatos, valida emails y perfiles de LinkedIn automáticamente, integración directa con Google Drive y Sheets, y recibe CVs por email y obtén pre-selección instantánea.",
            "short_description": "Análisis automático de CVs con IA",
            "price_monthly": 249000,
            "price_annual": 2490000,
            "price_annual_crypto": 1867500,
            "price_monthly_telegram": 199200,
            "price_annual_telegram": 1992000,
            "price_annual_crypto_telegram": 1494000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,
            "platform": "whatsapp_telegram",
            "telegram_discount": 20,
            "multi_purchase": False,
            "order": 3,
            "active": True,
            "features": [
                "Análisis automático de CVs con IA",
                "Sistema de scoring inteligente",
                "Validación de emails y LinkedIn",
                "Integración Google Drive/Sheets",
                "Recepción automática por email",
                "Pre-selección instantánea",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Organizador de facturas para Contadores",
            "slug": "organizador-facturas",
            "category": "Finanzas",
            "description": "OCR avanzado con IA para extracción automática de datos. Procesa facturas, contratos, formularios y documentos complejos, extrae campos específicos con alta precisión, soporta PDF, imágenes (JPG, PNG) y documentos escaneados, integración automática con Google Drive y Sheets, y exporta datos estructurados listos para usar.",
            "short_description": "OCR inteligente para facturas",
            "price_monthly": 199000,
            "price_annual": 1990000,
            "price_annual_crypto": 1492500,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": False,
            "order": 4,
            "active": True,
            "features": [
                "OCR avanzado multi-formato",
                "Extracción automática de datos estructurados",
                "Soporte PDF, JPG, PNG",
                "Integración Google Drive/Sheets",
                "Procesa facturas, contratos, formularios",
                "Alta precisión con IA",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Organizador de Agenda",
            "slug": "organizador-agenda",
            "category": "Productividad",
            "description": "Gestión profesional de citas y contactos empresariales. Administra contactos y citas en una interfaz intuitiva, sincronización bidireccional con Google Calendar, envío automático de invitaciones por email con Brevo, emails personalizables con tu logo y branding, y recordatorios automáticos para contactos.",
            "short_description": "Gestión inteligente de citas",
            "price_monthly": 99000,
            "price_annual": 990000,
            "price_annual_crypto": 742500,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": False,
            "order": 5,
            "active": True,
            "features": [
                "Gestión de contactos y citas",
                "Sincronización Google Calendar",
                "Invitaciones automáticas por email",
                "Personalización con tu branding",
                "Emails con logo personalizado",
                "Recordatorios automáticos",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Consultoría Técnica Personalizada",
            "slug": "consultoria-tecnica",
            "category": "Consultoría",
            "description": "Servicio premium de consultoría técnica one-on-one. Análisis profundo de tus procesos empresariales, estrategia personalizada de automatización con IA, implementación de soluciones custom adaptadas a tu negocio, acceso a información técnica confidencial de la plataforma, y sesiones de consultoría directa con el equipo técnico. Pago único que no caduca - usa bajo demanda cuando lo necesites.",
            "short_description": "Consultoría técnica premium",
            "price_monthly": 750000,
            "price_crypto": 562500,
            "currency": "PYG",
            "billing_type": "one_time",
            "no_expiration": True,
            "requires_messaging": False,
            "platform": "consultancy",
            "multi_purchase": True,
            "order": 6,
            "active": True,
            "features": [
                "Análisis profundo empresarial",
                "Estrategia personalizada de automatización",
                "Soluciones custom",
                "Información técnica confidencial",
                "Consultoría directa con equipo técnico",
                "25% descuento con BTC/ETH",
                "⏰ No caduca - Usa bajo demanda"
            ]
        },
        # SERVICIOS PRÓXIMAMENTE
        {
            "name": "Generador de Blogs Automatizado y SEO",
            "slug": "generador-blogs-seo",
            "category": "Marketing",
            "description": "Sistema de generación automática de contenido optimizado para SEO. Genera 1 artículo diario de 800-1500 palabras con IA avanzada, crea imágenes profesionales automáticamente, publica directamente en WordPress/Ghost/Medium, incluye análisis de tendencias y competencia. Puedes contratar múltiples instancias si gestionas varios blogs.",
            "short_description": "Blogs SEO automáticos con IA",
            "price_monthly": 0,
            "price_annual": 0,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": True,
            "order": 7,
            "active": True,
            "status": "coming_soon",
            "features": [
                "1 artículo diario SEO-optimizado (800-1500 palabras)",
                "Generación con IA avanzada",
                "Imágenes profesionales incluidas",
                "Publicación directa en CMS (WordPress/Ghost/Medium)",
                "Análisis de tendencias y competencia",
                "Contrata múltiples instancias para varios blogs",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Automatización y Gestión de E-commerce",
            "slug": "automatizacion-ecommerce",
            "category": "E-commerce",
            "description": "Gestión centralizada multi-plataforma de tu tienda online. Integración completa con Shopify (100% operativo), WooCommerce, BigCommerce y más, administra productos, inventario y pedidos desde un solo lugar, búsqueda inteligente de proveedores con IA. Puedes contratar múltiples instancias si gestionas varias tiendas.",
            "short_description": "Gestión multi-plataforma de tiendas",
            "price_monthly": 0,
            "price_annual": 0,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": True,
            "order": 8,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Integración Shopify (100% operativo)",
                "Soporte WooCommerce, BigCommerce",
                "Gestión de productos e inventario",
                "Administración de pedidos",
                "Búsqueda inteligente de proveedores",
                "Contrata múltiples instancias para varias tiendas",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Automatización de Contenidos en redes sociales",
            "slug": "automatizacion-redes-sociales",
            "category": "Marketing",
            "description": "Crea contenido viral optimizado para cada red social. Genera posts automáticamente desde videos de YouTube o artículos web, optimización específica para LinkedIn, Twitter/X, Instagram y Facebook, análisis automático de trending topics. Puedes contratar múltiples instancias si gestionas varios perfiles.",
            "short_description": "Contenido viral para redes sociales",
            "price_monthly": 0,
            "price_annual": 0,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": True,
            "order": 9,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Generación desde YouTube y artículos",
                "Optimización para 4 redes sociales",
                "Análisis de trending topics",
                "Adaptación de tono por plataforma",
                "Auto-publicación o borradores",
                "Contrata múltiples instancias para varios perfiles",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual"
            ]
        },
        {
            "name": "Ruptura del Hielo y Prospección Comercial Automatizada",
            "slug": "prospeccion-comercial",
            "category": "Ventas",
            "description": "Sistema de prospección comercial automatizada con IA. Prueba GRATIS con 5 leads para descubrir cómo obtenemos contactos reales de Google Maps. Búsqueda automática de leads, extracción y validación de emails, generación de mensajes Ice Breaker personalizados con IA, exportación a Google Sheets. Compra packs de búsquedas según tus necesidades.",
            "short_description": "Prospección automática con IA",
            "price_monthly": 0,
            "currency": "PYG",
            "billing_type": "one_time",
            "no_expiration": True,
            "requires_messaging": False,
            "platform": "web_panel",
            "multi_purchase": True,
            "order": 10,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Búsqueda automática en Google Maps",
                "Extracción y validación de emails",
                "Mensajes Ice Breaker personalizados con IA",
                "Exportación a Google Sheets",
                "⏰ Usos no caducan - Usa bajo demanda",
                "25% descuento con BTC/ETH",
                "Compra según necesidad"
            ]
        },
        {
            "name": "Agente de Ventas IA",
            "slug": "agente-ventas-ia",
            "category": "Ventas",
            "description": "Agente de ventas con IA que revoluciona tu proceso comercial. Base vectorizada de productos, búsqueda inteligente, envío automático de catálogos y fotos, cualificación automática de clientes (1-5 estrellas), seguimientos automáticos a las 6 y 23 horas aprovechando ventana de WhatsApp sin costo adicional, conversaciones naturales que replican vendedores humanos. Integración con WhatsApp, gestión de inventario hasta 200+ productos, calculadora de medidas y precios, y transferencia a humano cuando es necesario.",
            "short_description": "Vendedor IA 24/7",
            "price_monthly": 0,
            "price_annual": 0,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,
            "platform": "whatsapp_telegram",
            "telegram_discount": 20,
            "multi_purchase": False,
            "order": 11,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Base vectorizada con IA (hasta 200+ productos)",
                "Búsqueda inteligente de productos",
                "Envío automático de catálogos y fotos",
                "Cualificación de clientes (1-5 estrellas)",
                "Seguimientos automáticos (6h y 23h)",
                "Conversaciones naturales como humano",
                "Calculadora de medidas y precios",
                "Transferencia a vendedor humano",
                "Integración WhatsApp Business",
                "25% descuento con BTC/ETH",
                "💰 2 meses gratis con plan anual",
                "Ahorro en costos de seguimiento"
            ]
        }
    ]
    
    # Insertar servicios
    result = await services_collection.insert_many(services)
    print(f"✅ {len(result.inserted_ids)} servicios insertados en MongoDB")
    
    # Verificar
    count = await services_collection.count_documents({})
    print(f"Total de servicios en la base de datos: {count}")
    
    # Estadísticas
    active_count = await services_collection.count_documents({"status": {"$ne": "coming_soon"}})
    coming_soon_count = await services_collection.count_documents({"status": "coming_soon"})
    
    print(f"\n📊 Estadísticas:")
    print(f"   Servicios activos: {active_count}")
    print(f"   Servicios próximamente: {coming_soon_count}")
    
    client.close()
    print("✅ Inicialización completada - Servicios del sitio real replicados")

if __name__ == "__main__":
    asyncio.run(init_services())
