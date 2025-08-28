from src.services.serviceTypes.Email import Email
from src.services.helpers import classify_email
from src.services.errors.email import MissingEmailBodyError, MissingEmailSubjectError

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
    
    print('BOI===============================')


    return classify_email(subject, body)
