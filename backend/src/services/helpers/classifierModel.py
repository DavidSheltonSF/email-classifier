from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

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
    
    self.model = pipeline(
        'text-classification', 
        model=model, 
        tokenizer=tokenizer
    )

  
  def classify(self, text: str):
    if not self.model:
      raise Exception('Model not loaded!')
    
    return self.model(text)
  