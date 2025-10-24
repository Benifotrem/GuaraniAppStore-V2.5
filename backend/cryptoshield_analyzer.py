"""
Analizador de transacciones blockchain para CryptoShield
Análisis de wallets, contratos y transacciones usando Etherscan
"""
import os
from web3 import Web3
from etherscan import Etherscan
from datetime import datetime, timezone
from typing import Dict, List, Optional
import numpy as np

class CryptoShieldAnalyzer:
    def __init__(self, etherscan_api_key=None):
        """
        Inicializar analizador
        
        Args:
            etherscan_api_key: API key de Etherscan
        """
        self.etherscan_api_key = etherscan_api_key or os.environ.get('ETHERSCAN_API_KEY')
        
        if self.etherscan_api_key:
            self.etherscan = Etherscan(self.etherscan_api_key)
            print("✅ Etherscan API inicializada")
        else:
            self.etherscan = None
            print("⚠️ Etherscan API key no configurada - Modo MOCK")
        
        # Web3 para conversiones
        self.w3 = Web3()
    
    def analyze_wallet(self, address: str) -> Dict:
        """
        Analizar una wallet de Ethereum
        
        Args:
            address: Dirección de wallet
        
        Returns:
            Dict con análisis completo
        """
        if not self.etherscan:
            return self._mock_wallet_analysis(address)
        
        try:
            # Obtener balance
            balance_wei = int(self.etherscan.get_eth_balance(address))
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            
            # Obtener transacciones
            txs = self.etherscan.get_normal_txs_by_address(
                address, 
                startblock=0, 
                endblock=99999999, 
                sort='desc'
            )
            
            tx_count = len(txs) if isinstance(txs, list) else 0
            
            # Análisis de riesgo básico
            risk_factors = []
            risk_score = 0
            
            # Factor 1: Balance muy bajo con muchas transacciones (posible mixer)
            if balance_eth < 0.01 and tx_count > 100:
                risk_factors.append("High activity with low balance")
                risk_score += 20
            
            # Factor 2: Wallet muy nueva con alto volumen
            if tx_count > 0:
                first_tx = txs[-1] if isinstance(txs, list) else None
                if first_tx:
                    timestamp = int(first_tx.get('timeStamp', 0))
                    wallet_age_days = (datetime.now(timezone.utc).timestamp() - timestamp) / 86400
                    
                    if wallet_age_days < 7 and tx_count > 50:
                        risk_factors.append("New wallet with high activity")
                        risk_score += 25
            
            # Factor 3: Muchas transacciones fallidas
            if isinstance(txs, list):
                failed_txs = sum(1 for tx in txs if tx.get('isError') == '1')
                fail_rate = failed_txs / tx_count if tx_count > 0 else 0
                
                if fail_rate > 0.3:
                    risk_factors.append(f"High failure rate: {fail_rate:.1%}")
                    risk_score += 15
            
            # Determinar nivel de riesgo
            if risk_score >= 50:
                risk_level = 'high'
            elif risk_score >= 25:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'address': address,
                'balance_eth': float(balance_eth),
                'balance_wei': balance_wei,
                'transaction_count': tx_count,
                'risk_score': min(risk_score, 100),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'is_contract': False,  # Requiere otro endpoint
                'analyzed_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error analizando wallet {address}: {e}")
            return self._mock_wallet_analysis(address)
    
    def verify_transaction(self, tx_hash: str) -> Dict:
        """
        Verificar una transacción específica
        
        Args:
            tx_hash: Hash de la transacción
        
        Returns:
            Dict con análisis de la transacción
        """
        if not self.etherscan:
            return self._mock_transaction_analysis(tx_hash)
        
        try:
            # Obtener status de transacción
            status = self.etherscan.get_tx_receipt_status(tx_hash)
            
            is_success = status == '1'
            
            # Análisis simple
            risk_score = 0 if is_success else 50
            risk_level = 'low' if is_success else 'high'
            risk_factors = [] if is_success else ['Transaction failed']
            
            return {
                'tx_hash': tx_hash,
                'status': 'success' if is_success else 'failed',
                'is_success': is_success,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'verified_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error verificando transacción {tx_hash}: {e}")
            return self._mock_transaction_analysis(tx_hash)
    
    def analyze_contract(self, contract_address: str) -> Dict:
        """
        Analizar un contrato inteligente
        
        Args:
            contract_address: Dirección del contrato
        
        Returns:
            Dict con análisis del contrato
        """
        if not self.etherscan:
            return self._mock_contract_analysis(contract_address)
        
        try:
            # Verificar si es contrato
            # Nota: Etherscan no tiene método directo, usamos balance como proxy
            balance = self.etherscan.get_eth_balance(contract_address)
            
            # Análisis básico
            risk_factors = []
            risk_score = 30  # Base para contratos no verificados
            
            # TODO: Agregar análisis de código fuente si está verificado
            # contract_source = self.etherscan.get_contract_source_code(contract_address)
            
            risk_factors.append("Contract not verified or analysis limited")
            
            return {
                'contract_address': contract_address,
                'is_contract': True,
                'balance': balance,
                'risk_score': risk_score,
                'risk_level': 'medium',
                'risk_factors': risk_factors,
                'is_verified': False,
                'analyzed_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error analizando contrato {contract_address}: {e}")
            return self._mock_contract_analysis(contract_address)
    
    def _mock_wallet_analysis(self, address: str) -> Dict:
        """Análisis MOCK de wallet (sin API)"""
        # Generar valores aleatorios basados en address hash
        address_hash = sum(ord(c) for c in address)
        np.random.seed(address_hash % 10000)
        
        balance = np.random.uniform(0.01, 10.0)
        tx_count = np.random.randint(10, 500)
        risk_score = np.random.randint(0, 70)
        
        risk_factors = []
        if risk_score > 50:
            risk_factors.append("MOCK: Simulated high risk pattern")
        
        risk_level = 'high' if risk_score >= 50 else 'medium' if risk_score >= 25 else 'low'
        
        return {
            'address': address,
            'balance_eth': round(balance, 4),
            'balance_wei': int(balance * 1e18),
            'transaction_count': tx_count,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'is_contract': False,
            'is_mock': True,
            'analyzed_at': datetime.now(timezone.utc).isoformat()
        }
    
    def _mock_transaction_analysis(self, tx_hash: str) -> Dict:
        """Análisis MOCK de transacción"""
        tx_hash_val = sum(ord(c) for c in tx_hash)
        np.random.seed(tx_hash_val % 10000)
        
        is_success = np.random.random() > 0.1
        risk_score = 10 if is_success else 60
        
        return {
            'tx_hash': tx_hash,
            'status': 'success' if is_success else 'failed',
            'is_success': is_success,
            'risk_score': risk_score,
            'risk_level': 'low' if is_success else 'high',
            'risk_factors': [] if is_success else ['MOCK: Transaction failed'],
            'is_mock': True,
            'verified_at': datetime.now(timezone.utc).isoformat()
        }
    
    def _mock_contract_analysis(self, contract_address: str) -> Dict:
        """Análisis MOCK de contrato"""
        return {
            'contract_address': contract_address,
            'is_contract': True,
            'balance': '1000000000000000000',
            'risk_score': 35,
            'risk_level': 'medium',
            'risk_factors': ['MOCK: Contract analysis limited without API'],
            'is_verified': False,
            'is_mock': True,
            'analyzed_at': datetime.now(timezone.utc).isoformat()
        }
