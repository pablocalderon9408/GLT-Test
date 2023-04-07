import os
import requests

# Envs
from dotenv import load_dotenv

# JWT
from jwt import encode, decode

# Typing
from typing import List

# FastAPI
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

# Models
from users.models import User as UserModel

# Database
from config.database import Session

# Load environ needed variables.
load_dotenv()
from_email = os.getenv("FROM_EMAIL")
api_key = os.getenv("SENDGRID_API_KEY")
email_name = os.getenv("EMAIL_NAME")
url = os.getenv("URL_EMAIL_SERVICE")

class JWTBearer(HTTPBearer):
    """
    This class is used to validate the token
    and grant access to the endpoints.
    """
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@email.com":
            db = Session()
            authorized_email = db.query(UserModel).filter(UserModel.email == data['email'], UserModel.is_validated == True).first()
            if not authorized_email:
                raise HTTPException(status_code=403, detail="Credenciales son invalidas")


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data


def send_email(email, token):
    """
    Email is sent to user to validate the email.
    """

    # Dictionary structure is given by the SendGrid API.
    # https://docs.sendgrid.com/for-developers/sending-email/api-getting-started
    data = {
        "personalizations":[
            {
                "to":[
                    {
                        "email": email,
                        "name":"John Doe"
                    }
                    ],
                "subject": f"Hello!! Welcome to the app! Use this token: {token} to validate your email."
            }
        ],
        "content": [
            {
                "type": "text/plain", 
                "value": "Heya!"
            }
            ],
        "from":{
            "email":from_email,
            "name":email_name
        },
        "reply_to":{
            "email":from_email,
            "name":email_name
        }
    }

    # Headers are given by the SendGrid API. Note the Bearer.
    headers = {
        "Authorization": "Bearer " + api_key,
    }

    # Facilitate the testing.
    print(token)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 202:
        return True
    else:
        return False
