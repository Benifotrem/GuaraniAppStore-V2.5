"""
Servicio de predicción de Momentum Predictor
Genera señales de trading con LSTM
"""
import os
import ccxt
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Optional
import joblib

from momentum_preprocessor import MomentumPreprocessor

class MomentumPredictorService:
    def __init__(self, model_path=None, scaler_path=None, use_mock=True):
        """
        Inicializar servicio de predicción
        
        Args:
            model_path: Ruta al modelo .h5 (opcional)
            scaler_path: Ruta al scaler .pkl (opcional)
            use_mock: Si True, usa predicciones mock (para testing)
        """
        self.use_mock = use_mock
        self.model = None
        self.preprocessor = MomentumPreprocessor(lookback=60)
        
        # Cargar modelo si existe
        if model_path and os.path.exists(model_path) and not use_mock:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Modelo cargado: {model_path}")
            self.use_mock = False
            
            # Cargar scaler
            if scaler_path and os.path.exists(scaler_path):
                self.preprocessor.scaler = joblib.load(scaler_path)
                print(f"✅ Scaler cargado")
        else:
            print("⚠️ Modelo no encontrado - Usando predicciones MOCK")
            print("   Para entrenar el modelo, ejecuta: python train_momentum_model.py")
            self.use_mock = True
        
        # Exchange para obtener datos (usando Kraken - sin restricciones)
        self.exchange = ccxt.kraken()
    
    def fetch_recent_data(self, symbol, days=60):
        """
        Obtener datos recientes de un símbolo
        
        Args:
            symbol: Símbolo (ej: BTC)
            days: Días de historia
        
        Returns:
            DataFrame con OHLCV
        """
        pair = f"{symbol}/USDT"
        
        try:
            ohlcv = self.exchange.fetch_ohlcv(
                pair,
                timeframe='1d',
                limit=days + 30  # Extra para indicadores
            )
            
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            return df
        except Exception as e:
            print(f"❌ Error obteniendo datos de {symbol}: {e}")
            return None
    
    def predict_signal(self, symbol: str) -> Dict:
        """
        Generar señal de trading para un símbolo
        
        Args:
            symbol: Símbolo de cripto (ej: BTC, ETH)
        
        Returns:
            Dict con señal completa
        """
        print(f"\n📊 Generando señal para {symbol}...")
        
        # 1. Obtener datos recientes
        df = self.fetch_recent_data(symbol, days=90)
        
        if df is None or len(df) < 60:
            raise Exception(f"No hay suficientes datos para {symbol}")
        
        # 2. Precio actual
        current_price = float(df['close'].iloc[-1])
        
        # 3. Si no hay modelo, usar predicción MOCK
        if self.use_mock:
            return self._generate_mock_signal(symbol, current_price, df)
        
        # 4. Preparar para predicción
        X = self.preprocessor.prepare_for_prediction(df)
        
        # 5. Predecir
        predictions = self.model.predict(X, verbose=0)[0]
        
        # 6. Interpretar predicción
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class]) * 100
        
        signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
        signal = signal_map[predicted_class]
        
        # 7. Calcular niveles de trading
        levels = self._calculate_trading_levels(signal, current_price, confidence)
        
        # 8. Construir resultado
        result = {
            'symbol': symbol,
            'signal': signal,
            'confidence': round(confidence, 2),
            
            'current_price': round(current_price, 2),
            'entry_price': levels['entry'],
            'target_1': levels['target_1'],
            'target_2': levels['target_2'],
            'stop_loss': levels['stop_loss'],
            
            'timeframe': self._calculate_timeframe(confidence),
            'risk_level': self._calculate_risk(signal, confidence),
            
            'probabilities': {
                'SELL': round(float(predictions[0]) * 100, 2),
                'HOLD': round(float(predictions[1]) * 100, 2),
                'BUY': round(float(predictions[2]) * 100, 2)
            },
            
            'predicted_at': datetime.now(timezone.utc).isoformat(),
            'model_version': 'v1.0.0',
            'is_mock': False
        }
        
        print(f"✅ Señal generada: {signal} ({confidence:.1f}% confidence)")
        
        return result
    
    def _generate_mock_signal(self, symbol, current_price, df):
        """
        Generar señal MOCK para testing (sin modelo entrenado)
        
        Usa indicadores técnicos completos para simular una señal más realista
        """
        print("⚠️ Generando señal MOCK con indicadores técnicos completos")
        
        try:
            # Calcular todos los indicadores técnicos usando el preprocessor
            df_with_indicators = self.preprocessor.calculate_indicators(df)
            
            # Obtener valores actuales de los indicadores
            last_row = df_with_indicators.iloc[-1]
            
            rsi = last_row['rsi_14']
            macd = last_row['macd']
            macd_signal = last_row['macd_signal']
            sma_7 = last_row['sma_7']
            sma_25 = last_row['sma_25']
            bb_upper = last_row['bb_upper']
            bb_lower = last_row['bb_lower']
            stoch_k = last_row['stochastic_k']
            
            # Sistema de puntos para determinar señal
            buy_score = 0
            sell_score = 0
            
            # 1. RSI Analysis (peso: 2 puntos)
            if rsi < 30:  # Oversold
                buy_score += 2
            elif rsi > 70:  # Overbought
                sell_score += 2
            elif 45 <= rsi <= 55:  # Neutral
                pass
            elif rsi < 45:
                buy_score += 1
            else:
                sell_score += 1
            
            # 2. MACD Analysis (peso: 2 puntos)
            if macd > macd_signal and macd > 0:
                buy_score += 2
            elif macd < macd_signal and macd < 0:
                sell_score += 2
            elif macd > macd_signal:
                buy_score += 1
            else:
                sell_score += 1
            
            # 3. Moving Averages (peso: 2 puntos)
            if current_price > sma_7 > sma_25:
                buy_score += 2
            elif current_price < sma_7 < sma_25:
                sell_score += 2
            elif current_price > sma_7:
                buy_score += 1
            else:
                sell_score += 1
            
            # 4. Bollinger Bands (peso: 1 punto)
            if current_price < bb_lower:
                buy_score += 1
            elif current_price > bb_upper:
                sell_score += 1
            
            # 5. Stochastic (peso: 1 punto)
            if stoch_k < 20:
                buy_score += 1
            elif stoch_k > 80:
                sell_score += 1
            
            # Determinar señal basada en puntuación (máximo 8 puntos por lado)
            if buy_score >= sell_score + 2:
                signal = 'BUY'
                # Confianza basada en diferencia de scores
                confidence_base = min(50 + (buy_score - sell_score) * 8, 85)
                probabilities = [
                    max(0.10, (8 - buy_score) / 10),  # SELL
                    max(0.15, 1 - confidence_base/100 - 0.15),  # HOLD
                    confidence_base / 100  # BUY
                ]
            elif sell_score >= buy_score + 2:
                signal = 'SELL'
                confidence_base = min(50 + (sell_score - buy_score) * 8, 85)
                probabilities = [
                    confidence_base / 100,  # SELL
                    max(0.15, 1 - confidence_base/100 - 0.15),  # HOLD
                    max(0.10, (8 - sell_score) / 10)  # BUY
                ]
            else:
                signal = 'HOLD'
                # For HOLD, confidence varies based on how close the scores are
                score_diff = abs(buy_score - sell_score)
                confidence_base = max(50, 65 - score_diff * 5)  # Lower confidence when scores are closer
                
                # Make probabilities dynamic based on which score is higher
                if buy_score > sell_score:
                    # Slight BUY bias
                    probabilities = [0.15, 0.55, 0.30]
                elif sell_score > buy_score:
                    # Slight SELL bias
                    probabilities = [0.30, 0.55, 0.15]
                else:
                    # Equal scores - neutral
                    probabilities = [0.20, 0.60, 0.20]
            
            # Normalizar probabilidades para que sumen 1
            prob_sum = sum(probabilities)
            probabilities = [p / prob_sum for p in probabilities]
            
            # Use confidence_base instead of max(probabilities) for more dynamic calculation
            confidence = confidence_base
            
            # Calcular niveles
            levels = self._calculate_trading_levels(signal, current_price, confidence)
            
            # Información de indicadores para debugging
            indicators_info = {
                'rsi': round(rsi, 2),
                'macd': round(macd, 4),
                'sma_7': round(sma_7, 2),
                'sma_25': round(sma_25, 2),
                'stoch_k': round(stoch_k, 2),
                'buy_score': buy_score,
                'sell_score': sell_score
            }
            
            print(f"   RSI: {rsi:.1f}, MACD: {macd:.2f}, SMA7: ${sma_7:.2f}, SMA25: ${sma_25:.2f}")
            print(f"   Scores - BUY: {buy_score}, SELL: {sell_score} → {signal}")
            
            return {
                'symbol': symbol,
                'signal': signal,
                'confidence': round(confidence, 2),
                
                'current_price': round(current_price, 2),
                'entry_price': levels['entry'],
                'target_1': levels['target_1'],
                'target_2': levels['target_2'],
                'stop_loss': levels['stop_loss'],
                
                'timeframe': self._calculate_timeframe(confidence),
                'risk_level': self._calculate_risk(signal, confidence),
                
                'probabilities': {
                    'SELL': round(probabilities[0] * 100, 2),
                    'HOLD': round(probabilities[1] * 100, 2),
                    'BUY': round(probabilities[2] * 100, 2)
                },
                
                'indicators': indicators_info,
                
                'predicted_at': datetime.now(timezone.utc).isoformat(),
                'model_version': 'MOCK_v2_Technical_Analysis',
                'is_mock': True
            }
            
        except Exception as e:
            print(f"   Error calculando indicadores: {e}")
            print("   Usando lógica simple de respaldo...")
            
            # Fallback a lógica simple
            close = df['close'].iloc[-20:]
            sma_7 = close.rolling(7).mean().iloc[-1]
            sma_25 = close.rolling(25).mean().iloc[-1] if len(close) >= 25 else close.mean()
            
            if current_price > sma_7 > sma_25:
                signal = 'BUY'
                probabilities = [0.15, 0.20, 0.65]
            elif current_price < sma_7 < sma_25:
                signal = 'SELL'
                probabilities = [0.65, 0.20, 0.15]
            else:
                signal = 'HOLD'
                probabilities = [0.20, 0.60, 0.20]
            
            confidence = max(probabilities) * 100
            levels = self._calculate_trading_levels(signal, current_price, confidence)
            
            return {
                'symbol': symbol,
                'signal': signal,
                'confidence': round(confidence, 2),
                'current_price': round(current_price, 2),
                'entry_price': levels['entry'],
                'target_1': levels['target_1'],
                'target_2': levels['target_2'],
                'stop_loss': levels['stop_loss'],
                'timeframe': self._calculate_timeframe(confidence),
                'risk_level': self._calculate_risk(signal, confidence),
                'probabilities': {
                    'SELL': round(probabilities[0] * 100, 2),
                    'HOLD': round(probabilities[1] * 100, 2),
                    'BUY': round(probabilities[2] * 100, 2)
                },
                'predicted_at': datetime.now(timezone.utc).isoformat(),
                'model_version': 'MOCK_v1_Simple',
                'is_mock': True
            }
    
    def _calculate_trading_levels(self, signal, current_price, confidence):
        """Calcular niveles de entrada, targets y stop loss"""
        if signal == 'BUY':
            entry = current_price * 0.99
            target_1 = current_price * 1.05
            target_2 = current_price * 1.08
            stop_loss = current_price * 0.96
        elif signal == 'SELL':
            entry = current_price * 1.01
            target_1 = current_price * 0.95
            target_2 = current_price * 0.92
            stop_loss = current_price * 1.04
        else:  # HOLD
            entry = current_price
            target_1 = current_price * 1.02
            target_2 = current_price * 1.03
            stop_loss = current_price * 0.98
        
        return {
            'entry': round(entry, 2),
            'target_1': round(target_1, 2),
            'target_2': round(target_2, 2),
            'stop_loss': round(stop_loss, 2)
        }
    
    def _calculate_timeframe(self, confidence):
        """Calcular timeframe según confianza"""
        if confidence >= 80:
            return 'short'  # 1-3 días
        elif confidence >= 60:
            return 'mid'    # 3-7 días
        else:
            return 'long'   # 7+ días
    
    def _calculate_risk(self, signal, confidence):
        """Calcular nivel de riesgo"""
        if signal == 'HOLD':
            return 'low'
        elif confidence >= 75:
            return 'medium'
        else:
            return 'high'
    
    def format_telegram_message(self, prediction: Dict) -> str:
        """
        Formatear predicción para mensaje de Telegram
        
        Args:
            prediction: Dict retornado por predict_signal()
        
        Returns:
            Mensaje formateado en Markdown
        """
        signal_emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡'
        }
        
        risk_emoji = {
            'low': '🟢',
            'medium': '🟠',
            'high': '🔴'
        }
        
        mock_warning = "\n⚠️ *MOCK Signal* (Modelo no entrenado)\n" if prediction.get('is_mock') else ""
        
        message = f"""🎯 *Momentum Predictor Signal*
{mock_warning}
*Token:* {prediction['symbol']}
*Price:* ${prediction['current_price']:,.2f}

{signal_emoji[prediction['signal']]} *Signal:* *{prediction['signal']}*
*Confidence:* {prediction['confidence']:.1f}%

📊 *Trading Levels:*
*Entry:* ${prediction['entry_price']:,.2f}
*Target 1:* ${prediction['target_1']:,.2f} (+{((prediction['target_1']/prediction['current_price']-1)*100):.1f}%)
*Target 2:* ${prediction['target_2']:,.2f} (+{((prediction['target_2']/prediction['current_price']-1)*100):.1f}%)
*Stop Loss:* ${prediction['stop_loss']:,.2f} ({((prediction['stop_loss']/prediction['current_price']-1)*100):.1f}%)

⏱ *Timeframe:* {prediction['timeframe'].title()}-term
{risk_emoji[prediction['risk_level']]} *Risk:* {prediction['risk_level'].title()}

_Momentum Predictor IA {prediction['model_version']}_
        """.strip()
        
        return message
