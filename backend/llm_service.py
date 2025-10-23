"""
LLM Service - Servicio compartido para integración con Claude, GPT y Gemini
"""
import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

class LLMService:
    def __init__(self, provider="anthropic", model="claude-3-7-sonnet-20250219"):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.provider = provider
        self.model = model
    
    async def chat(self, message: str, system_message: str = "You are a helpful AI assistant.", session_id: str = "default"):
        """Send a chat message and get response"""
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            ).with_model(self.provider, self.model)
            
            user_message = UserMessage(text=message)
            response = await chat.send_message(user_message)
            
            return {
                'success': True,
                'response': response,
                'provider': self.provider,
                'model': self.model
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_blog(self, topic: str, keywords: str, tone: str = "professional", length: str = "medium"):
        """Generate blog content"""
        word_counts = {
            'short': 500,
            'medium': 1000,
            'long': 2000
        }
        
        word_count = word_counts.get(length, 1000)
        
        system_message = """Eres un experto en marketing de contenidos y SEO. 
        Generas contenido de alta calidad, bien estructurado y optimizado para motores de búsqueda."""
        
        prompt = f"""Genera un artículo de blog completo sobre: {topic}

Palabras clave a incluir: {keywords}
Tono: {tone}
Longitud aproximada: {word_count} palabras

El artículo debe incluir:
1. Título atractivo y optimizado para SEO
2. Meta descripción (150-160 caracteres)
3. Introducción enganchadora
4. 3-5 secciones con subtítulos H2
5. Conclusión con call-to-action
6. Sugerencias de imágenes

Formato en Markdown."""

        return await self.chat(prompt, system_message, f"blog_{topic[:20]}")
    
    async def technical_consultation(self, question: str, session_id: str):
        """Technical consultation with specialized knowledge"""
        system_message = """Eres un consultor técnico senior especializado en:
        - Arquitectura de software y diseño de sistemas
        - Cloud computing (AWS, Azure, GCP)
        - DevOps y CI/CD
        - Bases de datos (SQL y NoSQL)
        - Seguridad informática
        - Desarrollo full-stack
        - Inteligencia Artificial y Machine Learning
        
        Proporciona respuestas técnicas detalladas, con ejemplos de código cuando sea apropiado,
        y mejores prácticas de la industria."""
        
        return await self.chat(question, system_message, session_id)
    
    async def analyze_cv(self, cv_text: str, position: str = ""):
        """Analyze CV/Resume and extract information"""
        system_message = """Eres un experto en recursos humanos y análisis de currículums.
        Extrae información clave y proporciona un análisis objetivo."""
        
        prompt = f"""Analiza el siguiente CV{' para la posición de ' + position if position else ''}:

{cv_text}

Proporciona:
1. Nombre completo del candidato
2. Email y teléfono
3. Años de experiencia
4. Habilidades principales
5. Nivel educativo
6. Puntuación del 0-100 (considera experiencia, habilidades, educación)
7. Fortalezas y debilidades
8. Recomendación (contratar, entrevistar, descartar)

Responde en formato JSON."""

        return await self.chat(prompt, system_message, f"cv_analysis_{position}")
    
    async def extract_invoice_data(self, invoice_text: str):
        """Extract data from invoice text (OCR result)"""
        system_message = """Eres un experto en procesamiento de facturas y documentos contables.
        Extrae información estructurada de facturas."""
        
        prompt = f"""Extrae los siguientes datos de esta factura:

{invoice_text}

Información requerida:
1. RUC del emisor
2. Razón social
3. Fecha de emisión
4. Monto total (sin IVA)
5. Monto de IVA
6. Monto total con IVA
7. Descripción de productos/servicios
8. Número de factura

Responde en formato JSON con estos campos exactos."""

        return await self.chat(prompt, system_message, "invoice_extraction")
    
    async def generate_social_media_post(self, topic: str, platform: str, tone: str = "professional"):
        """Generate social media post"""
        platform_guides = {
            'facebook': 'Post de Facebook (máximo 300 caracteres, informal y enganchador)',
            'instagram': 'Caption de Instagram (con hashtags relevantes, máximo 200 caracteres)',
            'twitter': 'Tweet (máximo 280 caracteres, conciso e impactante)',
            'linkedin': 'Post de LinkedIn (profesional, máximo 1300 caracteres)'
        }
        
        guide = platform_guides.get(platform.lower(), 'Post de redes sociales')
        
        system_message = f"""Eres un experto en marketing de redes sociales.
        Creas contenido viral y enganchador."""
        
        prompt = f"""Crea un {guide} sobre: {topic}
        
Tono: {tone}
Incluye call-to-action y hashtags relevantes (si aplica).
Solo el texto del post, sin explicaciones adicionales."""

        return await self.chat(prompt, system_message, f"social_{platform}")
    
    async def find_leads(self, industry: str, location: str, size: str = ""):
        """Generate lead search strategy and insights"""
        system_message = """Eres un experto en prospección comercial y generación de leads.
        Proporciona estrategias detalladas para encontrar clientes potenciales."""
        
        prompt = f"""Proporciona una estrategia de prospección para:

Industria: {industry}
Ubicación: {location}
{f'Tamaño de empresa: {size}' if size else ''}

Incluye:
1. Mejores canales para encontrar leads en esta industria
2. Keywords de búsqueda recomendadas
3. Perfil ideal del decision maker
4. Estrategia de acercamiento
5. Mensaje de prospección inicial (template)

Responde de forma estructurada."""

        return await self.chat(prompt, system_message, f"lead_search_{industry}")


# Singleton instance
llm_service = LLMService()
