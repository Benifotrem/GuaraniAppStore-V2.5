"""
Blog Generator Service - Sistema automatizado de generación de artículos
Genera artículos de blog con IA usando OpenRouter (Claude 3.5 Sonnet + Gemini 2.5 Flash)
Incluye generación programada (7/semana) y bajo demanda (admin panel)
"""

import os
import httpx
import json
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from models import BlogPost
from database import get_db

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_EXTENDED_API_KEY = os.environ.get('OPENROUTER_EXTENDED_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Agentes con sus especialidades
AGENTS = {
    1: {
        "name": "Junior Cucurella",
        "role": "Especialista en Automatización WhatsApp",
        "expertise": "automatización, whatsapp business, chatbots, workflows",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/bgnarl3b_Junior%20Cucurella.png",
        "day": 0  # Lunes
    },
    2: {
        "name": "Jacinto Torrelavega",
        "role": "Experto en E-commerce y Shopify",
        "expertise": "e-commerce, shopify, tiendas online, ventas, conversión",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/vj2qbxyp_Jacinto%20Torrelavega.png",
        "day": 1  # Martes
    },
    3: {
        "name": "Alex Albiol",
        "role": "Estratega de Marketing Digital",
        "expertise": "marketing digital, redes sociales, publicidad, estrategia",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/inyaz3yz_Alex%20Albiol.png",
        "day": 2  # Miércoles
    },
    4: {
        "name": "Silvia Garcia",
        "role": "Especialista SEO y Content",
        "expertise": "seo, optimización, posicionamiento web, contenido, google",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/d46a0zdu_Silvia%20Garcia.png",
        "day": 3  # Jueves
    },
    5: {
        "name": "Blanca Garcia",
        "role": "Consultora de Procesos Empresariales",
        "expertise": "procesos, optimización, eficiencia, gestión empresarial",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/rra6yz0p_Blanca%20Garcia.png",
        "day": 4  # Viernes
    },
    6: {
        "name": "Rocío Almeida",
        "role": "Líder en Prospección Comercial",
        "expertise": "prospección, ventas, leads, generación de oportunidades",
        "avatar": "https://customer-assets.emergentagent.com/job_dd41205c-0563-410b-b982-82b058b7bad9/artifacts/kbxdkg6k_Rocio%20Almeida.png",
        "day": 5  # Sábado
    },
    0: {
        "name": "CEO - GuaraniAppStore",
        "role": "Director Ejecutivo",
        "expertise": "estrategia, liderazgo, visión empresarial, transformación digital",
        "avatar": None,
        "day": 6  # Domingo
    }
}

# Texto promocional de Bitfinex (al final de cada artículo)
BITFINEX_PROMO = """

---

## ¿Sabes cómo comprar Bitcoin de forma segura?

Si estás buscando una plataforma confiable para comenzar tu viaje en el mundo de las criptomonedas, **Bitfinex** es tu mejor opción. Con años de experiencia en el mercado y las más altas medidas de seguridad, Bitfinex te permite comprar Bitcoin de manera sencilla y segura.

¿Por qué elegir Bitfinex?
- 🔒 **Máxima seguridad** para tus activos digitales
- 💰 **Bajas comisiones** en cada transacción
- 🌍 **Plataforma global** con soporte en múltiples idiomas
- 📱 **Fácil de usar** desde cualquier dispositivo

**[Regístrate ahora en Bitfinex y comienza a invertir en Bitcoin](https://www.bitfinex.com/sign-up?refcode=_FfVSXR-a)**

No dejes pasar la oportunidad de formar parte de la revolución financiera. ¡El futuro es ahora!

"""


class BlogGeneratorService:
    """Servicio para generar artículos de blog con IA"""
    
    def __init__(self):
        self.text_api_key = OPENROUTER_API_KEY
        self.image_api_key = OPENROUTER_EXTENDED_API_KEY
        
    def _create_slug(self, title: str) -> str:
        """Crea un slug URL-friendly desde el título"""
        # Normalizar título
        slug = title.lower()
        # Reemplazar caracteres especiales
        slug = re.sub(r'[áàäâ]', 'a', slug)
        slug = re.sub(r'[éèëê]', 'e', slug)
        slug = re.sub(r'[íìïî]', 'i', slug)
        slug = re.sub(r'[óòöô]', 'o', slug)
        slug = re.sub(r'[úùüû]', 'u', slug)
        slug = re.sub(r'[ñ]', 'n', slug)
        # Reemplazar espacios y caracteres no alfanuméricos con guiones
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Eliminar guiones al inicio y final
        slug = slug.strip('-')
        return slug
    
    def _calculate_reading_time(self, content: str) -> int:
        """Calcula el tiempo estimado de lectura en minutos"""
        words = len(content.split())
        return max(1, round(words / 200))  # 200 palabras por minuto
    
    def _detect_agent_from_query(self, search_query: str) -> int:
        """
        Detecta automáticamente qué agente debe escribir el artículo
        basándose en la consulta de búsqueda
        """
        query_lower = search_query.lower()
        
        # Calcular score para cada agente
        scores = {}
        for agent_id, agent_data in AGENTS.items():
            if agent_id == 0:  # Skip CEO
                continue
            
            keywords = agent_data['expertise'].split(', ')
            score = sum(1 for keyword in keywords if keyword in query_lower)
            scores[agent_id] = score
        
        # Retornar el agente con mayor score, o random si empate
        best_agent = max(scores, key=scores.get)
        return best_agent if scores[best_agent] > 0 else 1  # Default: Junior
    
    async def generate_article_content(
        self,
        topic: str,
        agent_id: int,
        tone: str = "profesional",
        length: str = "medium",
        keywords: List[str] = None,
        include_faq: bool = True
    ) -> Dict:
        """
        Genera el contenido de un artículo usando Claude 3.5 Sonnet
        
        Args:
            topic: Tema del artículo
            agent_id: ID del agente (0-6)
            tone: Tono del artículo (profesional, casual, técnico)
            length: Longitud (short=800, medium=1200, long=1500 palabras)
            keywords: Lista de keywords objetivo
            include_faq: Incluir sección FAQ
        """
        agent = AGENTS[agent_id]
        
        # Determinar longitud objetivo
        word_counts = {
            "short": 800,
            "medium": 1200,
            "long": 1500
        }
        target_words = word_counts.get(length, 1200)
        
        # Construir prompt
        keywords_str = ", ".join(keywords) if keywords else "N/A"
        faq_instruction = "\n\n- INCLUIR una sección final de '## Preguntas Frecuentes (FAQ)' con 5 preguntas y respuestas relevantes." if include_faq else ""
        
        prompt = f"""Eres {agent['name']}, {agent['role']} en GuaraniAppStore.

Tu expertise: {agent['expertise']}

TAREA: Escribir un artículo de blog optimizado SEO sobre: "{topic}"

IMPORTANTE: Estamos en el año 2025. Todos los datos, ejemplos, y referencias deben ser actuales a 2025.

REQUISITOS:
- Longitud objetivo: ~{target_words} palabras
- Tono: {tone}
- Keywords principales a incluir naturalmente: {keywords_str}
- Formato: Markdown profesional
- Año actual: 2025
- Estructura:
  * Título atractivo (H1)
  * Extracto/resumen inicial (2-3 líneas)
  * Introducción engagement
  * 4-6 secciones principales con subtítulos (H2)
  * Conclusión con call-to-action
  {faq_instruction}

OPTIMIZACIÓN SEO:
- Incluir keywords naturalmente en título, subtítulos y contenido
- Usar listas, bullets, negritas para lectura fácil
- Lenguaje claro y directo
- Ejemplos prácticos y casos de uso
- Datos y estadísticas relevantes (si aplica)

ESTILO:
- Escribir desde tu perspectiva como experto
- Usar primera persona cuando sea apropiado
- Lenguaje accesible pero profesional
- Enfoque práctico y accionable
- Para audiencia hispanohablante (Paraguay, Latinoamérica)

FORMATO MARKDOWN ESTRICTO (MUY IMPORTANTE):
- Título principal con # (H1)
- Subtítulos con ## (H2) para cada sección principal
- Sub-subtítulos con ### (H3) si es necesario
- Cada párrafo DEBE estar separado por UNA línea en blanco
- Párrafos cortos: máximo 4 líneas cada uno
- Usar listas con - para bullets
- Usar negritas **texto** para énfasis
- Espaciar generosamente entre secciones

ESTRUCTURA OBLIGATORIA:
# Título Principal

Extracto introductorio de 2-3 líneas que resuma el artículo.

Primer párrafo del contenido. Debe ser conciso y directo.

Segundo párrafo continuando la idea. Mantener espaciado entre párrafos.

## Primera Sección Principal

Párrafo explicativo de la sección.

Otro párrafo con más detalles.

- Bullet point 1
- Bullet point 2
- Bullet point 3

## Segunda Sección Principal

Contenido de la segunda sección...

IMPORTANTE: NO incluir meta-información. Solo el contenido del artículo con formato Markdown correcto.
"""
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.text_api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://guaraniappstore.com",
                        "X-Title": "GuaraniAppStore Blog"
                    },
                    json={
                        "model": "tngtech/deepseek-r1t2-chimera:free",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 4000,
                        "temperature": 0.7
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                content = result['choices'][0]['message']['content']
                
                # Extraer título del markdown (buscar la primera línea con #)
                lines = content.split('\n')
                title = ""
                content_start_index = 0
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('# ') and len(line.strip()) > 2:
                        title = line.replace('# ', '').strip()
                        content_start_index = i
                        break
                
                # Si no se encontró título, usar el topic como título
                if not title:
                    title = topic
                    # Agregar título al inicio del contenido
                    content = f"# {title}\n\n{content}"
                
                # Extraer excerpt (primeras 2-3 líneas después del título que no sean vacías)
                content_lines = [l.strip() for l in lines[content_start_index+1:] if l.strip() and not l.strip().startswith('#')]
                excerpt = ' '.join(content_lines[:2]).strip()
                if len(excerpt) > 300:
                    excerpt = excerpt[:297] + "..."
                elif len(excerpt) < 50 and len(content_lines) > 2:
                    # Si el excerpt es muy corto, tomar más líneas
                    excerpt = ' '.join(content_lines[:3]).strip()
                    if len(excerpt) > 300:
                        excerpt = excerpt[:297] + "..."
                
                return {
                    "title": title,
                    "excerpt": excerpt,
                    "content": content,
                    "success": True
                }
                
        except Exception as e:
            print(f"Error generando artículo: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_image(self, article_content: str, article_title: str) -> Dict:
        """
        Genera una imagen para el artículo usando Gemini 2.5 Flash
        Basada en el CONTENIDO completo del artículo para representación gráfica precisa
        
        Args:
            article_content: Contenido completo del artículo
            article_title: Título del artículo
        """
        # Extraer conceptos clave del contenido (primeros 500 caracteres)
        content_preview = article_content[:500] if len(article_content) > 500 else article_content
        
        # Crear prompt para la imagen basado en el contenido
        image_prompt = f"""Genera una imagen profesional que represente gráficamente el siguiente artículo de blog:

TÍTULO: {article_title}

CONTENIDO (extracto):
{content_preview}

REQUISITOS:
- Crear una representación visual que capture la ESENCIA del artículo
- Estilo: Profesional, corporativo, tecnológico, moderno
- Colores: Vibrantes pero profesionales (azul, verde, turquesa)
- Elementos visuales: Relacionados específicamente con los conceptos del artículo
- Composición: Limpia, minimalista, con espacio negativo
- NO incluir: Texto legible, logos específicos, rostros de personas reales
- Formato: Landscape 16:9, alta calidad

La imagen debe ILUSTRAR VISUALMENTE los conceptos principales del artículo."""
        
        try:
            # Usar Google Gemini 2.5 Flash Image via OpenRouter para generar imágenes
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Intentar con ambas API keys
                api_keys_to_try = [self.image_api_key, self.text_api_key]
                last_error = None
                
                for api_key in api_keys_to_try:
                    if not api_key:
                        continue
                        
                    try:
                        response = await client.post(
                            f"{OPENROUTER_BASE_URL}/chat/completions",
                            headers={
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "https://guaraniappstore.com",
                                "X-Title": "GuaraniAppStore Blog"
                            },
                            json={
                                "model": "openai/gpt-5-image-mini",
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": image_prompt
                                    }
                                ]
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            break
                        else:
                            last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                            continue
                            
                    except Exception as e:
                        last_error = str(e)
                        continue
                
                # Si llegamos aquí y no hay result, lanzar error
                if not 'result' in locals():
                    raise Exception(f"Todas las API keys fallaron. Último error: {last_error}")
                
                # Extraer URL de la imagen generada
                if 'choices' in result and len(result['choices']) > 0:
                    message_content = result['choices'][0]['message']['content']
                    
                    # La respuesta puede contener la URL de la imagen o markdown con imagen
                    # Buscar URL de imagen en el contenido
                    import re
                    url_match = re.search(r'https?://[^\s\)]+\.(jpg|jpeg|png|webp)', message_content)
                    
                    if url_match:
                        image_url = url_match.group(0)
                        print(f"✅ Imagen generada exitosamente: {image_url[:80]}...")
                        return {
                            "success": True,
                            "image_url": image_url,
                            "image_prompt": image_prompt
                        }
                    else:
                        # Si no hay URL, el modelo podría haber retornado base64 o texto
                        print(f"⚠️ Respuesta del modelo no contiene URL de imagen")
                        print(f"   Contenido: {message_content[:200]}")
                        raise Exception("No se encontró URL de imagen en respuesta")
                else:
                    raise Exception("Respuesta sin choices")
                
        except Exception as e:
            print(f"⚠️ No se pudo generar imagen con IA: {str(e)}")
            print(f"   Usando imagen profesional placeholder")
            
            # Usar imágenes profesionales de Unsplash relacionadas con tecnología
            # Rotación de imágenes según día para variedad
            from datetime import datetime
            day = datetime.now().day
            
            # Colección de imágenes profesionales de tecnología/negocios
            professional_images = [
                "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&h=630&fit=crop",  # Tech abstract
                "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=1200&h=630&fit=crop",  # Team working
                "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&h=630&fit=crop",  # Laptop minimal
                "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=630&fit=crop",  # Analytics
                "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop",  # Charts data
                "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=1200&h=630&fit=crop",  # AI concept
                "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?w=1200&h=630&fit=crop",  # Laptop desk
            ]
            
            # Seleccionar imagen según día
            image_index = day % len(professional_images)
            selected_image = professional_images[image_index]
            
            return {
                "success": True,
                "image_url": selected_image,
                "image_prompt": image_prompt
            }
    
    async def generate_scheduled_article(self, day_of_week: int, db: Session) -> Optional[BlogPost]:
        """
        Genera un artículo programado para un día específico
        
        Args:
            day_of_week: Día de la semana (0=Monday, 6=Sunday)
            db: Database session
        """
        # Obtener agente para este día
        agent_id = None
        for aid, agent_data in AGENTS.items():
            if agent_data['day'] == day_of_week:
                agent_id = aid
                break
        
        if agent_id is None:
            print(f"No hay agente asignado para el día {day_of_week}")
            return None
        
        agent = AGENTS[agent_id]
        
        # Temas generales basados en expertise del agente
        topics_by_agent = {
            1: ["Automatización de WhatsApp Business 2025", "Chatbots que Generan Ventas", "WhatsApp API: Casos de Éxito"],
            2: ["Optimización de Conversión en Shopify", "E-commerce Trends 2025", "Automatizar Tienda Online"],
            3: ["Marketing Digital con IA", "Estrategias de Redes Sociales 2025", "ROI en Publicidad Digital"],
            4: ["SEO con Inteligencia Artificial", "Posicionamiento Web en 2025", "Content Marketing que Convierte en 2025"],
            5: ["Optimización de Procesos Empresariales", "Eficiencia Operacional con IA", "Gestión Empresarial Moderna"],
            6: ["Prospección Comercial Automatizada", "Lead Generation con IA", "Ventas B2B en la Era Digital"],
            0: ["Transformación Digital Empresarial", "Futuro de la IA en Negocios", "Liderazgo en la Era de la IA"]
        }
        
        import random
        topic = random.choice(topics_by_agent.get(agent_id, ["Innovación con IA en Negocios"]))
        
        # Generar artículo
        article_data = await self.generate_article_content(
            topic=topic,
            agent_id=agent_id,
            tone="profesional",
            length="medium",
            keywords=[],
            include_faq=True
        )
        
        if not article_data['success']:
            print(f"Error generando artículo: {article_data.get('error')}")
            return None
        
        # Generar imagen basada en el contenido completo
        image_data = await self.generate_image(
            article_content=article_data['content'],
            article_title=article_data['title']
        )
        
        # Insertar imagen anidada al inicio del contenido (después del extracto)
        content_with_image = article_data['content']
        if image_data.get('image_url'):
            # Obtener el día del mes para determinar float left/right
            from datetime import datetime
            day = datetime.now().day
            float_direction = 'right' if day % 2 == 0 else 'left'
            
            # Estilos inline fuertes para garantizar el float
            if float_direction == 'left':
                inline_style = 'float: left; margin: 0 2rem 1.5rem 0; max-width: 45%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'
            else:
                inline_style = 'float: right; margin: 0 0 1.5rem 2rem; max-width: 45%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'
            
            # Insertar imagen después del extracto (después de las primeras 3-4 líneas)
            lines = content_with_image.split('\n')
            # Buscar después del título y extracto (aproximadamente línea 4-5)
            insert_index = 4
            for i, line in enumerate(lines):
                if i > 3 and line.strip() != '' and not line.startswith('#'):
                    insert_index = i
                    break
            
            # HTML con estilos inline fuertes
            image_html = f'\n\n<img src="{image_data["image_url"]}" alt="{article_data["title"]}" style="{inline_style}" />\n\n'
            lines.insert(insert_index, image_html)
            content_with_image = '\n'.join(lines)
        
        # Agregar firma del autor
        agent = AGENTS[agent_id]
        author_signature = f"""

---

**Escrito por {agent['name']}**  
*{agent['role']}*

"""
        if agent.get('avatar'):
            author_signature = f"""

---

<div style="display: flex; align-items: center; gap: 1rem; padding: 1.5rem; background: #f9fafb; border-radius: 8px; margin: 2rem 0;">
  <img src="{agent['avatar']}" alt="{agent['name']}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;" />
  <div>
    <strong style="font-size: 1.1rem; color: #111827;">{agent['name']}</strong><br/>
    <em style="color: #6b7280;">{agent['role']}</em>
  </div>
</div>

"""
        
        # Agregar promoción de Bitfinex al final
        full_content = content_with_image + author_signature + BITFINEX_PROMO
        
        # Crear BlogPost
        blog_post = BlogPost(
            title=article_data['title'],
            slug=self._create_slug(article_data['title']),
            excerpt=article_data['excerpt'],
            content=full_content,
            image_url=image_data.get('image_url'),
            image_prompt=image_data.get('image_prompt'),
            author_name=agent['name'],
            author_role=agent['role'],
            author_avatar=agent.get('avatar'),
            author_id=agent_id,
            day_of_week=day_of_week,
            meta_description=article_data['excerpt'][:160],
            tags=[],
            keywords=[],
            published=True,  # Artículos programados se publican automáticamente
            published_at=datetime.now(timezone.utc),
            pending_approval=False,
            generation_type='scheduled',
            reading_time=self._calculate_reading_time(full_content)
        )
        
        db.add(blog_post)
        db.commit()
        db.refresh(blog_post)
        
        print(f"✅ Artículo programado generado: {blog_post.title} por {agent['name']}")
        return blog_post
    
    async def generate_custom_article(
        self,
        search_query: str,
        target_keywords: List[str],
        agent_id: Optional[int],
        tone: str,
        length: str,
        include_faq: bool,
        db: Session
    ) -> Optional[BlogPost]:
        """
        Genera un artículo personalizado bajo demanda (Panel Admin)
        
        Args:
            search_query: Consulta de búsqueda del admin
            target_keywords: Keywords objetivo
            agent_id: ID del agente (None = detectar automáticamente)
            tone: Tono del artículo
            length: Longitud del artículo
            include_faq: Incluir FAQ
            db: Database session
        """
        # Detectar agente si no se especifica
        if agent_id is None:
            agent_id = self._detect_agent_from_query(search_query)
        
        agent = AGENTS[agent_id]
        
        # Generar artículo
        article_data = await self.generate_article_content(
            topic=search_query,
            agent_id=agent_id,
            tone=tone,
            length=length,
            keywords=target_keywords,
            include_faq=include_faq
        )
        
        if not article_data['success']:
            print(f"Error generando artículo: {article_data.get('error')}")
            return None
        
        # Generar imagen basada en el contenido completo
        image_data = await self.generate_image(
            article_content=article_data['content'],
            article_title=article_data['title']
        )
        
        # Insertar imagen anidada al inicio del contenido (después del extracto)
        content_with_image = article_data['content']
        if image_data.get('image_url'):
            # Obtener el día del mes para determinar float left/right
            from datetime import datetime
            day = datetime.now().day
            float_direction = 'right' if day % 2 == 0 else 'left'
            
            # Estilos inline fuertes para garantizar el float
            if float_direction == 'left':
                inline_style = 'float: left; margin: 0 2rem 1.5rem 0; max-width: 45%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'
            else:
                inline_style = 'float: right; margin: 0 0 1.5rem 2rem; max-width: 45%; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'
            
            # Insertar imagen después del extracto (después de las primeras 3-4 líneas)
            lines = content_with_image.split('\n')
            # Buscar después del título y extracto (aproximadamente línea 4-5)
            insert_index = 4
            for i, line in enumerate(lines):
                if i > 3 and line.strip() != '' and not line.startswith('#'):
                    insert_index = i
                    break
            
            # HTML con estilos inline fuertes
            image_html = f'\n\n<img src="{image_data["image_url"]}" alt="{article_data["title"]}" style="{inline_style}" />\n\n'
            lines.insert(insert_index, image_html)
            content_with_image = '\n'.join(lines)
        
        # Agregar firma del autor
        agent = AGENTS[agent_id]
        author_signature = f"""

---

**Escrito por {agent['name']}**  
*{agent['role']}*

"""
        if agent.get('avatar'):
            author_signature = f"""

---

<div style="display: flex; align-items: center; gap: 1rem; padding: 1.5rem; background: #f9fafb; border-radius: 8px; margin: 2rem 0;">
  <img src="{agent['avatar']}" alt="{agent['name']}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;" />
  <div>
    <strong style="font-size: 1.1rem; color: #111827;">{agent['name']}</strong><br/>
    <em style="color: #6b7280;">{agent['role']}</em>
  </div>
</div>

"""
        
        # Agregar promoción de Bitfinex al final
        full_content = content_with_image + author_signature + BITFINEX_PROMO
        
        # Crear BlogPost (en cola de aprobación)
        blog_post = BlogPost(
            title=article_data['title'],
            slug=self._create_slug(article_data['title']),
            excerpt=article_data['excerpt'],
            content=full_content,
            image_url=image_data.get('image_url'),
            image_prompt=image_data.get('image_prompt'),
            author_name=agent['name'],
            author_role=agent['role'],
            author_avatar=agent.get('avatar'),
            author_id=agent_id,
            day_of_week=None,  # Artículos manuales no tienen día asignado
            meta_description=article_data['excerpt'][:160],
            tags=target_keywords[:5],  # Primeros 5 keywords como tags
            keywords=target_keywords,
            published=False,  # No publicar hasta aprobación
            published_at=None,
            pending_approval=True,
            requested_by='admin',
            requested_at=datetime.now(timezone.utc),
            search_query=search_query,
            generation_type='manual',
            reading_time=self._calculate_reading_time(full_content)
        )
        
        db.add(blog_post)
        db.commit()
        db.refresh(blog_post)
        
        print(f"✅ Artículo bajo demanda generado (en cola): {blog_post.title} por {agent['name']}")
        return blog_post


# Singleton instance
blog_generator = BlogGeneratorService()
