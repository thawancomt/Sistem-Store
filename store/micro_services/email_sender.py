import smtplib
from email.mime.text import MIMEText

import random

class Email:
    def __init__(self, recipient_email: str,) -> None:
        
        if not recipient_email:
            raise ValueError("Recipient email is required.")
        
        self.subject = 'Welcome to our System'
        self.body = f'Welcome to the most powerful system you have ever seen.\nYou have been set as a low-level user. To change this, please contact your manager.\nYour account is under verification. Here is the code to confirm your registration:{random.randint(1000, 9999)}'
        self._email_address = "thawancomt@gmail.com"
        self.recipient_email = recipient_email
        
    
    def create_body(self):
        msg = MIMEText(self.body)
        msg['Subject'] = self.subject
        msg['From'] = self._email_address
        msg['To'] = self.recipient_email
        return msg
    
    def send_email(self, code = False):
        if code:
            from store.blueprints.users.services.UserService import UserService
            from store.micro_services.code_verification import CodeService
            
            user = UserService(email=self.recipient_email).get_user_by_email()
            
            code_service = CodeService(user.id).insert_new_code()
            
            self.body = f'The code to register is: {code_service._code}'
        
        self.email_body = self.create_body()
            
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(self._email_address, "lalh mjqa xrft inot")  # Use an app-specific password for security

        # Send the email
        server.sendmail(self._email_address, self.recipient_email, self.email_body.as_string())
        
        server.quit()


    