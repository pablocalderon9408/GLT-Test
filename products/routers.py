import os

# Typing
from typing import List

# FastAPI
from fastapi import APIRouter
from fastapi import Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Models
from products.models import Product as ProductModel

# Schema
from products.schemas import Product

# Database
from config.database import Session


product_router = APIRouter()


@product_router.get('/products', tags=['products'], response_model=List[Product], status_code=200)
def get_products() -> List[Product]:
    db = Session()
    products = db.query(ProductModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(products))

@product_router.get('/products/{id}', tags=['products'], response_model=Product)
def get_product(id: int = Path(ge=1, le=2000)) -> Product:
    db = Session()
    product = db.query(ProductModel).filter(ProductModel.id == id).first()
    return JSONResponse(content=jsonable_encoder(product))

@product_router.post('/products', tags=['products'], response_model=dict, status_code=201)
def create_product(product: Product) -> dict:
    db = Session()
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el producto"})

@product_router.put('/products/{id}', tags=['products'], response_model=dict, status_code=200)
def update_product(id: int, product: Product)-> dict:
    db = Session()
    product_to_update = db.query(ProductModel).filter(ProductModel.id == id).first()
    product_to_update.name = product.name
    product_to_update.description = product.description
    product_to_update.price = product.price
    product_to_update.stock = product.stock
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el producto"})

@product_router.delete('/products/{id}', tags=['products'], response_model=dict, status_code=200)
def delete_product(id: int)-> dict:
    db = Session()
    product_to_delete = db.query(ProductModel).filter(ProductModel.id == id).first()
    db.delete(product_to_delete)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el producto"})
