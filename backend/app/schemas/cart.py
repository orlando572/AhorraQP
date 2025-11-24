from pydantic import BaseModel
from typing import List
from decimal import Decimal

class CartItem(BaseModel):
    product_id: int
    quantity: int = 1

class CartRequest(BaseModel):
    items: List[CartItem]

class StoreTotalResponse(BaseModel):
    store_id: int
    store_name: str
    total: Decimal
    items_available: int
    items_unavailable: int

class CartTotalsResponse(BaseModel):
    totals: List[StoreTotalResponse]