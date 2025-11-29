from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.cart import CartRequest, CartTotalsResponse
from app.services.product_service import ProductService

router = APIRouter()

@router.post("/calculate", response_model=CartTotalsResponse)
def calculate_cart_totals(cart: CartRequest, db: Session = Depends(get_db)):
    """
    Calcular el total de la lista de compras en cada tienda
    """
    service = ProductService(db)
    return service.calculate_cart_totals(cart.items)