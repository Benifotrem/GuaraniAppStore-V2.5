"""
Script para inicializar servicios en MongoDB
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
    
    # Lista de 11 servicios
    services = [
        {
            "name": "Consultoría Técnica IA",
            "slug": "consultoria-tecnica",
            "category": "Consultoría",
            "description": "Consultoría técnica personalizada con IA para optimizar procesos empresariales",
            "short_description": "Asesoría estratégica con IA",
            "price": 500000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 200000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 400000,
            "currency": "PYG",
            "duration_days": 30,
            "order": 3,
            "active": True,
            "features": ["Análisis de mercado", "Generación de prospectos", "Scoring automático"]
        },
        {
            "name": "Gestor de Emails con IA",
            "slug": "gestor-emails",
            "category": "Productividad",
            "description": "Gestiona tus emails automáticamente con inteligencia artificial",
            "short_description": "Automatiza tu bandeja de entrada",
            "price": 150000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 250000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 300000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 180000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 600000,
            "currency": "PYG",
            "duration_days": 30,
            "order": 8,
            "active": True,
            "features": ["Disponibilidad 24/7", "Gestión de tareas", "Integración completa"]
        },
        {
            "name": "Análisis de Redes Sociales con IA",
            "slug": "analisis-redes-sociales",
            "category": "Marketing",
            "description": "Analiza y optimiza tu presencia en redes sociales",
            "short_description": "Social media con IA",
            "price": 350000,
            "currency": "PYG",
            "duration_days": 30,
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
            "price": 280000,
            "currency": "PYG",
            "duration_days": 30,
            "order": 10,
            "active": True,
            "features": ["Multi-plataforma", "Respuestas inteligentes", "Integración CRM"]
        },
        {
            "name": "Suite Crypto",
            "slug": "suite-crypto",
            "category": "Cripto",
            "description": "Suite completa de 5 bots de Telegram para el ecosistema crypto",
            "short_description": "5 bots cripto en 1 suite",
            "price": 800000,
            "currency": "PYG",
            "duration_days": 30,
            "order": 11,
            "active": True,
            "features": [
                "CryptoShield IA - Anti-fraude",
                "Pulse IA - Sentimiento de mercado",
                "Momentum Predictor - Señales trading",
                "Asistente GuaraniAppStore",
                "Rocío Almeida - Consultor comercial"
            ]
        }
    ]
    
    # Insertar servicios
    result = await services_collection.insert_many(services)
    print(f"✅ {len(result.inserted_ids)} servicios insertados en MongoDB")
    
    # Verificar
    count = await services_collection.count_documents({})
    print(f"Total de servicios en la base de datos: {count}")
    
    client.close()
    print("✅ Inicialización completada")

if __name__ == "__main__":
    asyncio.run(init_services())
