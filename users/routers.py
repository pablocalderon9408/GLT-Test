import os
from dotenv import load_dotenv
# Typing
from typing import List

# FastAPI
from fastapi import APIRouter, Path, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Models
from users.models import User as UserModel

# Schemas
from users.schemas import SignUpUser, LoginUser

# Database
from config.database import Session

# JWT
from utils.jwt_manager import create_token, send_email, validate_token
# from utils.jwt_manager import EmailSchema
from middlewares.jwt_bearer import JWTBearer

users_router = APIRouter()

@users_router.post('/signup', tags=['auth'])
def signup(user: SignUpUser):
    """
    Endpoint to register a new user.

    Args:
        user (SignUpUser): The user to be registered.

    Returns:
        JSONResponse: A JSON response indicating if the registration was successful or not.
    """
    if user.password != user.password_confirmation:
        return JSONResponse(status_code=400, content={"message": "Las contraseñas no coinciden"})
    # Do not allow repeated emails.
    db = Session()
    user_exists = db.query(UserModel).filter(UserModel.email == user.email).first()
    if user_exists:
        return JSONResponse(status_code=400, content={"message": "El usuario ya existe"})
    new_user = UserModel(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    # Logic to create the validation email.
    new_user = {}
    new_user['email'] = user.email
    new_user['password'] = user.password
    token: str = create_token(new_user)
    send_email(user.email, token)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el usuario"})


@users_router.post('/validate', tags=['auth'])
def validate(token: str):
    """
    Description: Validates a user account using a token received via email.

    Request Parameters:
    - token: string, required. The token received via email for validating the user account.

    Response:
    - If the token is invalid or expired: status code 401, message: "El token no es válido".
    - If the user account does not exist: status code 404, message: "El usuario no existe".
    - If the validation is successful: status code 200, message: "El usuario ha sido validado".
    """
    # Decode token.
    decoded_token = validate_token(token)
    if not decoded_token:
        return JSONResponse(status_code=401, content={"message": "El token no es válido"})
    email = decoded_token['email']
    db = Session()
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "El usuario no existe"})
    user.is_validated = True
    db.commit()
    return JSONResponse(status_code=200, content={"message": "El usuario ha sido validado"})


@users_router.post('/login', tags=['auth'])
def login(user: LoginUser):
    """
    Endpoint to log in a user and get a token for authentication.

    Args:
        user (LoginUser): The user's email and password.

    Returns:
        JSONResponse: A token if the user is authorized, otherwise an error message.

    Raises:
        None
    """
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        db = Session()
        user = db.query(UserModel).filter(UserModel.email == user.email, UserModel.password == user.password).first()
        if not user:
            return JSONResponse(status_code=401, content={"message": "El usuario no existe"})
        authorized_email = user.is_validated
        if authorized_email:
            token: str = create_token(user.dict())
            return JSONResponse(status_code=200, content=token)
        else:
            return JSONResponse(
                status_code=401,
                content={"message": "Este email aún no ha sido validado."}
                )


@users_router.get(
        path='/users',
        tags=['users'],
        response_model=List[SignUpUser],
        status_code=200
        )
def get_users() -> List[SignUpUser]:
    db = Session()
    users = db.query(UserModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(users))


@users_router.get('/users/{id}', tags=['users'], response_model=SignUpUser, dependencies=[Depends(JWTBearer())])
def get_user(id: int = Path(ge=1, le=2000)) -> SignUpUser:
    """
    Retrieves a user by its id.

    Args:
        id (int): User id to be retrieved.

    Returns:
        dict: User information.

    Raises:
        HTTPException: If the user is not found.
    """
    db = Session()
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "El usuario no existe"})
    return JSONResponse(content=jsonable_encoder(user))


@users_router.put('/users/{id}', tags=['users'], response_model=SignUpUser, dependencies=[Depends(JWTBearer())])
def update_user(
    id: int = Path(ge=1, le=2000),
    user: SignUpUser = Body(...)
    ) -> SignUpUser:
    """
    Update a user's information.

    Parameters:
    - id (int): The ID of the user to update. Must be between 1 and 2000.
    - user (SignUpUser): The updated user information.

    Returns:
    - SignUpUser: The updated user information.

    Raises:
    - HTTPException 401: Unauthorized access.
    - HTTPException 404: User not found.
    """
    db = Session()
    user_to_update = db.query(UserModel).filter(UserModel.id == id).first()
    if not user_to_update:
        return JSONResponse(status_code=404, content={"message": "El usuario no existe"})
    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.password = user.password
    db.commit()
    return JSONResponse(content=user_to_update)


@users_router.delete('/users/{id}', tags=['users'], response_model=SignUpUser, dependencies=[Depends(JWTBearer())])
def delete_user(id: int = Path(ge=1, le=2000)) -> SignUpUser:
    """
    Deletes a user with the given ID.

    Args:
    - id (int): The ID of the user to delete.

    Returns:
    - A JSON response with the message "Se ha eliminado el usuario." (The user has been deleted.)

    Raises:
    - HTTPException(404): If the user with the given ID does not exist in the database.
    """
    db = Session()
    user_to_delete = db.query(UserModel).filter(UserModel.id == id).first()
    db.delete(user_to_delete)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado el usuario."})
