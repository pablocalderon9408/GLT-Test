# Typing
from typing import List

# FastAPI
from fastapi import APIRouter, Path
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


@order_router.post(
        '/users/{user_id}/orders',
        tags=['orders'],
        status_code=201
        )
def create_order(
    user_id: int = Path(..., gt=0)
) -> dict:
    db = Session()
    new_order = OrderModel(user_id=user_id)
    db.add(new_order)
    db.commit()
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(new_order)
        )


@order_router.get(
        '/users/{user_id}/orders',
        tags=['orders'],
        response_model=List[Order],
        status_code=200
        )
def get_orders(user_id: int) -> List[Order]:
    """
    Get all orders.

    Returns:
    --------
    List[Order]
        A list of Order objects containing information about
        each order in the database.
    """
    db = Session()
    orders = db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(orders)
        )


@order_router.get(
        '/users/{user_id}/orders/{order_id}',
        tags=['orders'],
        response_model=dict,
        status_code=201
        )
def get_order_detail(
    user_id: int,
    order_id: int,
    order: OrderProducts
) -> dict:
    """
    Get order detail.
    """
    db = Session()
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        return JSONResponse(
            status_code=404,
            content={"message": "El pedido no existe"}
            )
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(order)
        )


@order_router.delete(
        '/users/{user_id}/orders/{order_id}',
        tags=['orders'],
        response_model=dict,
        status_code=201
        )
def delete_order(
    user_id: int,
    order_id: int,
    order: OrderProducts
) -> dict:
    """
    Delete an order.
    """
    db = Session()
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not order:
        return JSONResponse(
            status_code=404,
            content={"message": "El pedido no existe"}
            )
    db.delete(order)
    db.commit()

    return JSONResponse(
        status_code=200,
        content={"message": "El pedido ha sido eliminado"}
        )


@order_router.post(
        '/users/{user_id}/orders/{order_id}',
        tags=['orders'],
        response_model=dict,
        status_code=201
        )
def add_product_to_order(
    user_id: int,
    order_id: int,
    order: OrderProducts
) -> dict:
    """
    Add a product to an order.
    """
    db = Session()
    new_order_product = OrderProductsModel(
        order_id=order_id,
        **order.dict()
        )
    db.add(new_order_product)
    db.commit()
    return JSONResponse(
        status_code=201,
        content={"message": "Se ha registrado el producto al pedido"}
        )
