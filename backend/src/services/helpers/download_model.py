import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def download_model() :
  BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
  MODEL_PATH = os.path.join(BASE_DIR, "model")

  os.makedirs(MODEL_PATH, exist_ok=True)  # garante que a pasta exista

  if not os.listdir(MODEL_PATH):
    print("Model path:", MODEL_PATH)

    repository = 'davidshelton/email-classifier-soft'
    tokenizer = AutoTokenizer.from_pretrained(repository)
    model = AutoModelForSequenceClassification.from_pretrained(
      repository, load_in_8bit=True,
    )


    # Se for privado, precisa do token: export HF_TOKEN=xxx
    classifier = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )

    classifier.save_pretrained(MODEL_PATH)

