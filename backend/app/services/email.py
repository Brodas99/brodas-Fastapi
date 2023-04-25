import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta 
from app.models.user.user import UserPassword_Update

from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.jwt.token import JWTMeta, JWTCreds, JWTPayload
from app.models.user.user import UserPassword_Update, UserInDB

from typing import Optional
from fastapi import HTTPException, status
from pydantic import ValidationError


class Email:
    def __init__(self):
        self.port = 587

    def send_email(self, subject, body, receiver_email, cc_list= None):
        
        # if cc_list:
        #     cc_list_string = ", ".join(cc_list)
        
        sender_email = "b.rodasdiaz@gmail.com"
        password = "Nalamijo99!"
        # Create a multipart message and set headers
        message = MIMEMultipart(body)
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message['Cc'] = cc_list
        
        # Add body to email
        message.attach(MIMEText(body, "html"))
        text = message.as_string()
        
        with smtplib.SMTP("smtp-mail.outlook.com", self.port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
            server.quit()


        

        