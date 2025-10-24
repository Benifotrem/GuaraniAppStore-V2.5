"""
Servicio principal de CryptoShield
Detección de fraude en blockchain con Autoencoder
"""
import os
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Optional
import joblib

from cryptoshield_analyzer import CryptoShieldAnalyzer

class CryptoShieldService:
    def __init__(self, model_path=None, use_mock=True):
        """
        Inicializar servicio de detección de fraude
        
        Args:
            model_path: Ruta al modelo .h5 (opcional)
            use_mock: Si True, usa análisis MOCK (sin modelo entrenado)
        """
        self.use_mock = use_mock
        self.model = None
        
        # Cargar modelo si existe
        if model_path and os.path.exists(model_path) and not use_mock:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Modelo Autoencoder cargado: {model_path}")
            self.use_mock = False
        else:
            print("⚠️ Modelo no encontrado - Usando análisis MOCK")
            print("   Para entrenar el modelo, ejecuta: python train_cryptoshield_model.py")
            self.use_mock = True
        
        # Inicializar analizador de blockchain
        etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')
        self.analyzer = CryptoShieldAnalyzer(etherscan_api_key)
    
    def scan_wallet(self, address: str) -> Dict:
        """
        Escanear una wallet para detectar fraude
        
        Args:
            address: Dirección de la wallet
        
        Returns:
            Dict con análisis completo de riesgo
        """
        print(f"\n🔍 Escaneando wallet: {address}")
        
        # Análisis básico de la wallet
        wallet_analysis = self.analyzer.analyze_wallet(address)
        
        # Si tenemos modelo entrenado, usar predicción de autoencoder
        if not self.use_mock and self.model:
            # Extraer features y predecir
            features = self._extract_features_from_wallet(wallet_analysis)
            reconstruction_error = self._calculate_reconstruction_error(features)
            
            # Determinar si es fraudulento
            is_fraud, fraud_score = self._evaluate_fraud_risk(reconstruction_error)
            
            wallet_analysis['is_fraudulent'] = is_fraud
            wallet_analysis['fraud_score'] = fraud_score
            wallet_analysis['reconstruction_error'] = reconstruction_error
        
        # Agregar recomendaciones
        wallet_analysis['recommendations'] = self._generate_recommendations(wallet_analysis)
        wallet_analysis['scan_type'] = 'wallet'
        wallet_analysis['model_version'] = 'MOCK' if self.use_mock else 'Autoencoder_v1'
        wallet_analysis['is_mock'] = self.use_mock
        
        print(f"✅ Análisis completado - Risk Level: {wallet_analysis.get('risk_level', 'unknown').upper()}")
        
        return wallet_analysis
    
    def verify_transaction(self, tx_hash: str) -> Dict:
        """
        Verificar una transacción específica
        
        Args:
            tx_hash: Hash de la transacción
        
        Returns:
            Dict con verificación de la transacción
        """
        print(f"\n🔍 Verificando transacción: {tx_hash}")
        
        tx_analysis = self.analyzer.verify_transaction(tx_hash)
        
        # Agregar recomendaciones
        tx_analysis['recommendations'] = self._generate_recommendations(tx_analysis)
        tx_analysis['scan_type'] = 'transaction'
        tx_analysis['model_version'] = 'MOCK' if self.use_mock else 'Autoencoder_v1'
        tx_analysis['is_mock'] = self.use_mock
        
        print(f"✅ Verificación completada - Status: {tx_analysis.get('status', 'unknown').upper()}")
        
        return tx_analysis
    
    def scan_contract(self, contract_address: str) -> Dict:
        """
        Escanear un contrato inteligente
        
        Args:
            contract_address: Dirección del contrato
        
        Returns:
            Dict con análisis del contrato
        """
        print(f"\n🔍 Escaneando contrato: {contract_address}")
        
        contract_analysis = self.analyzer.analyze_contract(contract_address)
        
        # Agregar recomendaciones
        contract_analysis['recommendations'] = self._generate_recommendations(contract_analysis)
        contract_analysis['scan_type'] = 'contract'
        contract_analysis['model_version'] = 'MOCK' if self.use_mock else 'Autoencoder_v1'
        contract_analysis['is_mock'] = self.use_mock
        
        print(f"✅ Análisis completado - Risk Level: {contract_analysis.get('risk_level', 'unknown').upper()}")
        
        return contract_analysis
    
    def _extract_features_from_wallet(self, wallet_data: Dict) -> np.ndarray:
        """
        Extraer features para el modelo Autoencoder
        
        Args:
            wallet_data: Datos de la wallet
        
        Returns:
            Array de features normalizadas (15 features)
        """
        # Placeholder - En producción extraería features reales
        # Features: balance, tx_count, age, etc.
        features = np.random.rand(1, 15)
        return features
    
    def _calculate_reconstruction_error(self, features: np.ndarray) -> float:
        """
        Calcular error de reconstrucción del autoencoder
        
        Args:
            features: Features de entrada
        
        Returns:
            Error de reconstrucción
        """
        reconstruction = self.model.predict(features, verbose=0)
        error = np.mean(np.square(features - reconstruction))
        return float(error)
    
    def _evaluate_fraud_risk(self, reconstruction_error: float, threshold=0.5) -> tuple:
        """
        Evaluar riesgo de fraude basado en error de reconstrucción
        
        Args:
            reconstruction_error: Error del autoencoder
            threshold: Umbral de detección
        
        Returns:
            (is_fraud, fraud_score)
        """
        is_fraud = reconstruction_error > threshold
        fraud_score = min(reconstruction_error * 200, 100)
        
        return is_fraud, round(fraud_score, 2)
    
    def _generate_recommendations(self, analysis: Dict) -> list:
        """
        Generar recomendaciones basadas en análisis
        
        Args:
            analysis: Resultado del análisis
        
        Returns:
            Lista de recomendaciones
        """
        recommendations = []
        risk_level = analysis.get('risk_level', 'low')
        risk_score = analysis.get('risk_score', 0)
        
        if risk_level == 'high' or risk_score >= 70:
            recommendations.append("⚠️ HIGH RISK: Avoid interacting with this address")
            recommendations.append("🔍 Conduct further manual investigation")
            recommendations.append("📊 Check recent transaction history")
        elif risk_level == 'medium' or risk_score >= 40:
            recommendations.append("⚡ MEDIUM RISK: Proceed with caution")
            recommendations.append("🔎 Verify legitimacy before large transactions")
            recommendations.append("📈 Monitor for suspicious activity")
        else:
            recommendations.append("✅ LOW RISK: Address appears safe")
            recommendations.append("🛡️ Continue normal operations")
        
        # Recomendaciones específicas por risk factors
        risk_factors = analysis.get('risk_factors', [])
        if risk_factors:
            recommendations.append(f"⚠️ Detected issues: {', '.join(risk_factors)}")
        
        return recommendations
    
    def format_telegram_message(self, scan_result: Dict) -> str:
        """
        Formatear resultado para Telegram
        
        Args:
            scan_result: Resultado del escaneo
        
        Returns:
            Mensaje formateado en Markdown
        """
        scan_type = scan_result.get('scan_type', 'unknown')
        risk_level = scan_result.get('risk_level', 'unknown')
        risk_score = scan_result.get('risk_score', 0)
        
        # Emojis según nivel de riesgo
        risk_emoji = {
            'low': '🟢',
            'medium': '🟠',
            'high': '🔴'
        }
        
        emoji = risk_emoji.get(risk_level, '⚪')
        
        mock_warning = "\n⚠️ *MOCK Analysis* (Modelo no entrenado)\n" if scan_result.get('is_mock') else ""
        
        if scan_type == 'wallet':
            address = scan_result.get('address', 'N/A')
            balance = scan_result.get('balance_eth', 0)
            tx_count = scan_result.get('transaction_count', 0)
            
            message = f"""🛡️ *CryptoShield Wallet Scan*
{mock_warning}
*Address:* `{address[:10]}...{address[-8:]}`
*Balance:* {balance:.4f} ETH
*Transactions:* {tx_count:,}

{emoji} *Risk Level:* *{risk_level.upper()}*
*Risk Score:* {risk_score}/100

*Recommendations:*
"""
            for rec in scan_result.get('recommendations', []):
                message += f"• {rec}\n"
            
        elif scan_type == 'transaction':
            tx_hash = scan_result.get('tx_hash', 'N/A')
            status = scan_result.get('status', 'unknown')
            
            message = f"""🛡️ *CryptoShield Transaction Scan*
{mock_warning}
*TX Hash:* `{tx_hash[:10]}...{tx_hash[-8:]}`
*Status:* {status.upper()}

{emoji} *Risk Level:* *{risk_level.upper()}*
*Risk Score:* {risk_score}/100

*Recommendations:*
"""
            for rec in scan_result.get('recommendations', []):
                message += f"• {rec}\n"
        
        elif scan_type == 'contract':
            contract_addr = scan_result.get('contract_address', 'N/A')
            is_verified = scan_result.get('is_verified', False)
            
            message = f"""🛡️ *CryptoShield Contract Scan*
{mock_warning}
*Contract:* `{contract_addr[:10]}...{contract_addr[-8:]}`
*Verified:* {'✅ Yes' if is_verified else '❌ No'}

{emoji} *Risk Level:* *{risk_level.upper()}*
*Risk Score:* {risk_score}/100

*Recommendations:*
"""
            for rec in scan_result.get('recommendations', []):
                message += f"• {rec}\n"
        
        else:
            message = "Unknown scan type"
        
        message += f"\n_CryptoShield IA {scan_result.get('model_version', 'v1')}_"
        
        return message.strip()
