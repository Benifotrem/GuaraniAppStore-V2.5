"""
API REST endpoints para CryptoShield
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

from cryptoshield_service import CryptoShieldService

router = APIRouter(prefix="/api/cryptoshield", tags=["cryptoshield"])

# Inicializar servicio
cryptoshield_service = None
db_client = None
db = None

def get_cryptoshield_service():
    global cryptoshield_service
    if cryptoshield_service is None:
        cryptoshield_service = CryptoShieldService(use_mock=True)
    return cryptoshield_service

def get_db():
    global db_client, db
    if db_client is None:
        MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/guarani_appstore')
        db_client = AsyncIOMotorClient(MONGO_URL)
        db = db_client.get_database()
    return db

# Schemas
class WalletScanResponse(BaseModel):
    address: str
    balance_eth: float
    transaction_count: int
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    recommendations: List[str]
    scan_type: str
    model_version: str
    is_mock: bool
    analyzed_at: str

class TransactionVerifyResponse(BaseModel):
    tx_hash: str
    status: str
    is_success: bool
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    recommendations: List[str]
    scan_type: str
    model_version: str
    is_mock: bool
    verified_at: str

class ContractScanResponse(BaseModel):
    contract_address: str
    is_contract: bool
    is_verified: bool
    risk_score: int
    risk_level: str
    risk_factors: List[str]
    recommendations: List[str]
    scan_type: str
    model_version: str
    is_mock: bool
    analyzed_at: str

class ScanHistoryItem(BaseModel):
    scan_type: str
    address_or_hash: str
    risk_level: str
    risk_score: int
    scanned_at: datetime

@router.get("/scan/wallet/{address}", response_model=WalletScanResponse)
async def scan_wallet(address: str):
    """
    Escanear una wallet de Ethereum para detectar fraude
    
    Args:
        address: Dirección de la wallet (formato 0x...)
    
    Returns:
        Análisis completo de riesgo de la wallet
    """
    try:
        # Validar formato de address
        if not address.startswith('0x') or len(address) != 42:
            raise HTTPException(status_code=400, detail="Invalid Ethereum address format")
        
        cryptoshield = get_cryptoshield_service()
        result = cryptoshield.scan_wallet(address)
        
        # Guardar en base de datos
        database = get_db()
        await database.cryptoshield_scans.insert_one({
            **result,
            'scan_type': 'wallet',
            'address_or_hash': address
        })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify/transaction/{tx_hash}", response_model=TransactionVerifyResponse)
async def verify_transaction(tx_hash: str):
    """
    Verificar una transacción específica
    
    Args:
        tx_hash: Hash de la transacción (formato 0x...)
    
    Returns:
        Verificación de la transacción
    """
    try:
        # Validar formato de tx_hash
        if not tx_hash.startswith('0x') or len(tx_hash) != 66:
            raise HTTPException(status_code=400, detail="Invalid transaction hash format")
        
        cryptoshield = get_cryptoshield_service()
        result = cryptoshield.verify_transaction(tx_hash)
        
        # Guardar en base de datos
        database = get_db()
        await database.cryptoshield_scans.insert_one({
            **result,
            'scan_type': 'transaction',
            'address_or_hash': tx_hash
        })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan/contract/{contract_address}", response_model=ContractScanResponse)
async def scan_contract(contract_address: str):
    """
    Escanear un contrato inteligente
    
    Args:
        contract_address: Dirección del contrato (formato 0x...)
    
    Returns:
        Análisis del contrato
    """
    try:
        # Validar formato de address
        if not contract_address.startswith('0x') or len(contract_address) != 42:
            raise HTTPException(status_code=400, detail="Invalid contract address format")
        
        cryptoshield = get_cryptoshield_service()
        result = cryptoshield.scan_contract(contract_address)
        
        # Guardar en base de datos
        database = get_db()
        await database.cryptoshield_scans.insert_one({
            **result,
            'scan_type': 'contract',
            'address_or_hash': contract_address
        })
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scans/history", response_model=List[ScanHistoryItem])
async def get_scan_history(
    scan_type: Optional[str] = None,
    limit: int = 50
):
    """
    Obtener historial de escaneos
    
    Args:
        scan_type: Filtrar por tipo (wallet/transaction/contract)
        limit: Número de resultados
    
    Returns:
        Lista de escaneos históricos
    """
    try:
        database = get_db()
        
        query = {}
        if scan_type and scan_type in ['wallet', 'transaction', 'contract']:
            query['scan_type'] = scan_type
        
        # Determinar campo de fecha según scan_type
        cursor = database.cryptoshield_scans.find(query).sort('analyzed_at', -1).limit(limit)
        
        results = await cursor.to_list(length=limit)
        
        history = []
        for r in results:
            # Manejar diferentes campos de fecha
            scanned_at = r.get('analyzed_at') or r.get('verified_at') or datetime.now().isoformat()
            
            history.append({
                'scan_type': r['scan_type'],
                'address_or_hash': r.get('address_or_hash', 'N/A'),
                'risk_level': r.get('risk_level', 'unknown'),
                'risk_score': r.get('risk_score', 0),
                'scanned_at': scanned_at
            })
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """
    Obtener estadísticas de escaneos
    
    Returns:
        Estadísticas generales
    """
    try:
        database = get_db()
        
        total_scans = await database.cryptoshield_scans.count_documents({})
        
        if total_scans == 0:
            return {
                'total_scans': 0,
                'wallet_scans': 0,
                'transaction_verifications': 0,
                'contract_scans': 0,
                'high_risk_found': 0,
                'medium_risk_found': 0,
                'low_risk_found': 0
            }
        
        # Contar por tipo
        wallet_scans = await database.cryptoshield_scans.count_documents({'scan_type': 'wallet'})
        tx_scans = await database.cryptoshield_scans.count_documents({'scan_type': 'transaction'})
        contract_scans = await database.cryptoshield_scans.count_documents({'scan_type': 'contract'})
        
        # Contar por nivel de riesgo
        high_risk = await database.cryptoshield_scans.count_documents({'risk_level': 'high'})
        medium_risk = await database.cryptoshield_scans.count_documents({'risk_level': 'medium'})
        low_risk = await database.cryptoshield_scans.count_documents({'risk_level': 'low'})
        
        return {
            'total_scans': total_scans,
            'wallet_scans': wallet_scans,
            'transaction_verifications': tx_scans,
            'contract_scans': contract_scans,
            'high_risk_found': high_risk,
            'medium_risk_found': medium_risk,
            'low_risk_found': low_risk,
            'high_risk_percentage': round((high_risk / total_scans) * 100, 2) if total_scans > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    cryptoshield = get_cryptoshield_service()
    
    return {
        "status": "healthy",
        "service": "CryptoShield IA",
        "version": "1.0.0",
        "model_loaded": not cryptoshield.use_mock,
        "mode": "MOCK" if cryptoshield.use_mock else "TRAINED",
        "etherscan_api": "configured" if cryptoshield.analyzer.etherscan else "not_configured"
    }
