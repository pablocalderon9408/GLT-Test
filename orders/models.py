from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utils.utils import BaseModel


class Order(BaseModel):
    """
    Model representing an order placed by a user.

    Attributes:
    -----------
    id : int
        Primary key of the order.
    user_id : int
        Foreign key referencing the id of the user who placed the order.
    user : User
        Many-to-one relationship with the User model, representing the user who placed the order.
    products : List[OrderProducts]
        One-to-many relationship with the OrderProducts model, representing the products associated with the order.
    """

    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")
    products = relationship("OrderProducts", back_populates="order")


class OrderProducts(BaseModel):
    """
    Model representing the products associated with an order.

    Attributes:
    -----------
    id : int
        Primary key of the order product.
    order_id : int
        Foreign key referencing the id of the order associated with the product.
    product_id : int
        Foreign key referencing the id of the product associated with the order.
    quantity : int
        Quantity of the product associated with the order.
    product : Product
        Many-to-one relationship with the Product model, representing the product associated with the order.
    order : Order
        Many-to-one relationship with the Order model, representing the order associated with the product.
    """

    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")
