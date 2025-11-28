"""
Script para actualizar precios automáticamente de Plaza Vea y Makro
Las URLs son casi idénticas para ambas tiendas
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
# Las URLs son las mismas para Plaza Vea y Makro
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
]

# URLs BASE - Ambas tiendas usan la misma estructura
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
        # Como ambas tiendas usan las mismas rutas, simplemente agregamos la base
        category_urls = {
            store_name: [f"{base_url}/{cat}" for cat in CATEGORIAS]
            for store_name, base_url in BASE_URLS.items()
        }
        
        # Mostrar plan de scraping
        print("\n📋 Plan de scraping:")
        total_urls = 0
        for store, urls in category_urls.items():
            print(f"\n{store}:")
            for url in urls:
                print(f"  → {url}")
                total_urls += 1
        
        print(f"\nTotal: {total_urls} URLs a procesar")
        print("Nota: Las URLs son idénticas para ambas tiendas, solo cambia el dominio")
        
        print("\n" + "="*70)
        print("INICIANDO SCRAPING...")
        print("="*70)
        
        # Ejecutar actualización
        service.update_all_prices(category_urls)
        
        print("\n" + "="*70)
        print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        
        # Mostrar resumen de datos en la DB
        print("\n📊 Resumen de la base de datos:")
        from app.models import Store, Brand, Category, Product, StorePrice
        
        stores_count = db.query(Store).count()
        brands_count = db.query(Brand).count()
        categories_count = db.query(Category).count()
        products_count = db.query(Product).count()
        prices_count = db.query(StorePrice).count()
        
        print(f"  • Tiendas: {stores_count}")
        print(f"  • Marcas: {brands_count}")
        print(f"  • Categorías: {categories_count}")
        print(f"  • Productos: {products_count}")
        print(f"  • Precios registrados: {prices_count}")
        
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