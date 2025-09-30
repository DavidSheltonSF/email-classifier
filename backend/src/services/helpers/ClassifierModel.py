from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os

class ClassifierModel:
  _instance = None
  _repository_link = 'davidshelton/email-classifier-soft'
  _local_model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../', 'model'))
  _label_identifiers = {0: "ham", 1: "spam"}

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.model = None
    return cls._instance
  
  def load_model_from_hub_and_save(self):
    if(self.model):
      return 

    tokenizer = AutoTokenizer.from_pretrained(self._repository_link)
    model = AutoModelForSequenceClassification.from_pretrained(
      self._repository_link,
    )
  
    self.model = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )
    self.model.save_pretrained(self._local_model_path)
  
  def load_model_from_hub(self):
    if(self.model):
      return 

    tokenizer = AutoTokenizer.from_pretrained(self._repository_link)
    model = AutoModelForSequenceClassification.from_pretrained(
      self._repository_link,
      id2label=self._label_identifiers
    )
  
    self.model = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )

  def load_model_localy(self):
    if(self.model):
      return None
    
    tokenizer = AutoTokenizer.from_pretrained(f"{self._local_model_path}")
    model = AutoModelForSequenceClassification.from_pretrained(f"{self._local_model_path}", id2label=self._label_identifiers)
    self.model = pipeline('text-classification', model=model, tokenizer=tokenizer)
  
  def classify(self, text: str):
    if not self.model:
      raise Exception('Model not loaded!')
    return self.model(text)
