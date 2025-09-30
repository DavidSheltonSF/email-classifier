from src.services.serviceTypes.Email import Email
from src.services.helpers.ClassifierModel import ClassifierModel
from src.services.errors.email import MissingEmailBodyError, MissingEmailSubjectError
from src.services.helpers.repliesMap import repliesMap

class EmailClassifierService:
  def __init__(self):
    pass

  def execute(self, email: Email):

    subject = email.get('subject')
    body = email.get('body')

    if(subject == None):
      raise MissingEmailSubjectError()
    
    if(body == None):
      raise MissingEmailBodyError()

    #result = classify_email(subject, body)
    classifier = ClassifierModel()

    email = f"{subject} {body}"

    result = classifier.classify(body)[0]

    print(result)
    reply = repliesMap[result.get('label')]

    response = {"result": {"label": result['label']}, "reply": reply}

    return response
