"""
Script para inicializar servicios en MongoDB con estructura completa
Incluye: billing_type, packs, precios crypto, requires_messaging, etc.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
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
    
    # Lista completa de servicios con estructura mejorada
    services = [
        {
            "name": "Consultoría Técnica IA",
            "slug": "consultoria-tecnica",
            "category": "Consultoría",
            "description": "Consultoría técnica personalizada con IA para optimizar procesos empresariales",
            "short_description": "Asesoría estratégica con IA",
            "price_monthly": 500000,
            "price_annual": 0,
            "price_crypto": 375000,  # 25% descuento
            "currency": "PYG",
            "billing_type": "one_time",
            "no_expiration": True,
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 1,
            "active": True,
            "features": ["Análisis de procesos", "Recomendaciones IA", "Soporte técnico"]
        },
        {
            "name": "Generador de Blogs con IA",
            "slug": "generador-blogs",
            "category": "Marketing",
            "description": "Genera contenido de blog de alta calidad usando Claude 3.5 Sonnet",
            "short_description": "Crea blogs profesionales con IA",
            "price_monthly": 200000,
            "price_annual": 2000000,  # 10 meses
            "price_annual_crypto": 1500000,  # 25% descuento
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": True,
            "order": 2,
            "active": True,
            "features": ["Generación automática", "SEO optimizado", "Publicación directa"]
        },
        {
            "name": "Prospección Comercial con IA",
            "slug": "prospeccion-comercial",
            "category": "Ventas",
            "description": "Sistema de prospección inteligente para encontrar clientes potenciales",
            "short_description": "Encuentra clientes con IA",
            "price_monthly": 0,
            "price_annual": 0,
            "currency": "PYG",
            "billing_type": "freemium_packs",
            "no_expiration": True,
            "requires_messaging": False,
            "packs": [
                {
                    "name": "Pack Básico",
                    "searches": 10,
                    "leads_per_search": 20,
                    "price_gs": 150000,
                    "popular": False
                },
                {
                    "name": "Pack Pro",
                    "searches": 25,
                    "leads_per_search": 20,
                    "price_gs": 350000,
                    "popular": True
                },
                {
                    "name": "Pack Enterprise",
                    "searches": 50,
                    "leads_per_search": 20,
                    "price_gs": 650000,
                    "popular": False
                }
            ],
            "order": 3,
            "active": True,
            "features": ["Análisis de mercado", "Generación de prospectos", "Scoring automático", "5 leads GRATIS de prueba"]
        },
        {
            "name": "Gestor de Emails con IA",
            "slug": "gestor-emails",
            "category": "Productividad",
            "description": "Gestiona tus emails automáticamente con inteligencia artificial",
            "short_description": "Automatiza tu bandeja de entrada",
            "price_monthly": 150000,
            "price_annual": 1500000,
            "price_annual_crypto": 1125000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 4,
            "active": True,
            "features": ["Clasificación automática", "Respuestas inteligentes", "Priorización"]
        },
        {
            "name": "Análisis de CVs con IA",
            "slug": "analisis-cvs",
            "category": "RRHH",
            "description": "Analiza currículums vitae de manera automática e inteligente",
            "short_description": "Screening inteligente de CVs",
            "price_monthly": 250000,
            "price_annual": 2500000,
            "price_annual_crypto": 1875000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 5,
            "active": True,
            "features": ["Análisis automatizado", "Ranking de candidatos", "Extracción de datos"]
        },
        {
            "name": "Procesamiento de Facturas con OCR",
            "slug": "procesamiento-facturas",
            "category": "Finanzas",
            "description": "Digitaliza y procesa facturas automáticamente con OCR",
            "short_description": "OCR para facturas",
            "price_monthly": 300000,
            "price_annual": 3000000,
            "price_annual_crypto": 2250000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 6,
            "active": True,
            "features": ["OCR avanzado", "Extracción de datos", "Integración contable"]
        },
        {
            "name": "Sistema de Agendamiento Inteligente",
            "slug": "agendamiento",
            "category": "Productividad",
            "description": "Gestiona citas y reuniones con inteligencia artificial",
            "short_description": "Agenda inteligente con IA",
            "price_monthly": 180000,
            "price_annual": 1800000,
            "price_annual_crypto": 1350000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 7,
            "active": True,
            "features": ["Sincronización de calendario", "Recordatorios automáticos", "Optimización de horarios"]
        },
        {
            "name": "Asistente Virtual para Directivos",
            "slug": "asistente-directivos",
            "category": "Asistencia",
            "description": "Asistente ejecutivo 24/7 powered by IA",
            "short_description": "Tu asistente personal IA",
            "price_monthly": 600000,
            "price_annual": 6000000,
            "price_annual_crypto": 4500000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,  # WhatsApp/Telegram
            "multi_purchase": False,
            "order": 8,
            "active": True,
            "features": ["Disponibilidad 24/7", "Gestión de tareas", "Integración completa", "WhatsApp o Telegram"]
        },
        {
            "name": "Análisis de Redes Sociales con IA",
            "slug": "analisis-redes-sociales",
            "category": "Marketing",
            "description": "Analiza y optimiza tu presencia en redes sociales",
            "short_description": "Social media con IA",
            "price_monthly": 350000,
            "price_annual": 3500000,
            "price_annual_crypto": 2625000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": True,
            "order": 9,
            "active": True,
            "features": ["Análisis de sentimiento", "Recomendaciones de contenido", "Métricas avanzadas"]
        },
        {
            "name": "Chatbot WhatsApp/Telegram",
            "slug": "chatbot-whatsapp",
            "category": "Atención al Cliente",
            "description": "Chatbot inteligente para atención al cliente 24/7",
            "short_description": "Atención automatizada",
            "price_monthly": 280000,
            "price_annual": 2800000,
            "price_annual_crypto": 2100000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,  # WhatsApp/Telegram
            "multi_purchase": True,
            "order": 10,
            "active": True,
            "features": ["Multi-plataforma", "Respuestas inteligentes", "Integración CRM", "WhatsApp o Telegram"]
        },
        {
            "name": "Pulse IA - Market Sentiment",
            "slug": "pulse-ia",
            "category": "Cripto",
            "description": "Análisis de sentimiento del mercado cripto desde 15+ fuentes (RSS, Twitter, Reddit)",
            "short_description": "Sentimiento de mercado con IA",
            "price_monthly": 200000,
            "price_annual": 2000000,
            "price_annual_crypto": 1500000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 11,
            "active": True,
            "features": [
                "Análisis de 15+ feeds RSS",
                "Scraping de Twitter y Reddit",
                "Detección FOMO/FUD con BERT",
                "Telegram Bot integrado",
                "Dashboard en tiempo real"
            ]
        },
        {
            "name": "Momentum Predictor IA",
            "slug": "momentum-predictor",
            "category": "Cripto",
            "description": "Predicción de señales de trading (BUY/SELL/HOLD) con LSTM y análisis técnico",
            "short_description": "Señales de trading con LSTM",
            "price_monthly": 250000,
            "price_annual": 2500000,
            "price_annual_crypto": 1875000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 12,
            "active": True,
            "features": [
                "Modelo LSTM para predicción",
                "20 indicadores técnicos (RSI, MACD, BB)",
                "Niveles de entrada/salida/stop loss",
                "Telegram Bot con señales",
                "Análisis de riesgo automático"
            ]
        },
        {
            "name": "CryptoShield IA",
            "slug": "cryptoshield-ia",
            "category": "Cripto",
            "description": "Detección de fraude y scams en blockchain con Autoencoder",
            "short_description": "Anti-fraude blockchain",
            "price_monthly": 300000,
            "price_annual": 3000000,
            "price_annual_crypto": 2250000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 13,
            "active": True,
            "features": [
                "Autoencoder para detección de fraude",
                "Análisis de transacciones en tiempo real",
                "Verificación de wallets/contratos",
                "Alertas automáticas",
                "Telegram Bot de seguridad"
            ]
        },
        {
            "name": "Suite Crypto IA Pro",
            "slug": "suite-crypto",
            "category": "Cripto",
            "description": "Suite completa con Pulse, Momentum, CryptoShield + 2 bots asistentes",
            "short_description": "5 bots cripto en 1 suite",
            "price_monthly": 800000,
            "price_annual": 8000000,
            "price_annual_crypto": 6000000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": False,
            "order": 14,
            "active": True,
            "features": [
                "CryptoShield IA - Anti-fraude",
                "Pulse IA - Sentimiento de mercado",
                "Momentum Predictor - Señales trading",
                "Asistente GuaraniAppStore",
                "Rocío Almeida - Consultor comercial"
            ]
        },
        {
            "name": "Automatización y Gestión de E-commerce",
            "slug": "automatizacion-ecommerce",
            "category": "E-commerce",
            "description": "Gestión automatizada completa para tu tienda online con IA",
            "short_description": "Automatiza tu tienda online",
            "price_monthly": 350000,
            "price_annual": 3500000,
            "price_annual_crypto": 2625000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": True,
            "order": 15,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Gestión de inventario automática",
                "Respuestas a clientes con IA",
                "Análisis de ventas",
                "Recomendaciones de productos"
            ]
        },
        {
            "name": "Automatización de Contenidos en redes sociales",
            "slug": "automatizacion-redes-sociales",
            "category": "Marketing",
            "description": "Crea y programa contenido automáticamente para tus redes sociales",
            "short_description": "Contenido automático para redes",
            "price_monthly": 250000,
            "price_annual": 2500000,
            "price_annual_crypto": 1875000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": True,
            "order": 16,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Generación de posts con IA",
                "Programación automática",
                "Análisis de engagement",
                "Optimización de hashtags"
            ]
        },
        {
            "name": "Generador de Blogs Automatizado y SEO",
            "slug": "generador-blogs-seo",
            "category": "Marketing",
            "description": "Genera artículos SEO optimizados automáticamente para tu blog",
            "short_description": "Blogs SEO con IA",
            "price_monthly": 280000,
            "price_annual": 2800000,
            "price_annual_crypto": 2100000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": False,
            "multi_purchase": True,
            "order": 17,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Artículos optimizados SEO",
                "Publicación automática",
                "Investigación de keywords",
                "Meta descriptions"
            ]
        },
        {
            "name": "Agente de Ventas IA",
            "slug": "agente-ventas-ia",
            "category": "Ventas",
            "description": "Agente de ventas con IA que contacta y cierra clientes automáticamente",
            "short_description": "Ventas automatizadas con IA",
            "price_monthly": 450000,
            "price_annual": 4500000,
            "price_annual_crypto": 3375000,
            "currency": "PYG",
            "billing_type": "subscription",
            "requires_messaging": True,
            "multi_purchase": False,
            "order": 18,
            "active": True,
            "status": "coming_soon",
            "features": [
                "Contacto automático de leads",
                "Seguimiento inteligente",
                "Cierre de ventas con IA",
                "Integración CRM",
                "WhatsApp o Telegram"
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
    messaging_count = await services_collection.count_documents({"requires_messaging": True})
    
    print(f"\n📊 Estadísticas:")
    print(f"   Servicios activos: {active_count}")
    print(f"   Servicios próximamente: {coming_soon_count}")
    print(f"   Servicios con mensajería: {messaging_count}")
    
    client.close()
    print("✅ Inicialización completada")

if __name__ == "__main__":
    asyncio.run(init_services())
