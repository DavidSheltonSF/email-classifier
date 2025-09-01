FROM python:3.12-slim

WORKDIR /backend

ENV PYTHONPATH=/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python download_model_from_hub.py

#CMD ["sh", "-c", "uvicorn src.main:app --host ${BACKEND_HOST} --port ${BACKEND_PORT} --reload"]
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]