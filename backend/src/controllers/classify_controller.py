import PyPDF2
import io
from fastapi import APIRouter, UploadFile, File
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
  
@router.post('/email-pdf')
async def classify_email_pdf(file: UploadFile = File(...)):

  print(type(file))
  pdf_bytes = await file.read()
  pdf_file = io.BytesIO(pdf_bytes)
  pdf_reader = PyPDF2.PdfReader(pdf_file)

  email_string = ''

  for page in pdf_reader.pages:
    email_string += f"\n{page.extract_text()}"


  email_split = email_string.split('\n')

  email = {
    "subject": email_split.pop(0),
    "body": '\n'.join(email_split)
  }

  data = classifier.execute(email)

  return JSONResponse(
      status_code=200,
      content={'status': 'success', 'data': data}
    )