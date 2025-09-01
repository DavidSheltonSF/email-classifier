# python com pythorch
FROM huggingface/transformers-pytorch-cpu

WORKDIR /backend

ENV PYTHONPATH=/backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#CMD ["sh", "-c", "uvicorn src.main:app --host ${BACKEND_HOST} --port ${BACKEND_PORT} --reload"]
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000"]