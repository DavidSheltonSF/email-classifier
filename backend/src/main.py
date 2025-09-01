from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import classify_controller
import src.download_model_from_hub

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