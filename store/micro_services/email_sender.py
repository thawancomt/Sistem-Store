import smtplib
from email.mime.text import MIMEText

from os import environ

EMAIL_SENDER = environ.get('EMAIL_ADRESS')
EMAIL_SENDER_PWD = environ.get('EMAIL_PWD')

class Email:
    
    def __init__(self, recipient_email: str, id = None) -> None:
        from .code_verification import CodeService
        
        if not recipient_email:
            raise ValueError("Recipient email is required.")
        
        self.__code = CodeService(id=id)
        
        self.code = self.__code._no_hashed_code
        
        self.subject = 'Welcome to our System'
        
        self.body = f'Welcome to the most powerful system you have ever seen. \
                    \nYou have been set as a low-level user. To change this, please contact your manager. \
                    \nYour account is under verification. Here is the code to confirm your registration: {self.code}'
                    
        self._email_address = EMAIL_SENDER
        self.recipient_email = recipient_email
        
        
    def create_body(self):
        msg = MIMEText(self.body)
        msg['Subject'] = self.subject
        msg['From'] = self._email_address
        msg['To'] = self.recipient_email
        return msg
    
    def send_email(self, code = False):
        self.body = self.create_body()
        
        if code:
            self._set_email_body()
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_SENDER_PWD)

        # Send the email
        server.sendmail(self._email_address, self.recipient_email, self.body.as_string())

        server.quit()

    def _set_email_body(self):
        from store.blueprints.users.services.UserService import UserService
        from store.micro_services.code_verification import CodeService
        
        user = UserService(email=self.recipient_email).get_user_by_email()

        code_service = CodeService(user.id)

        self.body = f'Welcome {user.username}.\nThe code to register is: {code_service._no_hashed_code}'
        self.body = self.create_body()


    