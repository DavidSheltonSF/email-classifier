from services.errors.application import ApplicationError

class MissingEmailSubjectError(ApplicationError):
  status_code = 400
  def __init__(self):
    super().__init__("The email's subject was not provided")
  
class MissingEmailBodyError(ApplicationError):
  status_code = 400
  def __init__(self):
    super().__init__("The email's subject was not provided")