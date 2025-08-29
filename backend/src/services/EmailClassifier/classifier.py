from backend.src.services.serviceTypes.Email import Email
from backend.src.services.helpers import classify_email
from backend.src.services.errors.email import MissingEmailBodyError, MissingEmailSubjectError
from backend.src.services.helpers.repliesMap import repliesMap

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

    result = classify_email(subject, body)

    reply = repliesMap[result.get('label')]

    response = {"result": result, "reply": reply}

    return response
