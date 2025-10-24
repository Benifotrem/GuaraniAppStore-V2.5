"""
API REST endpoints para Pulse IA
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

from pulse_service import PulseIAService

router = APIRouter(prefix="/api/pulse", tags=["pulse"])

# Inicializar servicio
pulse_service = None
db_client = None
db = None

def get_pulse_service():
    global pulse_service
    if pulse_service is None:
        pulse_service = PulseIAService()
    return pulse_service

def get_db():
    global db_client, db
    if db_client is None:
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')
        db_client = AsyncIOMotorClient(MONGO_URL)
        db = db_client.get_database()
    return db

# Schemas
class SentimentAnalysisResponse(BaseModel):
    symbol: str
    overall_sentiment: int
    news_sentiment: int
    social_sentiment: int
    reddit_sentiment: int
    twitter_sentiment: int
    trend: str
    momentum: float
    news_volume: int
    social_mentions: int
    reddit_posts: int
    twitter_tweets: int
    trending_keywords: List[str]
    fomo_score: int
    fud_score: int
    recommendation: str
    analyzed_at: str
    sources_analyzed: int

class HistoricalAnalysis(BaseModel):
    symbol: str
    overall_sentiment: int
    recommendation: str
    analyzed_at: datetime
    sources_analyzed: int

@router.get("/analyze/{symbol}", response_model=SentimentAnalysisResponse)
async def analyze_sentiment(symbol: str):
    """
    Analizar sentimiento de una crypto
    
    Args:
        symbol: Símbolo de la crypto (BTC, ETH, etc.)
    
    Returns:
        Análisis completo de sentimiento
    """
    try:
        pulse = get_pulse_service()
        analysis = await pulse.analyze_crypto_sentiment(symbol.upper())
        
        # Guardar en base de datos
        database = get_db()
        await database.pulse_sentiment_analysis.insert_one(analysis)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{symbol}", response_model=List[HistoricalAnalysis])
async def get_history(symbol: str, limit: int = 20):
    """
    Obtener historial de análisis de una crypto
    
    Args:
        symbol: Símbolo de la crypto
        limit: Número de análisis a retornar
    
    Returns:
        Lista de análisis históricos
    """
    try:
        database = get_db()
        
        cursor = database.pulse_sentiment_analysis.find(
            {'symbol': symbol.upper()}
        ).sort('analyzed_at', -1).limit(limit)
        
        results = await cursor.to_list(length=limit)
        
        return [{
            'symbol': r['symbol'],
            'overall_sentiment': r['overall_sentiment'],
            'recommendation': r['recommendation'],
            'analyzed_at': r['analyzed_at'],
            'sources_analyzed': r['sources_analyzed']
        } for r in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending")
async def get_trending():
    """
    Obtener análisis de las cryptos más populares
    
    Returns:
        Análisis de BTC, ETH, BNB, SOL, ADA
    """
    try:
        pulse = get_pulse_service()
        
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA']
        results = []
        
        for symbol in symbols:
            try:
                analysis = await pulse.analyze_crypto_sentiment(symbol)
                results.append({
                    'symbol': analysis['symbol'],
                    'overall_sentiment': analysis['overall_sentiment'],
                    'trend': analysis['trend'],
                    'recommendation': analysis['recommendation']
                })
            except:
                pass
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{symbol}")
async def get_stats(symbol: str):
    """
    Obtener estadísticas agregadas de un símbolo
    
    Args:
        symbol: Símbolo de la crypto
    
    Returns:
        Estadísticas de sentimiento
    """
    try:
        database = get_db()
        
        # Obtener últimos 30 análisis
        cursor = database.pulse_sentiment_analysis.find(
            {'symbol': symbol.upper()}
        ).sort('analyzed_at', -1).limit(30)
        
        analyses = await cursor.to_list(length=30)
        
        if not analyses:
            raise HTTPException(status_code=404, detail="No data found for symbol")
        
        # Calcular estadísticas
        sentiments = [a['overall_sentiment'] for a in analyses]
        
        stats = {
            'symbol': symbol.upper(),
            'total_analyses': len(analyses),
            'avg_sentiment': sum(sentiments) / len(sentiments),
            'max_sentiment': max(sentiments),
            'min_sentiment': min(sentiments),
            'current_sentiment': sentiments[0],
            'sentiment_change_7d': sentiments[0] - sentiments[-1] if len(sentiments) > 7 else 0,
            'last_updated': analyses[0]['analyzed_at']
        }
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Pulse IA",
        "version": "1.0.0"
    }
