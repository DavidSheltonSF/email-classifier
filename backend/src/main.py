import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import classify_controller
from transformers import pipeline

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
MODEL_PATH = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_PATH, exist_ok=True)  # garante que a pasta exista

if not os.listdir(MODEL_PATH):
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
  "http://localhost:8000",
  "http://0.0.0.0:8000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(classify_controller.router)