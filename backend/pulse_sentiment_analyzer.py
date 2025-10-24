"""
Analizador de sentimiento usando BERT para textos crypto
Usa FinBERT (modelo fine-tuned para textos financieros)
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class PulseSentimentAnalyzer:
    def __init__(self):
        """
        Inicializar modelo BERT fine-tuned para crypto sentiment
        """
        # Usar modelo pre-entrenado para sentimiento financiero
        model_name = "ProsusAI/finbert"
        
        print("🤖 Cargando modelo FinBERT...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Mover a GPU si está disponible
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        self.model.eval()
        
        print(f"✅ Sentiment Analyzer cargado (device: {self.device})")
    
    def analyze_text(self, text: str) -> dict:
        """
        Analizar sentimiento de un texto
        
        Args:
            text: Texto a analizar
        
        Returns:
            Dict con sentiment score y label
        """
        if not text or len(text.strip()) < 10:
            return {
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral',
                'confidence': 0.0,
                'probabilities': {'negative': 0.33, 'neutral': 0.34, 'positive': 0.33}
            }
        
        # Tokenizar
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)
        
        # Predecir
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Interpretar resultados
        # FinBERT retorna: [negative, neutral, positive]
        probs = predictions.cpu().numpy()[0]
        
        # Calcular sentiment score (-1 a +1)
        sentiment_score = (probs[2] - probs[0])  # positive - negative
        
        # Determinar label
        label_map = ['negative', 'neutral', 'positive']
        label = label_map[np.argmax(probs)]
        
        return {
            'sentiment_score': float(sentiment_score),
            'sentiment_label': label,
            'confidence': float(np.max(probs)),
            'probabilities': {
                'negative': float(probs[0]),
                'neutral': float(probs[1]),
                'positive': float(probs[2])
            }
        }
    
    def analyze_batch(self, texts: list) -> list:
        """
        Analizar múltiples textos en batch (más eficiente)
        
        Args:
            texts: Lista de textos
        
        Returns:
            Lista de resultados
        """
        results = []
        
        for text in texts:
            result = self.analyze_text(text)
            results.append(result)
        
        return results
    
    def detect_fomo_fud(self, text: str) -> dict:
        """
        Detectar FOMO (Fear of Missing Out) o FUD (Fear, Uncertainty, Doubt)
        
        Args:
            text: Texto a analizar
        
        Returns:
            Dict con scores FOMO/FUD
        """
        text_lower = text.lower()
        
        # Keywords FOMO
        fomo_keywords = [
            'moon', 'to the moon', 'lambo', 'millionaire',
            'get rich', 'dont miss', 'last chance', 'fomo',
            'pump', 'rally', 'breakout', 'explode', 'rocket',
            '100x', '10x', 'gem', 'early'
        ]
        
        # Keywords FUD
        fud_keywords = [
            'crash', 'dump', 'scam', 'rug pull', 'rugpull',
            'ponzi', 'bubble', 'collapse', 'plummet',
            'fud', 'bearish', 'sell', 'exit', 'warning',
            'risk', 'danger', 'fear', 'uncertainty'
        ]
        
        fomo_count = sum(1 for kw in fomo_keywords if kw in text_lower)
        fud_count = sum(1 for kw in fud_keywords if kw in text_lower)
        
        # Calcular scores (0-100)
        fomo_score = min(fomo_count * 20, 100)
        fud_score = min(fud_count * 20, 100)
        
        return {
            'fomo_score': fomo_score,
            'fud_score': fud_score,
            'dominant': 'FOMO' if fomo_score > fud_score else 'FUD' if fud_score > 0 else 'NEUTRAL'
        }
