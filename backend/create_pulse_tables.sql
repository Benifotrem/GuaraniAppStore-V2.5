-- ============================================
-- PULSE IA DATABASE SCHEMA
-- ============================================

-- Tabla de análisis de sentimiento
CREATE TABLE IF NOT EXISTS pulse_sentiment_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Crypto symbol
    symbol VARCHAR(20) NOT NULL,
    
    -- Sentiment scores (-100 to +100)
    overall_sentiment INTEGER,
    news_sentiment INTEGER,
    social_sentiment INTEGER,
    reddit_sentiment INTEGER,
    twitter_sentiment INTEGER,
    
    -- Trends
    trend VARCHAR(20),
    momentum DECIMAL(5, 2),
    
    -- Volume metrics
    news_volume INTEGER DEFAULT 0,
    social_mentions INTEGER DEFAULT 0,
    reddit_posts INTEGER DEFAULT 0,
    twitter_tweets INTEGER DEFAULT 0,
    
    -- Keywords trending
    trending_keywords TEXT[],
    
    -- FOMO/FUD detection
    fomo_score INTEGER DEFAULT 0,
    fud_score INTEGER DEFAULT 0,
    
    -- Recommendation
    recommendation VARCHAR(20),
    
    -- Metadata
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sources_analyzed INTEGER DEFAULT 0,
    
    -- Full data snapshot
    raw_data JSONB
);

CREATE INDEX IF NOT EXISTS idx_pulse_symbol ON pulse_sentiment_analysis(symbol);
CREATE INDEX IF NOT EXISTS idx_pulse_analyzed ON pulse_sentiment_analysis(analyzed_at DESC);
CREATE INDEX IF NOT EXISTS idx_pulse_sentiment ON pulse_sentiment_analysis(overall_sentiment DESC);

-- Tabla de fuentes de noticias (RSS feeds)
CREATE TABLE IF NOT EXISTS pulse_news_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50),
    
    url TEXT NOT NULL,
    rss_feed_url TEXT,
    
    is_active BOOLEAN DEFAULT TRUE,
    reliability_score INTEGER DEFAULT 70,
    
    last_fetched_at TIMESTAMP WITH TIME ZONE,
    fetch_frequency_minutes INTEGER DEFAULT 30,
    
    total_articles_fetched INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de artículos/posts analizados
CREATE TABLE IF NOT EXISTS pulse_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    source_id UUID REFERENCES pulse_news_sources(id),
    
    title TEXT NOT NULL,
    content TEXT,
    url TEXT,
    author VARCHAR(200),
    
    -- Sentiment del artículo individual
    sentiment_score DECIMAL(5, 2),
    sentiment_label VARCHAR(20),
    
    -- Crypto mencionadas
    mentioned_cryptos TEXT[],
    
    -- Metadata
    published_at TIMESTAMP WITH TIME ZONE,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Categoría
    category VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_pulse_articles_source ON pulse_articles(source_id);
CREATE INDEX IF NOT EXISTS idx_pulse_articles_published ON pulse_articles(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_pulse_articles_sentiment ON pulse_articles(sentiment_score);

-- Tabla de suscripciones al bot
CREATE TABLE IF NOT EXISTS pulse_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    telegram_chat_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(100),
    
    -- Símbolos trackeados
    tracked_symbols TEXT[] DEFAULT '{"BTC", "ETH"}',
    
    -- Notificaciones
    notifications_enabled BOOLEAN DEFAULT TRUE,
    min_sentiment_change INTEGER DEFAULT 20,
    
    -- Metadata
    status VARCHAR(20) DEFAULT 'active',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pulse_subs_telegram ON pulse_subscriptions(telegram_chat_id);

-- Insertar fuentes RSS predeterminadas
INSERT INTO pulse_news_sources (source_name, source_type, url, rss_feed_url, reliability_score) VALUES
('CoinDesk', 'rss', 'https://www.coindesk.com', 'https://www.coindesk.com/arc/outboundfeeds/rss/', 95),
('CoinTelegraph', 'rss', 'https://cointelegraph.com', 'https://cointelegraph.com/rss', 90),
('Decrypt', 'rss', 'https://decrypt.co', 'https://decrypt.co/feed', 90),
('The Block', 'rss', 'https://www.theblockcrypto.com', 'https://www.theblockcrypto.com/rss.xml', 95),
('Bitcoin Magazine', 'rss', 'https://bitcoinmagazine.com', 'https://bitcoinmagazine.com/.rss/full/', 85),
('CryptoSlate', 'rss', 'https://cryptoslate.com', 'https://cryptoslate.com/feed/', 85),
('BeInCrypto', 'rss', 'https://beincrypto.com', 'https://beincrypto.com/feed/', 80),
('NewsBTC', 'rss', 'https://www.newsbtc.com', 'https://www.newsbtc.com/feed/', 75),
('U.Today', 'rss', 'https://u.today', 'https://u.today/rss', 75),
('Bitcoinist', 'rss', 'https://bitcoinist.com', 'https://bitcoinist.com/feed/', 75),
('CoinMarketCap News', 'rss', 'https://coinmarketcap.com', 'https://coinmarketcap.com/headlines/rss/', 90),
('Crypto Briefing', 'rss', 'https://cryptobriefing.com', 'https://cryptobriefing.com/feed/', 85),
('AMBCrypto', 'rss', 'https://ambcrypto.com', 'https://ambcrypto.com/feed/', 80),
('Crypto News', 'rss', 'https://cryptonews.com', 'https://cryptonews.com/news/feed/', 75),
('Bitcoin.com News', 'rss', 'https://news.bitcoin.com', 'https://news.bitcoin.com/feed/', 80)
ON CONFLICT DO NOTHING;
