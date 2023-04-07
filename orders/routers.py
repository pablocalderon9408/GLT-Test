# Typing
from typing import List

# FastAPI
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Models
from orders.models import OrderProducts as OrderProductsModel
from orders.models import Order as OrderModel

# Schemas
from orders.schemas import Order, OrderProducts

# Database
from config.database import Session


order_router = APIRouter()

@order_router.get('/orders', tags=['orders'], response_model=List[Order], status_code=200)
def get_orders() -> List[Order]:
    """
    Get all orders.

    Returns:
    --------
    List[Order]
        A list of Order objects containing information about each order in the database.
    """
    db = Session()
    orders = db.query(OrderModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(orders))


@order_router.post('/add-product-to-order', tags=['orders'], response_model=dict, status_code=201)
def add_product_to_order(order: OrderProducts) -> dict:
    db = Session()
    new_order_product = OrderProductsModel(**order.dict())
    db.add(new_order_product)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el producto al pedido"})


@order_router.post('/orders', tags=['orders'], response_model=dict, status_code=201)
def create_order(order: Order) -> dict:
    db = Session()
    new_order = OrderModel(**order.dict())
    db.add(new_order)
    db.commit()
    return JSONResponse(status_code=201, content=jsonable_encoder(new_order))
