"""
Arquitectura del modelo LSTM para Momentum Predictor
Predicción de señales de trading (BUY/SELL/HOLD)
"""
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

def create_momentum_lstm(input_shape=(60, 20), learning_rate=0.001):
    """
    Crear modelo LSTM para predicción de señales
    
    Architecture:
    - Input: (60 días, 20 features)
    - 3 capas LSTM con BatchNorm y Dropout
    - 2 capas Dense
    - Output: 3 clases (SELL, HOLD, BUY) con softmax
    
    Features (20):
    1. open, high, low, close, volume (5)
    2. RSI, momentum, stochastic_k, stochastic_d (4)
    3. SMA_7, SMA_25, EMA_12, EMA_26 (4)
    4. MACD, MACD_signal (2)
    5. BB_upper, BB_middle, BB_lower (3)
    6. ATR (1)
    7. Price change % (1)
    
    Args:
        input_shape: (lookback_window, num_features)
        learning_rate: Learning rate para Adam optimizer
    
    Returns:
        Modelo compilado
    """
    model = Sequential([
        # Primera capa LSTM
        LSTM(128, return_sequences=True, input_shape=input_shape, name='lstm_1'),
        Dropout(0.2),
        BatchNormalization(),
        
        # Segunda capa LSTM
        LSTM(64, return_sequences=True, name='lstm_2'),
        Dropout(0.2),
        BatchNormalization(),
        
        # Tercera capa LSTM
        LSTM(32, return_sequences=False, name='lstm_3'),
        Dropout(0.2),
        
        # Capas Dense
        Dense(64, activation='relu', name='dense_1'),
        Dropout(0.3),
        
        Dense(32, activation='relu', name='dense_2'),
        
        # Capa de salida: 3 clases (SELL=0, HOLD=1, BUY=2)
        Dense(3, activation='softmax', name='output')
    ], name='MomentumPredictor')
    
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def get_training_callbacks(model_path='momentum_lstm_best.h5'):
    """
    Callbacks para entrenamiento del modelo
    
    Returns:
        Lista de callbacks
    """
    return [
        EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            model_path,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001,
            verbose=1
        )
    ]

def create_model_summary():
    """
    Crear resumen del modelo para documentación
    
    Returns:
        String con arquitectura del modelo
    """
    model = create_momentum_lstm()
    
    print("\n" + "="*60)
    print("MOMENTUM PREDICTOR LSTM - ARQUITECTURA")
    print("="*60)
    model.summary()
    print("="*60)
    print(f"Total de parámetros: {model.count_params():,}")
    print("="*60 + "\n")
    
    return model

if __name__ == "__main__":
    # Mostrar arquitectura del modelo
    create_model_summary()
