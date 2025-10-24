"""
API REST endpoints para Momentum Predictor
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

from momentum_service import MomentumPredictorService

router = APIRouter(prefix="/api/momentum", tags=["momentum"])

# Inicializar servicio
momentum_service = None
db_client = None
db = None

def get_momentum_service():
    global momentum_service
    if momentum_service is None:
        momentum_service = MomentumPredictorService(use_mock=True)
    return momentum_service

def get_db():
    global db_client, db
    if db_client is None:
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')
        db_client = AsyncIOMotorClient(MONGO_URL)
        db = db_client.get_database()
    return db

# Schemas
class SignalResponse(BaseModel):
    symbol: str
    signal: str
    confidence: float
    current_price: float
    entry_price: float
    target_1: float
    target_2: float
    stop_loss: float
    timeframe: str
    risk_level: str
    probabilities: dict
    predicted_at: str
    model_version: str
    is_mock: bool
    indicators: Optional[dict] = None

class SignalHistory(BaseModel):
    symbol: str
    signal: str
    confidence: float
    current_price: float
    predicted_at: datetime

@router.get("/signal/{symbol}", response_model=SignalResponse)
async def get_signal(symbol: str):
    """
    Obtener señal de trading para un símbolo
    
    Args:
        symbol: Símbolo de la crypto (BTC, ETH, etc.)
    
    Returns:
        Señal de trading completa
    """
    try:
        momentum = get_momentum_service()
        prediction = momentum.predict_signal(symbol.upper())
        
        # Guardar en base de datos
        database = get_db()
        await database.momentum_signals.insert_one(prediction)
        
        return prediction
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/signals/history", response_model=List[SignalHistory])
async def get_signals_history(
    symbol: Optional[str] = None,
    limit: int = 50
):
    """
    Obtener historial de señales
    
    Args:
        symbol: Filtrar por símbolo (opcional)
        limit: Número de señales a retornar
    
    Returns:
        Lista de señales históricas
    """
    try:
        database = get_db()
        
        query = {}
        if symbol:
            query['symbol'] = symbol.upper()
        
        cursor = database.momentum_signals.find(query).sort('predicted_at', -1).limit(limit)
        
        results = await cursor.to_list(length=limit)
        
        return [{
            'symbol': r['symbol'],
            'signal': r['signal'],
            'confidence': r['confidence'],
            'current_price': r['current_price'],
            'predicted_at': r['predicted_at']
        } for r in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{symbol}")
async def get_accuracy_stats(symbol: str):
    """
    Obtener estadísticas de accuracy para un símbolo
    
    Args:
        symbol: Símbolo de la crypto
    
    Returns:
        Estadísticas de accuracy
    """
    try:
        database = get_db()
        
        # Contar señales por tipo
        total = await database.momentum_signals.count_documents({'symbol': symbol.upper()})
        
        if total == 0:
            raise HTTPException(status_code=404, detail="No signals found for symbol")
        
        buy_signals = await database.momentum_signals.count_documents({
            'symbol': symbol.upper(),
            'signal': 'BUY'
        })
        
        sell_signals = await database.momentum_signals.count_documents({
            'symbol': symbol.upper(),
            'signal': 'SELL'
        })
        
        hold_signals = await database.momentum_signals.count_documents({
            'symbol': symbol.upper(),
            'signal': 'HOLD'
        })
        
        # Obtener última señal
        last_signal = await database.momentum_signals.find_one(
            {'symbol': symbol.upper()},
            sort=[('predicted_at', -1)]
        )
        
        return {
            'symbol': symbol.upper(),
            'total_predictions': total,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'hold_signals': hold_signals,
            'buy_percentage': round((buy_signals / total) * 100, 2),
            'last_signal': last_signal['signal'] if last_signal else None,
            'last_confidence': last_signal['confidence'] if last_signal else None,
            'last_predicted_at': last_signal['predicted_at'] if last_signal else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    momentum = get_momentum_service()
    
    return {
        "status": "healthy",
        "service": "Momentum Predictor",
        "version": "1.0.0",
        "model_loaded": not momentum.use_mock,
        "mode": "MOCK" if momentum.use_mock else "TRAINED"
    }
