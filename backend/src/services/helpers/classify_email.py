import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from src.services.serviceTypes.EmailClassification import EmailClassification

def classify_email(subject, body) -> EmailClassification:
  email = f"{subject} {body}"
  BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
  MODEL_PATH = os.path.join(BASE_DIR, "data", "model")
  TOKENIZER_PATH = os.path.join(BASE_DIR, "data", "tokenizer")

  model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, id2label={0: 'produtivo', 1: 'improdutivo'})
  tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
  classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
  result = classifier(email)

  return {"label": result[0].get('label'), "score": result[0].get('score')}

