"""
Script para actualizar precios automáticamente de Plaza Vea y Makro
Usa las categorías definidas en categorias_tiendas.txt
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import SessionLocal
from app.services.scraper_service import ScraperService
from datetime import datetime

# CATEGORÍAS A SCRAPEAR (basadas en categorias_tiendas.txt)
CATEGORIAS = [
    'abarrotes/arroz',
    'abarrotes/aceite',
    'abarrotes/azucar-y-endulzantes',
    'abarrotes/menestras',
    'lacteos-y-huevos',
    'carnes-aves-y-pescados',
    'quesos-y-fiambres',
    'bebidas',
    'frutas-y-verduras',
    'abarrotes/salsas-cremas-y-condimentos',
    'abarrotes/fideos-pastas-y-salsas',
    'abarrotes/conservas',
]


# URLs BASE
BASE_URLS = {
    'Plaza Vea': 'https://www.plazavea.com.pe',
    'Makro': 'https://www.makro.plazavea.com.pe'
}

def main():
    print("="*70)
    print(f"ACTUALIZACIÓN AUTOMÁTICA DE PRECIOS - {datetime.now()}")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        service = ScraperService(db)
        
        # Construir URLs completas para cada tienda
        category_urls = {
            store_name: [f"{base_url}/{cat}" for cat in CATEGORIAS]
            for store_name, base_url in BASE_URLS.items()
        }
        
        # Mostrar plan de scraping
        print("\n📋 Plan de scraping:")
        for store, urls in category_urls.items():
            print(f"\n{store}:")
            for url in urls:
                print(f"  → {url}")
        
        print("\n" + "="*70)
        print("INICIANDO SCRAPING...")
        print("="*70)
        
        # Ejecutar actualización
        service.update_all_prices(category_urls)
        
        print("\n" + "="*70)
        print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrumpido por el usuario")
        db.rollback()
    except Exception as e:
        print(f"\n\n❌ Error durante la actualización: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()