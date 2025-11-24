from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database.session import get_db
from app.models.store import Store

router = APIRouter()

class StoreResponse(BaseModel):
    id: int
    name: str
    logo_url: str | None
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[StoreResponse])
def list_stores(db: Session = Depends(get_db)):
    """Listar todas las tiendas disponibles"""
    stores = db.query(Store).all()
    return stores