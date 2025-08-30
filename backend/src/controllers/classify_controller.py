from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.src.services.EmailClassifier.classifier import EmailClassifierService
from backend.src.services.errors.email import ApplicationError

router = APIRouter(prefix='/classify', tags=['classify'])
classifier = EmailClassifierService()

@router.post('/email')
def classify_email(email: dict):
  try:
    data = classifier.execute(email)
    return JSONResponse(
      status_code=200,
      content={'status': 'success', 'data': data}
    )
  except ApplicationError as e:
    return JSONResponse(
      status_code=e.status_code,
      content={'status': 'error', 'message': e.message}
    )