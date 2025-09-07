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
  _repository_link = 'davidshelton/email-classifier-soft'
  _local_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../', 'model'))

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.model = None
    return cls._instance
  
  def load_model_from_hub(self):
    if(self.model):
      return 

    tokenizer = AutoTokenizer.from_pretrained(self._repository_link)
    model = AutoModelForSequenceClassification.from_pretrained(
      self._repository_link
    )

    model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
  
    self.model = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )
    #self.model.save_pretrained('./backend/model')

  def classify(self, text: str):
    if not self.model:
      raise Exception('Model not loaded!')
    
    return self.model(text)
  