from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=15, max_length=50)
    price: float = Field(gte=0)
    stock: int = Field(gte=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Mi película",
                "description": "Descripción de la película",
                "price": 2022.99,
                "stock": 10,
            }
        }
