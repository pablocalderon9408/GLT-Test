from config.database import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from models.utils import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_validated = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")
