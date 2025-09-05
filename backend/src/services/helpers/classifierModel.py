from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from huggingface_hub import login 
import os
from dotenv import load_dotenv
from torch.ao.quantization import quantize_dynamic

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
      repository
    )

    model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
  
    for name, param in model.named_parameters():
        print('oo')
        print(name, param.dtype)

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
  