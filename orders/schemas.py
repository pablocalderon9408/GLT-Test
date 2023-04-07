from pydantic import BaseModel, Field

class Order(BaseModel):
    # id: Optional[int] = None
    user_id: int = Field(gte=1)


class OrderProducts(BaseModel):
    order_id: int = Field(gte=1)
    product_id: int = Field(gte=1)
    quantity: int = Field(gte=1)
