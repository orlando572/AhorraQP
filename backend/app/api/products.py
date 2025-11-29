from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.schemas.product import ProductResponse, ProductSearch
from app.services.product_service import ProductService

router = APIRouter()

@router.get("/search", response_model=List[ProductResponse])
def search_products(
    q: str = Query(..., min_length=2, description="Término de búsqueda"),
    category_id: int = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db)
):
    """Buscar productos por nombre"""
    service = ProductService(db)
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