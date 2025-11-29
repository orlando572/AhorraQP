from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database.session import get_db
from app.models.category import Category

router = APIRouter()

class CategoryResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Listar todas las categorías disponibles"""
    categories = db.query(Category).order_by(Category.name).all()
    return categories