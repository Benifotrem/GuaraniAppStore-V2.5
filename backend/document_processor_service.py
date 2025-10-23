"""
GuaraniAppStore V2.5 Pro - Servicio Avanzado de Procesamiento de Documentos
Integración dual: Mistral Pixtral Large (OpenRouter) + Google Cloud Vision
"""

import os
import logging
import base64
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import httpx

# Google Cloud Vision
try:
    from google.cloud import vision
    from google.oauth2 import service_account
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

logger = logging.getLogger(__name__)


class DocumentProcessorService:
    """
    Servicio híbrido de OCR con dos engines:
    1. Mistral Pixtral Large (OpenRouter) - Extracción estructurada con IA
    2. Google Cloud Vision - OCR tradicional de alta precisión
    """
    
    def __init__(self):
        # OpenRouter (Mistral Pixtral)
        self.openrouter_key = os.environ.get('OPENROUTER_API_KEY')
        self.openrouter_extended_key = os.environ.get('OPENROUTER_EXTENDED_API_KEY')
        self.pixtral_model = "mistralai/pixtral-large-latest"
        
        # Google Cloud Vision
        self.vision_client = None
        self.vision_enabled = GOOGLE_VISION_AVAILABLE
        
        if self.vision_enabled:
            try:
                credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
                project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
                
                if credentials_path and os.path.exists(credentials_path):
                    credentials = service_account.Credentials.from_service_account_file(
                        credentials_path
                    )
                    self.vision_client = vision.ImageAnnotatorClient(credentials=credentials)
                    logger.info("✅ Google Cloud Vision inicializado")
                else:
                    logger.warning("⚠️ Google Cloud Vision: credenciales no encontradas")
                    self.vision_enabled = False
            except Exception as e:
                logger.error(f"❌ Error inicializando Google Vision: {str(e)}")
                self.vision_enabled = False
        
        # Verificar OpenRouter
        if not self.openrouter_key:
            logger.warning("⚠️ OPENROUTER_API_KEY no configurada. Pixtral OCR no disponible.")
    
    async def process_with_pixtral(
        self, 
        image_path: str = None,
        image_bytes: bytes = None,
        custom_fields: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Procesar documento con Mistral Pixtral Large (extracción estructurada)
        
        Args:
            image_path: Ruta al archivo de imagen
            image_bytes: Bytes de la imagen
            custom_fields: Campos personalizados a extraer
                Ejemplo: {'fecha': 'Fecha de emisión', 'nombre': 'Nombre del proveedor'}
        
        Returns:
            Dict con datos estructurados extraídos
        """
        if not self.openrouter_key:
            return {
                'success': False,
                'error': 'OpenRouter API key no configurada',
                'extracted_data': {}
            }
        
        try:
            # Leer imagen
            if image_path:
                with open(image_path, 'rb') as f:
                    image_data = f.read()
            elif image_bytes:
                image_data = image_bytes
            else:
                return {
                    'success': False,
                    'error': 'No se proporcionó imagen',
                    'extracted_data': {}
                }
            
            # Convertir imagen a base64
            image_b64 = base64.b64encode(image_data).decode('utf-8')
            
            # Construir prompt para extracción estructurada
            if custom_fields:
                fields_prompt = "\n".join([
                    f"- {key}: {description}"
                    for key, description in custom_fields.items()
                ])
                example_json = json.dumps({k: "valor" for k in custom_fields.keys()}, indent=2)
            else:
                # Campos por defecto para facturas paraguayas
                fields_prompt = """
- fecha: Fecha de emisión
- nombre: Nombre del proveedor o emisor
- ruc: RUC del emisor
- importe: Total a pagar
- concepto: Descripción o concepto principal
- moneda: Moneda (PYG, USD, etc.)
"""
                example_json = '''{
  "fecha": "15/10/2024",
  "nombre": "Distribuidora ABC S.A.",
  "ruc": "80012345-1",
  "importe": "5500000",
  "concepto": "Venta de mercaderías",
  "moneda": "PYG"
}'''
            
            prompt = f"""Extrae la siguiente información de esta factura/documento:

{fields_prompt}

Responde SOLO con un JSON válido, sin texto adicional ni markdown.
Ejemplo de formato esperado:
{example_json}

Si algún campo no está presente, usa null como valor."""
            
            # Hacer request a OpenRouter
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {self.openrouter_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': self.pixtral_model,
                        'messages': [
                            {
                                'role': 'user',
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': prompt
                                    },
                                    {
                                        'type': 'image_url',
                                        'image_url': {
                                            'url': f'data:image/jpeg;base64,{image_b64}'
                                        }
                                    }
                                ]
                            }
                        ],
                        'temperature': 0.1,  # Baja temperatura para consistencia
                        'max_tokens': 2000
                    }
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ OpenRouter error: {response.status_code} - {response.text}")
                    return {
                        'success': False,
                        'error': f'OpenRouter API error: {response.status_code}',
                        'extracted_data': {}
                    }
                
                data = response.json()
                
                # Extraer contenido de respuesta
                content = data['choices'][0]['message']['content']
                
                # Limpiar respuesta (remover markdown si existe)
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.startswith('```'):
                    content = content[3:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                # Parsear JSON
                try:
                    extracted_data = json.loads(content)
                except json.JSONDecodeError as je:
                    logger.error(f"❌ Error parseando JSON: {str(je)}\nContenido: {content[:200]}")
                    return {
                        'success': False,
                        'error': f'Error parseando respuesta JSON: {str(je)}',
                        'raw_content': content,
                        'extracted_data': {}
                    }
                
                logger.info(f"✅ Pixtral OCR exitoso: {len(extracted_data)} campos extraídos")
                
                return {
                    'success': True,
                    'engine': 'mistral_pixtral_large',
                    'model': self.pixtral_model,
                    'extracted_data': extracted_data,
                    'tokens_used': data.get('usage', {}),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
        
        except Exception as e:
            logger.error(f"❌ Error en Pixtral OCR: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'extracted_data': {}
            }
    
    async def process_with_google_vision(
        self,
        image_bytes: bytes,
        language_hint: str = "es"
    ) -> Dict[str, Any]:
        """
        Procesar documento con Google Cloud Vision (OCR tradicional)
        
        Args:
            image_bytes: Bytes de la imagen
            language_hint: Idioma esperado (es, en, pt)
        
        Returns:
            Dict con texto extraído
        """
        if not self.vision_enabled or not self.vision_client:
            return {
                'success': False,
                'error': 'Google Cloud Vision no disponible',
                'full_text': ''
            }
        
        try:
            image = vision.Image(content=image_bytes)
            
            # Contexto con hint de idioma
            image_context = vision.ImageContext(language_hints=[language_hint])
            
            # Detectar texto con DOCUMENT_TEXT_DETECTION (mejor para documentos)
            response = self.vision_client.document_text_detection(
                image=image,
                image_context=image_context
            )
            
            if response.error.message:
                logger.error(f"Vision API error: {response.error.message}")
                return {
                    'success': False,
                    'error': response.error.message,
                    'full_text': ''
                }
            
            # Extraer texto completo
            full_text = ""
            if response.full_text_annotation:
                full_text = response.full_text_annotation.text
            
            # Calcular confianza
            confidence = 0.95  # Vision API típicamente alta confianza
            if response.text_annotations and len(response.text_annotations) > 1:
                confidence = getattr(response.text_annotations[1], 'confidence', 0.95)
            
            logger.info(f"✅ Google Vision OCR exitoso: {len(full_text)} caracteres")
            
            return {
                'success': True,
                'engine': 'google_cloud_vision',
                'full_text': full_text,
                'confidence': confidence,
                'char_count': len(full_text),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            logger.error(f"❌ Error en Google Vision OCR: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'full_text': ''
            }
    
    async def process_document_hybrid(
        self,
        image_path: str = None,
        image_bytes: bytes = None,
        custom_fields: Optional[Dict[str, str]] = None,
        use_pixtral: bool = True,
        use_google: bool = True
    ) -> Dict[str, Any]:
        """
        Procesar documento con ambos engines y combinar resultados
        
        Args:
            image_path: Ruta al archivo
            image_bytes: Bytes de imagen
            custom_fields: Campos a extraer (para Pixtral)
            use_pixtral: Usar Mistral Pixtral
            use_google: Usar Google Vision
        
        Returns:
            Dict con resultados combinados de ambos engines
        """
        results = {
            'pixtral': None,
            'google_vision': None,
            'combined': {}
        }
        
        # Leer imagen si no se proporcionaron bytes
        if not image_bytes and image_path:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
        
        if not image_bytes:
            return {
                'success': False,
                'error': 'No se proporcionó imagen',
                'results': results
            }
        
        # Procesar con Pixtral (extracción estructurada)
        if use_pixtral and self.openrouter_key:
            pixtral_result = await self.process_with_pixtral(
                image_bytes=image_bytes,
                custom_fields=custom_fields
            )
            results['pixtral'] = pixtral_result
        
        # Procesar con Google Vision (OCR completo)
        if use_google and self.vision_enabled:
            google_result = await self.process_with_google_vision(image_bytes)
            results['google_vision'] = google_result
        
        # Combinar resultados
        if results['pixtral'] and results['pixtral'].get('success'):
            results['combined']['structured_data'] = results['pixtral']['extracted_data']
        
        if results['google_vision'] and results['google_vision'].get('success'):
            results['combined']['full_text'] = results['google_vision']['full_text']
            results['combined']['confidence'] = results['google_vision']['confidence']
        
        # Determinar éxito general
        success = (
            (results['pixtral'] and results['pixtral'].get('success')) or
            (results['google_vision'] and results['google_vision'].get('success'))
        )
        
        return {
            'success': success,
            'engines_used': {
                'pixtral': use_pixtral and bool(self.openrouter_key),
                'google_vision': use_google and self.vision_enabled
            },
            'results': results,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }


# Instancia global
document_processor = DocumentProcessorService()
