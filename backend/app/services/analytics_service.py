from sqlalchemy.orm import Session
from app.models.search_query import SearchQuery
from datetime import datetime
from typing import Dict, Any


class AnalyticsService:
    """
    Servicio para registrar y analizar búsquedas de usuarios
    Útil para entender qué productos buscan más y mejorar el sistema
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_search(self, query: str, results_count: int, filters: Dict[str, Any] = None):
        """
        Registrar una búsqueda realizada
        
        Args:
            query: Término de búsqueda
            results_count: Número de resultados encontrados
            filters: Filtros aplicados (categoría, etc.)
        """
        query_data = {
            "query": query,
            "results_count": results_count,
            "filters": filters or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        search_record = SearchQuery(query_data=query_data)
        self.db.add(search_record)
        self.db.commit()
    
    def log_cart_calculation(self, items_count: int, stores_compared: int):
        """
        Registrar un cálculo de carrito
        """
        query_data = {
            "action": "cart_calculation",
            "items_count": items_count,
            "stores_compared": stores_compared,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        search_record = SearchQuery(query_data=query_data)
        self.db.add(search_record)
        self.db.commit()
    
    def get_popular_searches(self, limit: int = 10) -> list:
        """
        Obtener las búsquedas más populares
        (Requiere procesar el JSONB - implementación básica)
        """
        # Esta es una implementación simple
        # Para producción, considera agregar índices GIN en query_data
        searches = self.db.query(SearchQuery).limit(100).all()
        
        # Procesar y contar
        query_counts = {}
        for search in searches:
            if 'query' in search.query_data:
                q = search.query_data['query']
                query_counts[q] = query_counts.get(q, 0) + 1
        
        # Ordenar por popularidad
        popular = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
        return popular[:limit]