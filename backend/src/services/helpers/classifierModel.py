from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from huggingface_hub import login 
import os
from dotenv import load_dotenv

load_dotenv()

login(os.getenv('HUGGINGFACE_HUB_TOKEN'))

class ClassifierModel:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.model = None
    return cls._instance
  
  def load_model(self):
    if(self.model):
      return None

    repository = 'davidshelton/email-classifier-soft'

    tokenizer = AutoTokenizer.from_pretrained(repository)
    model = AutoModelForSequenceClassification.from_pretrained(
      repository, id2label={0: 'produtivo', 1: 'improdutivo'}
    )
    
    self.model = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )
    #self.model.push_to_hub(repository)

  def classify(self, text: str):
    if not self.model:
      raise Exception('Model not loaded!')
    
    return self.model(text)
  