from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.database.session import Base


class SearchQuery(Base):
    """
    Modelo para almacenar búsquedas realizadas por usuarios
    Útil para analytics y mejorar el sistema
    """
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<SearchQuery(id={self.id}, created_at={self.created_at})>"