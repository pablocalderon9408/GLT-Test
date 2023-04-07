from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

from config.database import Session
from users.models import User as UserModel

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@email.com":
            db = Session()
            authorized_email = db.query(UserModel).filter(UserModel.email == data['email'], UserModel.is_validated == True).first()
            if not authorized_email:
                raise HTTPException(status_code=403, detail="Credenciales son invalidas")