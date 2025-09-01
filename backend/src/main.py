import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import classify_controller
from huggingface_hub import login
from transformers import pipeline

login(os.getenv('HUGGINGFACE_HUB_TOKEN'))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
MODEL_PATH = os.path.join(BASE_DIR, "model")

if not os.listdir(MODEL_PATH):
  os.makedirs(MODEL_PATH, exist_ok=True)  # garante que a pasta exista
  print("Model path:", MODEL_PATH)

  # Se for privado, precisa do token: export HF_TOKEN=xxx
  classifier = pipeline(
      'text-classification', 
      model="davidshelton/email-classifier-soft-test", 
      tokenizer="davidshelton/email-classifier-soft-test"
  )

  classifier.save_pretrained(MODEL_PATH)

app = FastAPI()

origins = [
  "http://localhost:5501",
  "https://desafio-autou-back.onrender.com:8000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(classify_controller.router)