from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.services.EmailClassifier.classifier import EmailClassifierService
from src.services.errors.email import ApplicationError

app = FastAPI()
classifier = EmailClassifierService()

@app.post('/classify')
def classify(email: dict):
  try:
    result = classifier.execute(email)
    return JSONResponse(
      status_code=200,
      content={'status': 'success', 'result': result}
    )
  except ApplicationError as e:
    return JSONResponse(
      status_code=e.status_code,
      content={'status': 'error', 'messge': e.message}
    )