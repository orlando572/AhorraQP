"""
Script para actualizar precios de Tottus en la base de datos
Usa matching inteligente para evitar duplicados con Plaza Vea y Makro
"""

import sys
from pathlib import Path
from datetime import datetime

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import SessionLocal
from app.scrapers.tottus_scraper import TottusScraper
from app.services.tottus_service import TottusDataService
from app.models.store import Store


# URLs de categorías de Tottus
TOTTUS_URLS = [
    # Abarrotes
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16815/Arroz?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16815%7C%7CArroz',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16818/Pasta?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16818%7C%7CPasta',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16820/Especias?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16820%7C%7CEspecias',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16819/Condimentos?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16819%7C%7CCondimentos',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16825/Conservas?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16825%7C%7CConservas',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16817/Aceite?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16817%7C%7CAceite',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16822/Salsas-y-Cremas?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16822%7C%7CSalsas+y+Cremas',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16823/Menestras?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16823%7C%7CMenestras',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16821/Salsas-para-Pasta?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16821%7C%7CSalsas+para+Pasta',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16816/Sal?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16816%7C%7CSal',
    
    # Desayunos/Lácteos
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16808/Azucar-y-endulzantes?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16065%7C%7CDesayunos%2FCATG16808%7C%7CAz%C3%BAcar+y+endulzantes',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16782/Leches?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16065%7C%7CDesayunos%2FCATG16782%7C%7CLeches',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16061/Lacteos',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16784/Quesos',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16777/Huevos-de-Gallina',
    
    # Carnes y Fiambres
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16778/Jamones',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16780/Salchichas-y-Hot-Dogs',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16076/Carnes',
    
    # Frutas y Verduras
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16794/Frutas-y-Verduras-Congeladas',
    'https://www.tottus.com.pe/tottus-pe/lista/CATG16985/Lechugas--Espinacas-y-Hojas',
]


def main():
    print("="*70)
    print(f"🏪 ACTUALIZACIÓN DE TOTTUS - {datetime.now()}")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        # 1. Obtener o crear la tienda Tottus
        print("\n1️⃣ Verificando tienda Tottus...")
        store = db.query(Store).filter(Store.name.ilike('Tottus')).first()
        
        if not store:
            store = Store(name='Tottus')
            db.add(store)
            db.commit()
            db.refresh(store)
            print(f"   ✅ Tienda 'Tottus' creada con ID: {store.id}")
        else:
            print(f"   ✅ Tienda 'Tottus' existente con ID: {store.id}")
        
        # 2. Inicializar servicios
        print("\n2️⃣ Inicializando servicios...")
        scraper = TottusScraper()
        data_service = TottusDataService(db)
        print("   ✅ Scraper y servicio de datos listos")
        
        # 3. Mostrar plan de scraping
        print("\n3️⃣ Plan de scraping:")
        print(f"   Total de URLs: {len(TOTTUS_URLS)}")
        print("\n   Categorías:")
        for i, url in enumerate(TOTTUS_URLS, 1):
            # Extraer nombre de categoría de la URL
            if '/lista/' in url:
                parts = url.split('/lista/')[1].split('?')[0]
                category_name = parts.split('/')[-1] if '/' in parts else parts
                print(f"   {i}. {category_name}")
        
        print("\n" + "="*70)
        print("🚀 INICIANDO SCRAPING Y GUARDADO...")
        print("="*70)
        
        # 4. Procesar cada URL
        total_products = 0
        total_saved = 0
        
        for i, url in enumerate(TOTTUS_URLS, 1):
            try:
                # Extraer nombre de categoría
                category_name = "Desconocida"
                if '/lista/' in url:
                    parts = url.split('/lista/')[1].split('?')[0]
                    category_name = parts.split('/')[-1] if '/' in parts else parts
                
                print(f"\n{'─'*70}")
                print(f"📦 [{i}/{len(TOTTUS_URLS)}] Procesando: {category_name}")
                print(f"{'─'*70}")
                
                # Scrapear categoría
                print(f"   ⏳ Scrapeando productos...")
                products = scraper.scrape_category(url)
                
                if not products:
                    print(f"   ⚠️  No se encontraron productos")
                    continue
                
                print(f"   ✅ {len(products)} productos scrapeados")
                total_products += len(products)
                
                # Guardar en DB con matching inteligente
                print(f"   💾 Guardando en base de datos...")
                saved = data_service.save_tottus_products(products, store.id)
                total_saved += saved
                
                print(f"   ✅ {saved} productos guardados/actualizados")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Proceso interrumpido por el usuario")
                raise
            
            except Exception as e:
                print(f"\n   ❌ Error procesando {category_name}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # 5. Resumen final
        print("\n" + "="*70)
        print("✅ PROCESO COMPLETADO")
        print("="*70)
        
        print(f"\n📊 Resumen:")
        print(f"   • Total scrapeado: {total_products} productos")
        print(f"   • Total guardado/actualizado: {total_saved} productos")
        
        # Estadísticas de la DB
        from app.models import Brand, Category, Product, StorePrice
        from sqlalchemy import func
        
        print(f"\n📈 Estadísticas de la base de datos:")
        
        # Total de productos en Tottus
        tottus_prices = db.query(StorePrice).filter(
            StorePrice.store_id == store.id
        ).count()
        print(f"   • Productos en Tottus: {tottus_prices}")
        
        # Productos en múltiples tiendas
        products_in_multiple = db.query(Product.id).join(StorePrice).group_by(
            Product.id
        ).having(func.count(StorePrice.store_id) > 1).count()
        
        print(f"   • Productos en múltiples tiendas: {products_in_multiple}")
        
        if products_in_multiple > 0:
            total_products_db = db.query(Product).count()
            comparison_rate = (products_in_multiple / total_products_db) * 100
            print(f"   • Tasa de comparación: {comparison_rate:.1f}%")
        
        print("\n" + "="*70)
        print("🎉 ¡Actualización de Tottus completada exitosamente!")
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