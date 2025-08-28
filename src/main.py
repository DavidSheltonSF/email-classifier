from fastapi import FastAPI
from src.controllers import classify_controller

app = FastAPI()

app.include_router(classify_controller.router)