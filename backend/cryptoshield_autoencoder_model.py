"""
Modelo Autoencoder para detección de fraude en transacciones blockchain
Detecta anomalías en patrones de transacciones
"""
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def create_fraud_autoencoder(input_dim=15, encoding_dim=8, learning_rate=0.001):
    """
    Crear modelo Autoencoder para detección de fraude
    
    El autoencoder se entrena solo con transacciones normales.
    Transacciones fraudulentas tendrán alto error de reconstrucción.
    
    Architecture:
    - Input: 15 features de transacción
    - Encoder: 15 → 12 → 8 (bottleneck)
    - Decoder: 8 → 12 → 15 (reconstrucción)
    
    Features (15):
    1. transaction_value (normalizado)
    2. gas_price
    3. gas_used
    4. transaction_fee
    5. value_to_fee_ratio
    6. is_contract_creation
    7. time_since_last_tx (segundos)
    8. sender_balance
    9. receiver_balance
    10. sender_tx_count
    11. receiver_tx_count
    12. value_change_from_avg
    13. hour_of_day (0-23)
    14. day_of_week (0-6)
    15. is_round_number (0/1)
    
    Args:
        input_dim: Número de features
        encoding_dim: Dimensión del bottleneck
        learning_rate: Learning rate
    
    Returns:
        Modelo compilado
    """
    
    # Input layer
    input_layer = Input(shape=(input_dim,), name='input')
    
    # Encoder
    encoded = Dense(12, activation='relu', name='encoder_1')(input_layer)
    encoded = BatchNormalization(name='bn_encoder_1')(encoded)
    encoded = Dropout(0.2, name='dropout_encoder_1')(encoded)
    
    encoded = Dense(encoding_dim, activation='relu', name='bottleneck')(encoded)
    encoded = BatchNormalization(name='bn_bottleneck')(encoded)
    
    # Decoder
    decoded = Dense(12, activation='relu', name='decoder_1')(encoded)
    decoded = BatchNormalization(name='bn_decoder_1')(decoded)
    decoded = Dropout(0.2, name='dropout_decoder_1')(decoded)
    
    decoded = Dense(input_dim, activation='sigmoid', name='output')(decoded)
    
    # Autoencoder model
    autoencoder = Model(inputs=input_layer, outputs=decoded, name='FraudAutoencoder')
    
    # Compilar con Mean Squared Error (para reconstrucción)
    autoencoder.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='mse',
        metrics=['mae']
    )
    
    return autoencoder

def get_training_callbacks(model_path='cryptoshield_autoencoder_best.h5'):
    """
    Callbacks para entrenamiento
    
    Returns:
        Lista de callbacks
    """
    return [
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            model_path,
            monitor='val_loss',
            save_best_only=True,
            verbose=1
        )
    ]

def calculate_reconstruction_error(autoencoder, X):
    """
    Calcular error de reconstrucción
    
    Args:
        autoencoder: Modelo entrenado
        X: Features de transacción
    
    Returns:
        Error de reconstrucción (MSE)
    """
    reconstruction = autoencoder.predict(X, verbose=0)
    mse = tf.keras.losses.MeanSquaredError()
    return float(mse(X, reconstruction).numpy())

def is_fraudulent(reconstruction_error, threshold=0.5):
    """
    Determinar si una transacción es fraudulenta
    
    Args:
        reconstruction_error: Error de reconstrucción
        threshold: Umbral (calibrar con datos de validación)
    
    Returns:
        (is_fraud, risk_score)
    """
    # Normalizar error a score 0-100
    risk_score = min(reconstruction_error * 200, 100)
    
    is_fraud = reconstruction_error > threshold
    
    return is_fraud, risk_score

def create_model_summary():
    """
    Crear resumen del modelo
    
    Returns:
        Modelo para inspección
    """
    model = create_fraud_autoencoder()
    
    print("\n" + "="*60)
    print("CRYPTOSHIELD AUTOENCODER - ARQUITECTURA")
    print("="*60)
    model.summary()
    print("="*60)
    print(f"Total de parámetros: {model.count_params():,}")
    print("="*60 + "\n")
    
    return model

if __name__ == "__main__":
    # Mostrar arquitectura del modelo
    create_model_summary()
