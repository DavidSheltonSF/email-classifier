import PyPDF2
import io
import os
from dotenv import load_dotenv
from datasets import Dataset, DatasetDict
from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from src.services.EmailClassifier.classifier import EmailClassifierService
from src.services.errors.email import ApplicationError
from backend.src.services.helpers.download_model_from_hub import download_model_from_hub
import pandas as pd
from huggingface_hub import login

load_dotenv()

login(os.getenv('HUGGINGFACE_HUB_TOKEN'))

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
  try:
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
  except ApplicationError as e:
    return JSONResponse(
      status_code=e.status_code,
      content={'status': 'error', 'message': e.message}
    )
  
@router.post('/save-dataset')
async def save_data_set(files: List[UploadFile] = File(...)):

  try:
    
    train_content = await files[0].read()
    train_decoded = train_content.decode('utf-8')
    train_buffer = io.StringIO(train_decoded)
    train_df = pd.read_csv(train_buffer)

    test_content = await files[1].read()
    test_decoded = test_content.decode('utf-8')
    test_buffer = io.StringIO(test_decoded)
    test_df = pd.read_csv(test_buffer)

    
  
    dataset = DatasetDict({
      "train": Dataset.from_pandas(train_df),
      "test": Dataset.from_pandas(test_df)
    })

    dataset.push_to_hub("davidshelton/email-classifier-soft-dataset")

    return JSONResponse(
    status_code=200,
    content={'status': 'success', 'message': 'Dataset uploaded successfuly'}
    )
  except ApplicationError as e:
    return JSONResponse(
      status_code=e.status_code,
      content={'status': 'error', 'message': e.message}
    )
  
@router.post('/download-model')
def download_model():
  try:
    result = download_model_from_hub()
    if(result):
      return JSONResponse(
      status_code=200,
      content={'status': 'success', 'message': 'model downloaded successfuly'}
    )

    return JSONResponse(
      status_code=200,
      content={'status': 'error', 'message': 'model was not downloaded'}
    )

  except ApplicationError as e:
    return JSONResponse(
      status_code=e.status_code,
      content={'status': 'error', 'message': e.message}
    )