import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controllers import classify_controller
from src.services.helpers.download_model import download_model
from backend.src.services.helpers.ClassifierModel import ClassifierModel

#download_model()

classifier = ClassifierModel()
classifier.load_model()

app = FastAPI()

origins = [
  "http://localhost:5501",
  "http://0.0.0.0:5501",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(classify_controller.router)