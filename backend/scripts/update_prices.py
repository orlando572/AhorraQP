"""
Script para actualizar precios periódicamente.
Ejecutar con cron job o scheduler.

Ejemplo cron (cada día a las 3 AM):
0 3 * * * cd /path/to/project && python scripts/update_prices.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import SessionLocal
from app.services.scraper_service import ScraperService

def main():
    print("=== Iniciando actualización de precios ===")
    db = SessionLocal()
    
    try:
        service = ScraperService(db)
        
        # Definir URLs de categorías a scrapear
        category_urls = {
            'Tottus': [
                'https://www.tottus.com.pe/abarrotes',
                'https://www.tottus.com.pe/lacteos',
                'https://www.tottus.com.pe/bebidas',
                # Agregar más categorías
            ],
            'Plaza Vea': [
                'https://www.plazavea.com.pe/abarrotes',
                'https://www.plazavea.com.pe/lacteos',
                'https://www.plazavea.com.pe/bebidas',
                # Agregar más categorías
            ]
        }
        
        service.update_all_prices(category_urls)
        print("=== Actualización completada ===")
        
    except Exception as e:
        print(f"❌ Error en actualización: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()