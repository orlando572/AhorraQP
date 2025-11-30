from pydantic import BaseModel
from typing import List, Dict, Any
from decimal import Decimal

class CartItem(BaseModel):
    product_id: int
    quantity: int = 1
    store_id: int = None  # Tienda seleccionada (opcional)

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

class SaveCartRequest(BaseModel):
    items: List[dict]  # Lista completa de items con detalles
    totals: dict  # Totales calculados por tienda