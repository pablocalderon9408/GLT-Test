from jwt import encode, decode
from typing import List

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data


class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME ="username",
    MAIL_PASSWORD = "admin123",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "mail server",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_confirmation_email(email):
    html = """
    <p>Thanks for using Fastapi-mail</p> 
    """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    print(fm.send_message(message))
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) 