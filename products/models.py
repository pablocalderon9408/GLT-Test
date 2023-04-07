from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from utils.utils import BaseModel


class Product(BaseModel):
    """
    Model representing a product.

    Attributes:
    -----------
    id : int
        Primary key of the product.
    name : str
        Name of the product.
    description : str
        Description of the product.
    price : float
        Price of the product.
    stock : int
        Stock quantity of the product.
    orders : List[OrderProducts]
        One-to-many relationship with the OrderProducts model,
        representing the orders associated with the product.
    """

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    stock = Column(Integer, index=True)
    orders = relationship("OrderProducts", back_populates="product")
