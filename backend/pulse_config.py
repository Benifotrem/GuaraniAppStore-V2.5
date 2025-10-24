"""
Configuración de fuentes RSS para Pulse IA
15 feeds principales de noticias crypto
"""

RSS_FEEDS = [
    {
        'name': 'CoinDesk',
        'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'category': 'news',
        'reliability': 95
    },
    {
        'name': 'CoinTelegraph',
        'url': 'https://cointelegraph.com/rss',
        'category': 'news',
        'reliability': 90
    },
    {
        'name': 'Decrypt',
        'url': 'https://decrypt.co/feed',
        'category': 'news',
        'reliability': 90
    },
    {
        'name': 'The Block',
        'url': 'https://www.theblockcrypto.com/rss.xml',
        'category': 'news',
        'reliability': 95
    },
    {
        'name': 'Bitcoin Magazine',
        'url': 'https://bitcoinmagazine.com/.rss/full/',
        'category': 'news',
        'reliability': 85
    },
    {
        'name': 'CryptoSlate',
        'url': 'https://cryptoslate.com/feed/',
        'category': 'news',
        'reliability': 85
    },
    {
        'name': 'BeInCrypto',
        'url': 'https://beincrypto.com/feed/',
        'category': 'news',
        'reliability': 80
    },
    {
        'name': 'NewsBTC',
        'url': 'https://www.newsbtc.com/feed/',
        'category': 'news',
        'reliability': 75
    },
    {
        'name': 'U.Today',
        'url': 'https://u.today/rss',
        'category': 'news',
        'reliability': 75
    },
    {
        'name': 'Bitcoinist',
        'url': 'https://bitcoinist.com/feed/',
        'category': 'news',
        'reliability': 75
    },
    {
        'name': 'CoinMarketCap News',
        'url': 'https://coinmarketcap.com/headlines/rss/',
        'category': 'news',
        'reliability': 90
    },
    {
        'name': 'Crypto Briefing',
        'url': 'https://cryptobriefing.com/feed/',
        'category': 'analysis',
        'reliability': 85
    },
    {
        'name': 'AMBCrypto',
        'url': 'https://ambcrypto.com/feed/',
        'category': 'analysis',
        'reliability': 80
    },
    {
        'name': 'Crypto News',
        'url': 'https://cryptonews.com/news/feed/',
        'category': 'news',
        'reliability': 75
    },
    {
        'name': 'Bitcoin.com News',
        'url': 'https://news.bitcoin.com/feed/',
        'category': 'news',
        'reliability': 80
    }
]

# Subreddits para análisis
REDDIT_SUBREDDITS = [
    'cryptocurrency',
    'bitcoin',
    'ethereum',
    'CryptoMarkets',
    'altcoin'
]

# Top crypto influencers en Twitter (sample - expandir a 300+)
TWITTER_ACCOUNTS = [
    'VitalikButerin',
    'APompliano',
    'DocumentingBTC',
    'woonomic',
    'santimentfeed',
    'CryptoWhale',
    'PeterLBrandt',
    'ToneVays',
    'CarpeNoctom',
    'CryptoCred'
]
