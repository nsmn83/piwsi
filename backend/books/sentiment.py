from transformers import pipeline

# Inicjalizacja pipeline'u raz przy starcie
sentiment_pipeline = pipeline("sentiment-analysis", model="bardsai/twitter-sentiment-pl-base")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label']