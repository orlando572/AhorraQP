from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.cart import CartRequest, CartTotalsResponse, SaveCartRequest
from app.services.product_service import ProductService
from app.models.search_query import SearchQuery
from datetime import datetime

router = APIRouter()

@router.post("/calculate", response_model=CartTotalsResponse)
def calculate_cart_totals(cart: CartRequest, db: Session = Depends(get_db)):
    """
    Calcular el total de la lista de compras en cada tienda
    """
    service = ProductService(db)
    return service.calculate_cart_totals(cart.items)

@router.post("/save")
def save_cart(cart: SaveCartRequest, db: Session = Depends(get_db)):
    """
    Guardar el carrito en la base de datos
    """
    cart_data = {
        "type": "cart",
        "items": cart.items,
        "totals": cart.totals,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    search_record = SearchQuery(query_data=cart_data)
    db.add(search_record)
    db.commit()
    db.refresh(search_record)
    
    return {
        "id": search_record.id,
        "message": "Carrito guardado exitosamente",
        "created_at": search_record.created_at
    }