from pydantic import BaseModel, Field


class Order(BaseModel):
    # id: Optional[int] = None
    # user_id: int = Field(gte=1)
    pass


class OrderProducts(BaseModel):
    product_id: int = Field(gte=1)
    quantity: int = Field(gte=1)
