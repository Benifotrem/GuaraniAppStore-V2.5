"""
Scraper de noticias RSS para Pulse IA
"""
import feedparser
import asyncio
from datetime import datetime, timezone
from typing import List, Dict
from pulse_config import RSS_FEEDS

class PulseRSSScraper:
    def __init__(self):
        self.feeds = RSS_FEEDS
    
    async def fetch_all_feeds(self) -> List[Dict]:
        """
        Obtener artículos de todos los RSS feeds
        
        Returns:
            List de artículos
        """
        print("📰 Obteniendo artículos de RSS feeds...")
        all_articles = []
        
        for feed_config in self.feeds:
            articles = await self.fetch_feed(feed_config)
            all_articles.extend(articles)
        
        print(f"✅ Total artículos obtenidos: {len(all_articles)}")
        return all_articles
    
    async def fetch_feed(self, feed_config: Dict) -> List[Dict]:
        """
        Obtener artículos de un RSS feed específico
        
        Args:
            feed_config: Dict con configuración del feed
        
        Returns:
            List de artículos
        """
        try:
            # Ejecutar feedparser en thread pool (es blocking)
            loop = asyncio.get_event_loop()
            feed = await loop.run_in_executor(
                None, 
                feedparser.parse, 
                feed_config['url']
            )
            
            articles = []
            
            for entry in feed.entries[:20]:  # Últimos 20 artículos
                article = {
                    'source_name': feed_config['name'],
                    'source_type': 'rss',
                    'title': entry.get('title', ''),
                    'content': self._extract_content(entry),
                    'url': entry.get('link', ''),
                    'author': entry.get('author', ''),
                    'published_at': self._parse_date(entry.get('published')),
                    'category': feed_config['category'],
                    'reliability_score': feed_config['reliability']
                }
                
                articles.append(article)
            
            print(f"  ✓ {feed_config['name']}: {len(articles)} artículos")
            return articles
            
        except Exception as e:
            print(f"  ✗ Error en {feed_config['name']}: {e}")
            return []
    
    def _extract_content(self, entry):
        """Extraer contenido del artículo"""
        if hasattr(entry, 'content'):
            return entry.content[0].value
        elif hasattr(entry, 'summary'):
            return entry.summary
        elif hasattr(entry, 'description'):
            return entry.description
        return ''
    
    def _parse_date(self, date_str):
        """Parsear fecha del artículo"""
        if not date_str:
            return datetime.now(timezone.utc)
        
        try:
            from dateutil import parser
            return parser.parse(date_str)
        except:
            return datetime.now(timezone.utc)
