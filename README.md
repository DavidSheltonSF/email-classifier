# Email Spam Classifier

Project: Intelligent Spam Email Classifier

This project is a smart spam email classifier designed for easy use and fast results. Users can type their email directly into the interface, drag and drop .txt files, or upload PDFs to check for spam. The UI provides real-time feedback, showing the status of each operation for a smooth experience.

OBS: The only the email body is analyzed

Backend:

- Python

- FastAPI

- Docker

- Hugging Face AI model for advanced email classification

Frontend:

- JavaScript

- HTML5

- CSS3

This tool combines AI-powered accuracy with an intuitive interface.

The AI model was trained with data provided on Kaggle

## How test it

1 - Clone repository
```bash
git clone https://github.com/DavidSheltonSF/desafio-autoU.git
```

2 - Configure the .env file
```bash
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=5501
```
3 - In main.py file, modify the line bellow, calling load_from_hub_and_save() method,
so the AI model will be download from the hub and saved localy.
```python
classifier = ClassifierModel()
classifier.load_model_localy() # <- substitua esse método
```
4 - Run the command to build the docker container
```bash
docker compose up --build
```