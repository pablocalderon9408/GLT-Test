from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from utils.utils import BaseModel


class User(BaseModel):
    """
    Model representing a user.

    Attributes:
    -----------
    id : int
        Primary key of the user.
    name : str
        Name of the user.
    email : str
        Email address of the user. Must be unique.
    password : str
        Password of the user.
    is_validated : bool
        Flag indicating whether the user's email has been validated.
    orders : List[Order]
        One-to-many relationship with the Order model, representing
        the orders placed by the user.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_validated = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")
