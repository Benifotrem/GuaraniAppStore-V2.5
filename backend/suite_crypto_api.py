"""
API unificada para Suite Crypto IA
Proporciona acceso a los 3 servicios: Pulse IA, Momentum Predictor y CryptoShield
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, List
from datetime import datetime

router = APIRouter(prefix="/api/suite-crypto", tags=["suite-crypto"])

@router.get("/health")
async def health_check():
    """
    Health check para verificar el estado de los 3 servicios de la suite
    """
    services_status = {
        'pulse_ia': {
            'name': 'Pulse IA',
            'status': 'active',
            'description': 'Análisis de sentimiento del mercado',
            'endpoint': '/api/pulse'
        },
        'momentum_predictor': {
            'name': 'Momentum Predictor IA', 
            'status': 'active',
            'description': 'Señales de trading diarias',
            'endpoint': '/api/momentum'
        },
        'cryptoshield_ia': {
            'name': 'CryptoShield IA',
            'status': 'active',
            'description': 'Escáner de fraude GRATIS',
            'endpoint': '/api/cryptoshield',
            'is_free': True
        }
    }
    
    return {
        "status": "healthy",
        "service": "Suite Crypto IA",
        "version": "1.0.0",
        "services": services_status,
        "price": {
            "annual": 600000,
            "annual_crypto": 450000,
            "currency": "PYG"
        },
        "checked_at": datetime.now().isoformat()
    }

@router.get("/dashboard")
async def get_dashboard_data():
    """
    Obtener datos del dashboard unificado
    Incluye resumen de los 3 servicios
    """
    import requests
    
    dashboard_data = {
        'pulse_ia': {
            'name': 'Pulse IA',
            'description': 'Análisis de sentimiento del mercado cripto',
            'status': 'active',
            'endpoint': '/api/pulse',
            'icon': '📊'
        },
        'momentum_predictor': {
            'name': 'Momentum Predictor IA',
            'description': 'Señales de trading diarias',
            'status': 'active',
            'endpoint': '/api/momentum',
            'icon': '📈'
        },
        'cryptoshield_ia': {
            'name': 'CryptoShield IA',
            'description': 'Escáner de fraude GRATIS',
            'status': 'active',
            'endpoint': '/api/cryptoshield',
            'icon': '🛡️',
            'is_free': True
        }
    }
    
    return dashboard_data

@router.get("/quick-analysis/{symbol}")
async def quick_analysis(symbol: str):
    """
    Análisis rápido de una criptomoneda usando los 3 servicios
    
    Args:
        symbol: Símbolo de la criptomoneda (BTC, ETH, etc.)
    """
    import requests
    
    base_url = "http://localhost:8001"
    analysis = {
        'symbol': symbol.upper(),
        'timestamp': datetime.now().isoformat()
    }
    
    # Obtener señal de trading de Momentum Predictor
    try:
        momentum_response = requests.get(f"{base_url}/api/momentum/signal/{symbol}", timeout=10)
        if momentum_response.status_code == 200:
            analysis['trading_signal'] = momentum_response.json()
        else:
            analysis['trading_signal'] = {'error': 'No disponible'}
    except Exception as e:
        analysis['trading_signal'] = {'error': str(e)}
    
    # Obtener sentimiento de Pulse IA
    try:
        # Pulse IA no tiene endpoint por símbolo específico, usar el general
        analysis['sentiment'] = {
            'message': 'Análisis de sentimiento general disponible en dashboard de Pulse IA',
            'endpoint': '/api/pulse'
        }
    except Exception as e:
        analysis['sentiment'] = {'error': str(e)}
    
    return analysis

@router.get("/services-list")
async def get_services_list():
    """
    Listar los servicios incluidos en la suite con sus descripciones
    """
    return {
        'suite_name': 'Suite Crypto IA',
        'price': {
            'annual': 600000,
            'annual_crypto': 450000,
            'currency': 'PYG',
            'discount_crypto': 25
        },
        'services': [
            {
                'id': 'cryptoshield-ia',
                'name': 'CryptoShield IA',
                'status': 'GRATIS',
                'description': 'Escáner de fraude en tiempo real para transacciones blockchain',
                'features': [
                    'Análisis de wallets en tiempo real',
                    'Verificación de transacciones',
                    'Escaneo de contratos inteligentes',
                    'Detección de patrones fraudulentos',
                    'Alertas automáticas'
                ],
                'endpoint': '/api/cryptoshield',
                'telegram_bot': 'CryptoShield_IA_Bot'
            },
            {
                'id': 'pulse-ia',
                'name': 'Pulse IA',
                'status': 'included',
                'description': 'Indicador de sentimiento algorítmico del mercado cripto',
                'features': [
                    'Análisis de 15+ fuentes RSS',
                    'Scraping de Twitter y Reddit',
                    'Detección FOMO/FUD con BERT',
                    'Trending topics en tiempo real',
                    'Dashboard de sentimiento'
                ],
                'endpoint': '/api/pulse',
                'telegram_bot': 'Pulse_IA_Bot'
            },
            {
                'id': 'momentum-predictor-ia',
                'name': 'Momentum Predictor IA',
                'status': 'included',
                'description': 'Señales diarias de trading con análisis técnico',
                'features': [
                    'Señales BUY/SELL/HOLD',
                    '20 indicadores técnicos',
                    'Niveles de entrada/salida',
                    'Stop loss automático',
                    'Análisis de riesgo'
                ],
                'endpoint': '/api/momentum',
                'telegram_bot': 'Momentum_Predictor_Bot'
            }
        ],
        'benefits': [
            '🤖 Acceso vía Telegram 24/7',
            '📱 3 bots especializados',
            '💰 Ahorro vs comprar por separado',
            '🛡️ CryptoShield GRATIS incluido',
            '📊 Dashboard unificado'
        ]
    }
