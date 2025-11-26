from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

class PriceInfo(BaseModel):
    store_id: int
    store_name: str
    price: Decimal
    url: Optional[str]
    is_available: bool
    
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    brand_name: str
    category_name: str
    image_url: Optional[str]
    prices: List[PriceInfo]
    
    class Config:
        from_attributes = True

class ProductSearch(BaseModel):
    query: str
    category_id: Optional[int] = None