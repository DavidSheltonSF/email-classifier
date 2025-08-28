from services.serviceTypes.Email import Email
from services.helpers import classify_email
from services.errors.email import MissingEmailBodyError, MissingEmailSubjectError

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


    return classify_email(email.get('subject'), email.get('body'))
