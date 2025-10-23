"""
GuaraniAppStore V2.5 Pro - Servicio de APIs Externas
Integración centralizada de Google Cloud Vision, CoinGecko, Etherscan, BSCScan, Outscraper, Apify

Arquitectura:
- Google Cloud Vision: Service Account (OCR para facturas/documentos)
- Google Calendar/Sheets/Blogger: OAuth 2.0 por usuario
- CoinGecko: API directa con caching
- Etherscan/BSCScan: API directa para datos blockchain
- Outscraper/Apify: Web scraping y automation
"""

import os
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

# Google Cloud Vision
try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    logging.warning("Google Cloud Vision no disponible. Instalar: pip install google-cloud-vision")

# CoinGecko
try:
    from pycoingecko import CoinGeckoAPI
    COINGECKO_AVAILABLE = True
except ImportError:
    COINGECKO_AVAILABLE = False
    logging.warning("CoinGecko no disponible. Instalar: pip install pycoingecko")

# Etherscan
try:
    from etherscan import Etherscan
    ETHERSCAN_AVAILABLE = True
except ImportError:
    ETHERSCAN_AVAILABLE = False
    logging.warning("Etherscan no disponible. Instalar: pip install etherscan-python")

# Google APIs (Calendar, Sheets, Blogger)
try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import Flow
    from google.auth.transport.requests import Request
    import pickle
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False
    logging.warning("Google APIs no disponibles. Instalar: pip install google-api-python-client google-auth-oauthlib")

logger = logging.getLogger(__name__)


class GoogleVisionService:
    """Servicio de OCR usando Google Cloud Vision API con Service Account"""
    
    def __init__(self):
        self.client = None
        self.enabled = GOOGLE_VISION_AVAILABLE
        
        if self.enabled:
            try:
                credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
                project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
                
                if credentials_path and os.path.exists(credentials_path):
                    credentials = service_account.Credentials.from_service_account_file(
                        credentials_path
                    )
                    self.client = vision.ImageAnnotatorClient(credentials=credentials)
                    logger.info("✅ Google Cloud Vision inicializado correctamente")
                else:
                    logger.warning("⚠️ Google Cloud Vision: credenciales no encontradas")
                    self.enabled = False
            except Exception as e:
                logger.error(f"❌ Error inicializando Google Vision: {str(e)}")
                self.enabled = False
    
    async def detect_text_from_image(self, image_content: bytes, language_hint: str = "es") -> Dict[str, Any]:
        """
        Detecta texto en una imagen (OCR)
        Args:
            image_content: Contenido de la imagen en bytes
            language_hint: Idioma esperado (es, en, pt)
        Returns:
            Dict con texto detectado, confianza y metadata
        """
        if not self.enabled or not self.client:
            return {
                "success": False,
                "error": "Google Cloud Vision no está disponible. Necesita configurar GOOGLE_APPLICATION_CREDENTIALS",
                "full_text": "",
                "confidence": 0.0
            }
        
        try:
            image = vision.Image(content=image_content)
            
            # Contexto de imagen con hint de idioma
            image_context = vision.ImageContext(language_hints=[language_hint])
            
            # Detectar texto usando DOCUMENT_TEXT_DETECTION (mejor para documentos/facturas)
            response = self.client.document_text_detection(
                image=image,
                image_context=image_context
            )
            
            if response.error.message:
                logger.error(f"Vision API error: {response.error.message}")
                return {
                    "success": False,
                    "error": response.error.message,
                    "full_text": "",
                    "confidence": 0.0
                }
            
            # Extraer texto completo
            full_text = ""
            if response.full_text_annotation:
                full_text = response.full_text_annotation.text
            
            # Calcular confianza promedio
            confidence = 0.95  # Vision API típicamente tiene alta confianza
            if response.text_annotations and len(response.text_annotations) > 1:
                # Tomar confianza del primer bloque significativo
                confidence = getattr(response.text_annotations[1], 'confidence', 0.95)
            
            logger.info(f"✅ OCR completado: {len(full_text)} caracteres detectados")
            
            return {
                "success": True,
                "full_text": full_text,
                "confidence": confidence,
                "language_detected": language_hint,
                "char_count": len(full_text),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error en OCR: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "full_text": "",
                "confidence": 0.0
            }


class CryptoDataService:
    """Servicio de datos de criptomonedas usando CoinGecko"""
    
    def __init__(self):
        self.client = None
        self.enabled = COINGECKO_AVAILABLE
        self.cache = {}
        self.cache_ttl = 60  # 60 segundos de cache
        
        if self.enabled:
            try:
                # Siempre usar versión gratuita sin API key
                self.client = CoinGeckoAPI()
                logger.info("✅ CoinGecko API inicializada correctamente (versión gratuita)")
            except Exception as e:
                logger.error(f"❌ Error inicializando CoinGecko: {str(e)}")
                self.enabled = False
    
    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Obtener datos del cache si no están expirados"""
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if (datetime.now(timezone.utc) - timestamp).total_seconds() < self.cache_ttl:
                return cached_data
        return None
    
    def _set_cache(self, key: str, data: Dict):
        """Guardar datos en cache"""
        self.cache[key] = (data, datetime.now(timezone.utc))
    
    async def get_crypto_price(self, coin_id: str = "bitcoin", vs_currency: str = "usd") -> Dict[str, Any]:
        """
        Obtener precio actual de una criptomoneda
        Args:
            coin_id: ID de la moneda (bitcoin, ethereum, binancecoin, etc.)
            vs_currency: Moneda de referencia (usd, eur, etc.)
        """
        if not self.enabled or not self.client:
            return {
                "success": False,
                "error": "CoinGecko API no está disponible",
                "price": 0.0
            }
        
        cache_key = f"price_{coin_id}_{vs_currency}"
        cached = self._get_from_cache(cache_key)
        if cached:
            logger.info(f"📦 Cache hit para {cache_key}")
            return cached
        
        try:
            data = self.client.get_price(
                ids=coin_id,
                vs_currencies=vs_currency,
                include_24hr_change=True,
                include_market_cap=True,
                include_24hr_vol=True
            )
            
            if coin_id not in data:
                return {
                    "success": False,
                    "error": f"Moneda '{coin_id}' no encontrada",
                    "price": 0.0
                }
            
            result = {
                "success": True,
                "coin_id": coin_id,
                "price": data[coin_id][vs_currency],
                "price_change_24h": data[coin_id].get(f"{vs_currency}_24h_change", 0),
                "market_cap": data[coin_id].get(f"{vs_currency}_market_cap", 0),
                "volume_24h": data[coin_id].get(f"{vs_currency}_24h_vol", 0),
                "currency": vs_currency.upper(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            self._set_cache(cache_key, result)
            logger.info(f"✅ Precio de {coin_id}: {result['price']} {vs_currency.upper()}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo precio de {coin_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "price": 0.0
            }
    
    async def get_top_cryptocurrencies(self, limit: int = 50) -> Dict[str, Any]:
        """Obtener top criptomonedas por market cap"""
        if not self.enabled or not self.client:
            return {
                "success": False,
                "error": "CoinGecko API no está disponible",
                "coins": []
            }
        
        cache_key = f"top_coins_{limit}"
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            data = self.client.get_coins_markets(
                vs_currency='usd',
                order='market_cap_desc',
                per_page=limit,
                page=1,
                sparkline=False,
                price_change_percentage='24h'
            )
            
            result = {
                "success": True,
                "count": len(data),
                "coins": [
                    {
                        "id": coin['id'],
                        "name": coin['name'],
                        "symbol": coin['symbol'].upper(),
                        "price": coin['current_price'],
                        "market_cap_rank": coin['market_cap_rank'],
                        "market_cap": coin['market_cap'],
                        "price_change_24h": coin.get('price_change_percentage_24h', 0),
                        "volume_24h": coin['total_volume']
                    }
                    for coin in data
                ],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            self._set_cache(cache_key, result)
            logger.info(f"✅ Top {limit} criptomonedas obtenidas")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo top cryptos: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "coins": []
            }


class BlockchainDataService:
    """Servicio de datos blockchain (Etherscan y BSCScan)"""
    
    def __init__(self):
        self.eth_client = None
        self.bsc_client = None
        self.eth_enabled = ETHERSCAN_AVAILABLE
        self.bsc_enabled = False  # BSCScan requiere librería separada
        
        if self.eth_enabled:
            try:
                etherscan_key = os.getenv('ETHERSCAN_API_KEY', 'YourApiKeyToken')
                self.eth_client = Etherscan(etherscan_key)
                logger.info("✅ Etherscan API inicializada")
            except Exception as e:
                logger.error(f"❌ Error inicializando Etherscan: {str(e)}")
                self.eth_enabled = False
    
    async def get_eth_balance(self, address: str) -> Dict[str, Any]:
        """Obtener balance de ETH de una dirección"""
        if not self.eth_enabled or not self.eth_client:
            return {
                "success": False,
                "error": "Etherscan API no está disponible",
                "balance_eth": 0.0
            }
        
        try:
            balance_wei = self.eth_client.get_eth_balance(address=address)
            balance_eth = int(balance_wei) / 1e18
            
            logger.info(f"✅ Balance ETH de {address[:10]}...: {balance_eth} ETH")
            return {
                "success": True,
                "address": address,
                "balance_wei": balance_wei,
                "balance_eth": balance_eth,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Error obteniendo balance ETH: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "balance_eth": 0.0
            }
    
    async def verify_transaction(self, tx_hash: str, network: str = "ethereum") -> Dict[str, Any]:
        """
        Verificar estado de una transacción
        Args:
            tx_hash: Hash de la transacción
            network: "ethereum" o "bsc"
        """
        if network == "ethereum" and self.eth_enabled and self.eth_client:
            try:
                tx_receipt = self.eth_client.get_tx_receipt_status(txhash=tx_hash)
                logger.info(f"✅ Transacción {tx_hash[:10]}... verificada")
                return {
                    "success": True,
                    "tx_hash": tx_hash,
                    "status": tx_receipt.get('status', '0'),
                    "is_success": tx_receipt.get('status') == '1',
                    "network": "ethereum",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            except Exception as e:
                logger.error(f"❌ Error verificando transacción: {str(e)}")
                return {
                    "success": False,
                    "error": str(e)
                }
        else:
            return {
                "success": False,
                "error": f"Red '{network}' no soportada o API no disponible"
            }


class GoogleOAuthService:
    """Servicio de OAuth 2.0 para Google Calendar, Sheets y Blogger"""
    
    def __init__(self):
        self.enabled = GOOGLE_APIS_AVAILABLE
        self.client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
        self.redirect_uri = os.getenv('GOOGLE_OAUTH_REDIRECT_URI')
        self.scopes = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/blogger'
        ]
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.warning("⚠️ Google OAuth: credenciales no configuradas")
            self.enabled = False
    
    def get_authorization_url(self) -> Dict[str, Any]:
        """
        Obtener URL de autorización para que el usuario autorice la app
        El usuario debe visitar esta URL y autorizar, luego será redirigido a redirect_uri
        """
        if not self.enabled:
            return {
                "success": False,
                "error": "Google OAuth no está configurado",
                "auth_url": ""
            }
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            auth_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            
            logger.info("✅ URL de autorización Google OAuth generada")
            return {
                "success": True,
                "auth_url": auth_url,
                "state": state,
                "message": "El usuario debe visitar esta URL para autorizar el acceso"
            }
        except Exception as e:
            logger.error(f"❌ Error generando URL de autorización: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "auth_url": ""
            }


# Instancia global de servicios
vision_service = GoogleVisionService()
crypto_service = CryptoDataService()
blockchain_service = BlockchainDataService()
google_oauth_service = GoogleOAuthService()
