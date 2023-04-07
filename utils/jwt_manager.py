from jwt import encode, decode
from typing import List

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from users.models import User as UserModel
from config.database import Session


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


# class EmailSchema(BaseModel):
#     email: List[EmailStr]


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

def send_confirmation_email(new_user_info, token):
    import ipdb ; ipdb.set_trace()
    db = Session()
    email = new_user_info["email"]
    user = db.query(UserModel).filter(UserModel.email == email).first()
    decoded_token = validate_token(token)
    import ipdb ; ipdb.set_trace()
    if user and decoded_token:
        user.is_validated = True
        db.commit()
        db.refresh(user)
        return JSONResponse(status_code=200, content={"message": "email has been validated"})
    # html = """
    # <p>Thanks for using Fastapi-mail</p> 
    # """

    # message = MessageSchema(
    #     subject="Fastapi-Mail module",
    #     recipients=email.dict().get("email"),
    #     body=html,
    #     subtype=MessageType.html)

    # fm = FastMail(conf)
    # await fm.send_message(message)
    # print(fm.send_message(message))
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) 