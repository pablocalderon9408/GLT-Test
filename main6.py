import os
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from utils.jwt_manager import create_token, validate_token, send_confirmation_email
# from utils.jwt_manager import EmailSchema
from fastapi.security import HTTPBearer
from config.database import engine, Base, Session

from fastapi.encoders import jsonable_encoder
import uvicorn

#En el archivo main.py agregan 
#Deben importar os y uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(os.environ.get("PORT", 8000)))

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@email.com":
            db = Session()
            authorized_email = db.query(UserModel).filter(UserModel.email == data['email'], UserModel.is_validated == True).first()
            if not authorized_email:
                raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class LoginUser(BaseModel):
    email:str
    password:str

class SignUpUser(LoginUser):
    name: str
    password_confirmation: str


class Product(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=5, max_length=15)
    description: str = Field(min_length=15, max_length=50)
    price: float = Field(gte=0)
    stock: int = Field(gte=0)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Mi película",
                "description": "Descripción de la película",
                "price": 2022.99,
                "stock": 10,
            }
        }


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/signup', tags=['auth'])
def signup(user: SignUpUser):
    # Password validation.
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
    token: str = create_token(jsonable_encoder(new_user))
    # Send email.
    email_sent = send_confirmation_email(EmailSchema(email=[user.email]))
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el usuario"})

@app.post('/validate', tags=['auth'])
def validate(token: str):
    # Validate email.
    db = Session()
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return JSONResponse(status_code=404, content={"message": "El usuario no existe"})
    user.is_validated = True
    db.commit()
    return JSONResponse(status_code=200, content={"message": "El usuario ha sido validado"})


@app.post('/login', tags=['auth'])
def login(user: LoginUser):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        db = Session()
        authorized_email = db.query(UserModel).filter(UserModel.email == user.email, UserModel.password == user.password ,UserModel.is_validated == True).first()
        if authorized_email:
            token: str = create_token(user.dict())
            return JSONResponse(status_code=200, content=token)
        else:
            return JSONResponse(status_code=401, content={"message": "Este email aún no ha sido validado."})
        
@app.get('/users', tags=['users'], response_model=List[SignUpUser], status_code=200)
def get_users() -> List[SignUpUser]:
    db = Session()
    users = db.query(UserModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(users))

@app.get('/users/{id}', tags=['users'], response_model=SignUpUser)
def get_user(id: int = Path(ge=1, le=2000)) -> SignUpUser:
    db = Session()
    user = db.query(UserModel).filter(UserModel.id == id).first()
    return JSONResponse(content=jsonable_encoder(user))

@app.put('/users/{id}', tags=['users'], response_model=SignUpUser)
def update_user(id: int = Path(ge=1, le=2000), user: SignUpUser = Body(...)) -> SignUpUser:
    db = Session()
    user_to_update = db.query(UserModel).filter(UserModel.id == id).first()
    user_to_update.name = user.name
    user_to_update.email = user.email
    user_to_update.password = user.password
    db.commit()
    return JSONResponse(content=user_to_update)

@app.delete('/users/{id}', tags=['users'], response_model=SignUpUser)
def delete_user(id: int = Path(ge=1, le=2000)) -> SignUpUser:
    db = Session()
    user_to_delete = db.query(UserModel).filter(UserModel.id == id).first()
    db.delete(user_to_delete)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado el usuario."})


@app.get('/products', tags=['products'], response_model=List[Product], status_code=200)
def get_products() -> List[Product]:
    db = Session()
    products = db.query(ProductModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(products))

@app.get('/products/{id}', tags=['products'], response_model=Product)
def get_product(id: int = Path(ge=1, le=2000)) -> Product:
    db = Session()
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    return JSONResponse(content=jsonable_encoder(product))

@app.post('/products', tags=['products'], response_model=dict, status_code=201)
def create_product(product: Product) -> dict:
    db = Session()
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el producto"})

@app.put('/products/{id}', tags=['products'], response_model=dict, status_code=200)
def update_product(id: int, product: Product)-> dict:
    db = Session()
    product_to_update = db.query(ProductModel).filter(ProductModel.id == id).first()
    product_to_update.name = product.name
    product_to_update.description = product.description
    product_to_update.price = product.price
    product_to_update.stock = product.stock
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el producto"})

@app.delete('/products/{id}', tags=['products'], response_model=dict, status_code=200)
def delete_product(id: int)-> dict:
    db = Session()
    product_to_delete = db.query(ProductModel).filter(ProductModel.id == id).first()
    db.delete(product_to_delete)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el producto"})




from utils.order import OrderProducts as OrderProductsModel

class Order(BaseModel):
    # id: Optional[int] = None
    user_id: int


class OrderProducts(BaseModel):
    order_id: int = Field(gte=1)
    product_id: int = Field(gte=1)
    quantity: int = Field(gte=1)

@app.get('/orders', tags=['orders'], response_model=List[Order], status_code=200)
def get_orders() -> List[Order]:
    db = Session()
    orders = db.query(OrderModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(orders))

@app.post('/add-product-to-order', tags=['orders'], response_model=dict, status_code=201)
def add_product_to_order(order: OrderProducts) -> dict:
    db = Session()
    new_order_product = OrderProductsModel(**order.dict())
    db.add(new_order_product)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el producto al pedido"})


@app.post('/orders', tags=['orders'], response_model=dict, status_code=201)
def create_order(order: Order) -> dict:
    db = Session()
    new_order = OrderModel(**order.dict())
    db.add(new_order)
    db.commit()
    return JSONResponse(status_code=201, content=jsonable_encoder(new_order))
