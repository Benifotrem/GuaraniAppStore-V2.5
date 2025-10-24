"""
Preprocesador de datos para Momentum Predictor
Calcula indicadores técnicos y prepara datos para LSTM
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import ta  # Technical Analysis library

class MomentumPreprocessor:
    def __init__(self, lookback=60):
        """
        Args:
            lookback: Número de días históricos (ventana temporal)
        """
        self.lookback = lookback
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
        # Features que se calcularán
        self.feature_columns = [
            'open', 'high', 'low', 'close', 'volume',
            'rsi_14', 'momentum', 'stochastic_k', 'stochastic_d',
            'sma_7', 'sma_25', 'ema_12', 'ema_26',
            'macd', 'macd_signal',
            'bb_upper', 'bb_middle', 'bb_lower',
            'atr', 'price_change_pct'
        ]
    
    def calculate_indicators(self, df):
        """
        Calcular todos los indicadores técnicos
        
        Args:
            df: DataFrame con columnas ['open', 'high', 'low', 'close', 'volume']
        
        Returns:
            DataFrame con indicadores calculados
        """
        df = df.copy()
        
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        # RSI (Relative Strength Index)
        df['rsi_14'] = ta.momentum.RSIIndicator(close, window=14).rsi()
        
        # Momentum (Rate of Change)
        df['momentum'] = ta.momentum.ROCIndicator(close, window=10).roc()
        
        # Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(high, low, close)
        df['stochastic_k'] = stoch.stoch()
        df['stochastic_d'] = stoch.stoch_signal()
        
        # Moving Averages
        df['sma_7'] = ta.trend.SMAIndicator(close, window=7).sma_indicator()
        df['sma_25'] = ta.trend.SMAIndicator(close, window=25).sma_indicator()
        df['ema_12'] = ta.trend.EMAIndicator(close, window=12).ema_indicator()
        df['ema_26'] = ta.trend.EMAIndicator(close, window=26).ema_indicator()
        
        # MACD
        macd = ta.trend.MACD(close)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        
        # Bollinger Bands
        bb = ta.volatility.BollingerBands(close)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        
        # ATR (Average True Range)
        df['atr'] = ta.volatility.AverageTrueRange(high, low, close).average_true_range()
        
        # Price change percentage
        df['price_change_pct'] = close.pct_change() * 100
        
        # Eliminar NaN generados por indicadores
        df = df.dropna()
        
        return df
    
    def normalize_data(self, df):
        """
        Normalizar features con MinMaxScaler
        
        Args:
            df: DataFrame con indicadores calculados
        
        Returns:
            Array normalizado
        """
        data = df[self.feature_columns].values
        normalized = self.scaler.fit_transform(data)
        return normalized
    
    def create_sequences(self, data, labels=None):
        """
        Crear secuencias temporales para LSTM
        
        Args:
            data: Array normalizado (n_samples, n_features)
            labels: Array de etiquetas (opcional, para training)
        
        Returns:
            X, y (si labels está presente) o solo X
        """
        X = []
        y = [] if labels is not None else None
        
        for i in range(len(data) - self.lookback):
            X.append(data[i:i + self.lookback])
            
            if labels is not None:
                y.append(labels[i + self.lookback])
        
        X = np.array(X)
        
        if y is not None:
            y = np.array(y)
            return X, y
        
        return X
    
    def prepare_for_prediction(self, df):
        """
        Preparar datos para predicción (sin labels)
        
        Args:
            df: DataFrame con al menos 60 días de datos OHLCV
        
        Returns:
            Array listo para model.predict()
        """
        # Calcular indicadores
        df_processed = self.calculate_indicators(df)
        
        # Normalizar
        normalized = self.normalize_data(df_processed)
        
        # Tomar últimos 60 días
        if len(normalized) < self.lookback:
            raise ValueError(f"Se necesitan al menos {self.lookback} días de datos")
        
        sequence = normalized[-self.lookback:]
        
        # Reshape para modelo: (1, lookback, n_features)
        X = sequence.reshape(1, self.lookback, len(self.feature_columns))
        
        return X
    
    def generate_labels(self, df, threshold=0.03):
        """
        Generar labels para entrenamiento
        
        Args:
            df: DataFrame con columna 'close'
            threshold: Umbral de cambio de precio (default 3%)
        
        Returns:
            Array de labels: 0=SELL, 1=HOLD, 2=BUY
        """
        labels = []
        
        for i in range(len(df) - 5):  # Mirar 5 días adelante
            current_price = df['close'].iloc[i]
            future_price = df['close'].iloc[i + 5]
            
            change = (future_price - current_price) / current_price
            
            if change > threshold:
                labels.append(2)  # BUY
            elif change < -threshold:
                labels.append(0)  # SELL
            else:
                labels.append(1)  # HOLD
        
        # Padding para que coincida con el tamaño
        labels.extend([1] * 5)
        
        return np.array(labels)
