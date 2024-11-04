from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    customer_name: str
    total_amount: float
    currency: str

class OrderUpdateStatus(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    currency: str
    status: str
    converted_amount: Optional[float] = None

    class Config:
        from_attributes = True