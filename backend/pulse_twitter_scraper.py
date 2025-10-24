"""
Scraper de tweets para análisis de sentimiento en Pulse IA
"""
import tweepy
import os
from datetime import datetime, timedelta
from typing import List, Dict
from pulse_config import TWITTER_ACCOUNTS

class PulseTwitterScraper:
    def __init__(self):
        """Inicializar cliente de Twitter API v2"""
        self.client = tweepy.Client(
            bearer_token=os.environ.get('TWITTER_BEARER_TOKEN'),
            consumer_key=os.environ.get('TWITTER_API_KEY'),
            consumer_secret=os.environ.get('TWITTER_API_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_ACCESS_SECRET'),
            wait_on_rate_limit=True
        )
    
    async def fetch_crypto_tweets(self, symbol: str = 'BTC', hours: int = 24) -> List[Dict]:
        """
        Obtener tweets sobre una cripto específica
        
        Args:
            symbol: Símbolo de la crypto (BTC, ETH, etc.)
            hours: Horas hacia atrás para buscar
        
        Returns:
            List de tweets
        """
        query = f"(#{symbol} OR ${symbol} OR {symbol}) -is:retweet lang:en"
        
        # Calcular fecha de inicio
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        try:
            tweets = self.client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=100,
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )
            
            tweet_list = []
            
            if tweets.data:
                for tweet in tweets.data:
                    tweet_list.append({
                        'source_name': 'Twitter',
                        'source_type': 'twitter',
                        'content': tweet.text,
                        'author': f"user_{tweet.author_id}",
                        'url': f"https://twitter.com/i/web/status/{tweet.id}",
                        'published_at': tweet.created_at,
                        'metrics': {
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                            'replies': tweet.public_metrics['reply_count']
                        }
                    })
            
            print(f"🐦 Twitter: {len(tweet_list)} tweets sobre {symbol}")
            return tweet_list
            
        except Exception as e:
            print(f"⚠️ Error en Twitter scraping: {e}")
            return []
    
    async def fetch_influencer_tweets(self, username: str, count: int = 10) -> List[Dict]:
        """
        Obtener tweets recientes de un influencer específico
        
        Args:
            username: Username del influencer (sin @)
            count: Número de tweets a obtener
        
        Returns:
            List de tweets
        """
        try:
            user = self.client.get_user(username=username)
            
            if user.data:
                tweets = self.client.get_users_tweets(
                    id=user.data.id,
                    max_results=count,
                    tweet_fields=['created_at', 'public_metrics']
                )
                
                if tweets.data:
                    return [{
                        'content': tweet.text,
                        'author': username,
                        'published_at': tweet.created_at,
                        'metrics': tweet.public_metrics
                    } for tweet in tweets.data]
            
            return []
            
        except Exception as e:
            print(f"⚠️ Error obteniendo tweets de {username}: {e}")
            return []
