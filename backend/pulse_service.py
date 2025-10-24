"""
Servicio principal de Pulse IA
Análisis de sentimiento del mercado crypto
"""
import asyncio
from datetime import datetime, timezone
from typing import Dict, List
import numpy as np
from collections import Counter
import re

from pulse_rss_scraper import PulseRSSScraper
from pulse_twitter_scraper import PulseTwitterScraper
from pulse_reddit_scraper import PulseRedditScraper
from pulse_sentiment_analyzer import PulseSentimentAnalyzer

class PulseIAService:
    def __init__(self):
        """Inicializar todos los componentes"""
        print("🚀 Inicializando Pulse IA Service...")
        self.rss_scraper = PulseRSSScraper()
        self.twitter_scraper = PulseTwitterScraper()
        self.reddit_scraper = PulseRedditScraper()
        self.sentiment_analyzer = PulseSentimentAnalyzer()
        print("✅ Pulse IA Service listo")
    
    async def analyze_crypto_sentiment(self, symbol: str = 'BTC') -> Dict:
        """
        Análisis completo de sentimiento para una crypto
        
        Args:
            symbol: Símbolo de la crypto (BTC, ETH, etc.)
        
        Returns:
            Dict con análisis completo
        """
        print(f"\n📊 Analizando sentimiento de {symbol}...")
        print("=" * 60)
        
        # 1. Obtener datos de todas las fuentes en paralelo
        print("\n🔍 Obteniendo datos de fuentes...")
        
        tasks = [
            self.rss_scraper.fetch_all_feeds(),
            self.twitter_scraper.fetch_crypto_tweets(symbol),
            self.reddit_scraper.fetch_crypto_posts(symbol)
        ]
        
        rss_articles, twitter_posts, reddit_posts = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Manejar excepciones
        if isinstance(rss_articles, Exception):
            print(f"⚠️ RSS Error: {rss_articles}")
            rss_articles = []
        if isinstance(twitter_posts, Exception):
            print(f"⚠️ Twitter Error: {twitter_posts}")
            twitter_posts = []
        if isinstance(reddit_posts, Exception):
            print(f"⚠️ Reddit Error: {reddit_posts}")
            reddit_posts = []
        
        # 2. Filtrar artículos relevantes para el símbolo
        relevant_articles = self._filter_by_symbol(rss_articles, symbol)
        
        print(f"\n📈 Datos obtenidos:")
        print(f"   • Noticias RSS: {len(relevant_articles)}")
        print(f"   • Tweets: {len(twitter_posts)}")
        print(f"   • Reddit posts: {len(reddit_posts)}")
        
        total_sources = len(relevant_articles) + len(twitter_posts) + len(reddit_posts)
        
        if total_sources == 0:
            return self._empty_result(symbol)
        
        # 3. Analizar sentimiento de cada fuente
        print("\n🤖 Analizando sentimiento con IA...")
        
        news_sentiments = await self._analyze_source_batch(relevant_articles, 'news')
        twitter_sentiments = await self._analyze_source_batch(twitter_posts, 'twitter')
        reddit_sentiments = await self._analyze_source_batch(reddit_posts, 'reddit')
        
        # 4. Calcular métricas agregadas
        print("\n📊 Calculando métricas...")
        
        # Sentiment scores ponderados por fuente
        news_score = self._calculate_avg_sentiment(news_sentiments) * 0.5  # 50% peso
        social_score = self._calculate_avg_sentiment(twitter_sentiments) * 0.3  # 30% peso
        reddit_score = self._calculate_avg_sentiment(reddit_sentiments) * 0.2  # 20% peso
        
        overall_sentiment = news_score + social_score + reddit_score
        
        # Convertir a escala -100 a +100
        overall_sentiment_scaled = int(overall_sentiment * 100)
        
        # 5. Detectar FOMO/FUD
        all_texts = [
            item.get('content', item.get('title', ''))
            for item in (relevant_articles + twitter_posts + reddit_posts)
        ]
        
        fomo_fud_scores = [
            self.sentiment_analyzer.detect_fomo_fud(text)
            for text in all_texts[:100]  # Limitar a 100 para velocidad
        ]
        
        avg_fomo = int(np.mean([score['fomo_score'] for score in fomo_fud_scores])) if fomo_fud_scores else 0
        avg_fud = int(np.mean([score['fud_score'] for score in fomo_fud_scores])) if fomo_fud_scores else 0
        
        # 6. Determinar trend
        trend = self._determine_trend(overall_sentiment_scaled, avg_fomo, avg_fud)
        
        # 7. Extraer keywords trending
        trending_keywords = self._extract_trending_keywords(all_texts)
        
        # 8. Generar recomendación
        recommendation = self._generate_recommendation(overall_sentiment_scaled, trend, avg_fomo, avg_fud)
        
        # 9. Construir resultado
        result = {
            'symbol': symbol,
            'overall_sentiment': overall_sentiment_scaled,
            'news_sentiment': int(news_score * 100),
            'social_sentiment': int((social_score + reddit_score) * 100),
            'reddit_sentiment': int(reddit_score * 100),
            'twitter_sentiment': int(social_score * 100),
            
            'trend': trend,
            'momentum': abs(overall_sentiment_scaled) / 100,
            
            'news_volume': len(relevant_articles),
            'social_mentions': len(twitter_posts) + len(reddit_posts),
            'reddit_posts': len(reddit_posts),
            'twitter_tweets': len(twitter_posts),
            
            'trending_keywords': trending_keywords[:10],
            
            'fomo_score': avg_fomo,
            'fud_score': avg_fud,
            
            'recommendation': recommendation,
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'sources_analyzed': total_sources
        }
        
        print(f"\n✅ Análisis completado!")
        print(f"   Overall Sentiment: {overall_sentiment_scaled}/100")
        print(f"   Trend: {trend}")
        print(f"   Recommendation: {recommendation}")
        
        return result
    
    def _filter_by_symbol(self, articles, symbol):
        """Filtrar artículos que mencionan el símbolo"""
        symbol_variations = [symbol, f'${symbol}', f'#{symbol}', symbol.lower()]
        
        filtered = []
        for article in articles:
            text = (article.get('title', '') + ' ' + article.get('content', '')).lower()
            if any(var.lower() in text for var in symbol_variations):
                filtered.append(article)
        
        return filtered
    
    async def _analyze_source_batch(self, items, source_type):
        """Analizar sentimiento de un batch de items"""
        sentiments = []
        
        for item in items:
            text = item.get('content') or item.get('title', '')
            if text:
                sentiment = self.sentiment_analyzer.analyze_text(text[:512])
                sentiments.append(sentiment['sentiment_score'])
        
        return sentiments
    
    def _calculate_avg_sentiment(self, sentiments):
        """Calcular promedio de sentimientos"""
        if not sentiments:
            return 0.0
        return float(np.mean(sentiments))
    
    def _determine_trend(self, sentiment, fomo, fud):
        """Determinar trend del mercado"""
        if sentiment > 50 and fomo > 60:
            return '🔥 Hot'
        elif sentiment > 30:
            return '📈 Rising'
        elif sentiment > -30:
            return '➡️ Stable'
        else:
            return '📉 Declining'
    
    def _extract_trending_keywords(self, texts):
        """Extraer keywords más frecuentes"""
        # Palabras a ignorar
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'to', 'of', 'in', 'for', 'on', 'with'])
        
        all_words = []
        for text in texts:
            words = re.findall(r'\b[a-z]{4,}\b', text.lower())
            all_words.extend([w for w in words if w not in stop_words])
        
        # Contar frecuencias
        counter = Counter(all_words)
        
        return [word for word, count in counter.most_common(20)]
    
    def _generate_recommendation(self, sentiment, trend, fomo, fud):
        """Generar recomendación basada en análisis"""
        if sentiment > 60 and fomo < 40:
            return '🟢 Bullish'
        elif sentiment < -60 and fud > 40:
            return '🔴 Bearish'
        else:
            return '🟡 Neutral'
    
    def _empty_result(self, symbol):
        """Resultado vacío cuando no hay datos"""
        return {
            'symbol': symbol,
            'overall_sentiment': 0,
            'news_sentiment': 0,
            'social_sentiment': 0,
            'reddit_sentiment': 0,
            'twitter_sentiment': 0,
            'trend': '❓ No Data',
            'momentum': 0.0,
            'news_volume': 0,
            'social_mentions': 0,
            'reddit_posts': 0,
            'twitter_tweets': 0,
            'trending_keywords': [],
            'fomo_score': 0,
            'fud_score': 0,
            'recommendation': 'Neutral',
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'sources_analyzed': 0
        }
    
    def format_telegram_message(self, analysis: Dict) -> str:
        """Formatear análisis para Telegram"""
        sentiment_emoji = {
            range(-100, -60): '🔴',
            range(-60, -20): '🟠',
            range(-20, 20): '🟡',
            range(20, 60): '🟢',
            range(60, 101): '🟢🟢'
        }
        
        emoji = '🟡'
        for sent_range, em in sentiment_emoji.items():
            if analysis['overall_sentiment'] in sent_range:
                emoji = em
                break
        
        message = f"""📊 *Pulse IA Analysis*

*Token:* {analysis['symbol']}

{emoji} *Sentiment Score:* {analysis['overall_sentiment']:+d}/100
*Trend:* {analysis['trend']}

*Sources Analyzed:*
• {analysis['news_volume']} news articles
• {analysis['twitter_tweets']} tweets
• {analysis['reddit_posts']} Reddit posts

*Key Insights:*
• News Sentiment: {analysis['news_sentiment']:+d}
• Social Sentiment: {analysis['social_sentiment']:+d}
• FOMO Level: {analysis['fomo_score']}/100 {"🚀" if analysis['fomo_score'] > 60 else ""}
• FUD Level: {analysis['fud_score']}/100 {"⚠️" if analysis['fud_score'] > 60 else ""}

*Recommendation:* {analysis['recommendation']}

*Trending Keywords:*
{', '.join(analysis['trending_keywords'][:5])}

_Pulse IA - Market Sentiment Analysis_
        """.strip()
        
        return message
