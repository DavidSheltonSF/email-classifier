import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from src.services.serviceTypes.EmailClassification import EmailClassification

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model")
print(MODEL_PATH)

classifier = pipeline('text-classification', model="davidshelton/email-classifier-soft-test", tokenizer="davidshelton/email-classifier-soft-test")
classifier.save_pretrained(MODEL_PATH)