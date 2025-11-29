from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.database.session import Base


class SearchQuery(Base):
    """
    Modelo para almacenar búsquedas y carritos de usuarios
    query_data puede contener:
    - type: 'search' o 'cart'
    - Para búsquedas: {type: 'search', query: str, results_count: int, filters: {}}
    - Para carritos: {type: 'cart', items: [...], totals: [...], store_prices: {...}}
    """
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchQuery(id={self.id}, type={self.query_data.get('type')}, created_at={self.created_at})>"