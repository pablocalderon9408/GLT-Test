from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config.database import Base
from models.utils import BaseModel
from models.user import User


class Order(BaseModel):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    products = relationship("OrderProducts", back_populates="order")


class OrderProducts(BaseModel):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")