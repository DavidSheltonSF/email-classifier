import os
from transformers import pipeline

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_PATH, exist_ok=True)  # garante que a pasta exista
print("Model path:", MODEL_PATH)

# Se for privado, precisa do token: export HF_TOKEN=xxx
classifier = pipeline(
    'text-classification', 
    model="davidshelton/email-classifier-soft-test", 
    tokenizer="davidshelton/email-classifier-soft-test"
)

classifier.save_pretrained(MODEL_PATH)
