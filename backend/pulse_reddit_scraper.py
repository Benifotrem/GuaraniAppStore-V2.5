"""
Scraper de Reddit para análisis de sentimiento en Pulse IA
"""
import praw
import os
from datetime import datetime, timezone
from typing import List, Dict
from pulse_config import REDDIT_SUBREDDITS

class PulseRedditScraper:
    def __init__(self):
        """Inicializar cliente de Reddit API"""
        self.reddit = praw.Reddit(
            client_id=os.environ.get('REDDIT_CLIENT_ID'),
            client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
            user_agent=os.environ.get('REDDIT_USER_AGENT', 'PulseIA/1.0')
        )
    
    async def fetch_crypto_posts(self, symbol: str = 'BTC', limit: int = 50) -> List[Dict]:
        """
        Obtener posts de Reddit sobre una crypto
        
        Args:
            symbol: Símbolo de la crypto
            limit: Número de posts a obtener
        
        Returns:
            List de posts
        """
        posts = []
        
        for subreddit_name in REDDIT_SUBREDDITS:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Buscar posts con el símbolo
                for submission in subreddit.search(symbol, limit=limit, sort='hot'):
                    post = {
                        'source_name': f'Reddit r/{subreddit_name}',
                        'source_type': 'reddit',
                        'title': submission.title,
                        'content': submission.selftext,
                        'url': f"https://reddit.com{submission.permalink}",
                        'author': str(submission.author) if submission.author else '[deleted]',
                        'published_at': datetime.fromtimestamp(submission.created_utc, tz=timezone.utc),
                        'metrics': {
                            'upvotes': submission.score,
                            'comments': submission.num_comments,
                            'upvote_ratio': submission.upvote_ratio
                        }
                    }
                    
                    posts.append(post)
                
                print(f"  ✓ r/{subreddit_name}: {len([p for p in posts if f'r/{subreddit_name}' in p['source_name']])} posts")
                
            except Exception as e:
                print(f"  ✗ Error en r/{subreddit_name}: {e}")
        
        print(f"🔴 Reddit: {len(posts)} posts totales sobre {symbol}")
        return posts
    
    async def fetch_hot_discussions(self, subreddit_name: str = 'cryptocurrency', limit: int = 25) -> List[Dict]:
        """
        Obtener discusiones populares de un subreddit
        
        Args:
            subreddit_name: Nombre del subreddit
            limit: Número de posts
        
        Returns:
            List de posts hot
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            hot_posts = []
            
            for submission in subreddit.hot(limit=limit):
                hot_posts.append({
                    'title': submission.title,
                    'content': submission.selftext,
                    'score': submission.score,
                    'comments': submission.num_comments,
                    'url': f"https://reddit.com{submission.permalink}",
                    'published_at': datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)
                })
            
            return hot_posts
            
        except Exception as e:
            print(f"⚠️ Error en hot discussions: {e}")
            return []
