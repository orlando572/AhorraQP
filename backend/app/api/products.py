from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.schemas.product import ProductResponse
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/search", response_model=List[ProductResponse])
def search_products(
    q: Optional[str] = Query(None, description="Término de búsqueda"),
    category_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db)
):
    """
    Buscar productos por nombre Y/O categoría.
    Permite buscar solo por texto, solo por categoría o ambos.
    """
    service = ProductService(db)
    
    # Validación: Si no envía NADA, retornamos lista vacía para no traer toda la base de datos
    if not q and not category_id:
        return []
        
    return service.search_products(q, category_id)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener un producto específico con todos sus precios"""
    service = ProductService(db)
    return service.get_product_by_id(product_id)

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Listar productos (paginado)"""
    service = ProductService(db)
    return service.list_products(skip, limit)