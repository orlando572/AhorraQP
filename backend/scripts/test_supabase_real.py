"""
Script para probar la conexión a Supabase y realizar pruebas REALES
con datos del scraping
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import SessionLocal, engine
from app.models import Store, Brand, Category, Product, StorePrice
from sqlalchemy import text

def test_connection():
    """Probar conexión básica a Supabase"""
    print("\n1️⃣  Probando conexión a Supabase...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   ✅ Conexión exitosa a Supabase")
            print(f"   PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def test_tables_exist():
    """Verificar que las tablas existen"""
    print("\n2️⃣  Verificando tablas...")
    db = SessionLocal()
    try:
        tables = {
            'stores': Store,
            'brands': Brand,
            'categories': Category,
            'products': Product,
            'store_prices': StorePrice
        }
        
        for table_name, model in tables.items():
            count = db.query(model).count()
            print(f"   ✅ {table_name}: {count} registros")
        
        return True
    except Exception as e:
        print(f"   ❌ Error verificando tablas: {e}")
        return False
    finally:
        db.close()

def test_scraping_small_sample():
    """Probar scraping con una muestra pequeña"""
    print("\n3️⃣  Probando scraping con muestra pequeña...")
    print("   (Scrapeará la MISMA categoría en AMBAS tiendas)")
    
    db = SessionLocal()
    try:
        from app.services.scraper_service import ScraperService
        
        service = ScraperService(db)
        
        # Scrapear la MISMA categoría en ambas tiendas
        test_urls = {
            'Plaza Vea': ['https://www.plazavea.com.pe/abarrotes/azucar-y-endulzantes'],
            'Makro': ['https://www.makro.plazavea.com.pe/abarrotes/azucar-y-endulzantes']
        }
        
        print("   → Scrapeando: abarrotes/azucar-y-endulzantes")
        print("   → Tiendas: Plaza Vea y Makro")
        service.update_all_prices(test_urls)
        
        # Verificar resultados
        stores = db.query(Store).count()
        brands = db.query(Brand).count()
        categories = db.query(Category).count()
        products = db.query(Product).count()
        prices = db.query(StorePrice).count()
        
        print(f"\n   📊 Resultados del scraping:")
        print(f"      Tiendas: {stores}")
        print(f"      Marcas: {brands}")
        print(f"      Categorías: {categories}")
        print(f"      Productos: {products}")
        print(f"      Precios: {prices}")
        
        if products > 0 and prices > 0:
            print("   ✅ Scraping exitoso - Datos guardados en Supabase")
            return True
        else:
            print("   ⚠️  No se guardaron productos")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en scraping: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def test_query_products():
    """Probar consultas de productos con relaciones"""
    print("\n4️⃣  Probando consultas de productos...")
    db = SessionLocal()
    try:
        # Obtener 5 productos con sus relaciones
        products = db.query(Product).limit(5).all()
        
        if not products:
            print("   ⚠️  No hay productos en la base de datos")
            return False
        
        print(f"   📦 Mostrando {len(products)} productos:")
        
        for p in products:
            print(f"\n   → {p.name}")
            print(f"      Marca: {p.brand.name}")
            print(f"      Categoría: {p.category.name}")
            print(f"      Precios:")
            for price in p.prices:
                print(f"         • {price.store.name}: S/ {price.price}")
        
        print("\n   ✅ Consultas funcionando correctamente")
        
        # NUEVA SECCIÓN: Mostrar productos en AMBAS tiendas
        print("\n   🔍 Buscando productos disponibles en AMBAS tiendas...")
        
        from sqlalchemy import func
        
        # Productos que tienen precios en más de una tienda
        products_in_multiple_stores = db.query(
            Product.id,
            func.count(StorePrice.store_id).label('store_count')
        ).join(StorePrice).group_by(Product.id).having(
            func.count(StorePrice.store_id) > 1
        ).all()
        
        if products_in_multiple_stores:
            print(f"\n   🎯 {len(products_in_multiple_stores)} productos encontrados en múltiples tiendas:")
            
            for product_id, store_count in products_in_multiple_stores[:5]:  # Mostrar solo 5
                product = db.query(Product).filter(Product.id == product_id).first()
                print(f"\n   📦 {product.name}")
                print(f"      Marca: {product.brand.name}")
                
                # Ordenar precios de menor a mayor
                sorted_prices = sorted(product.prices, key=lambda x: x.price)
                
                for price in sorted_prices:
                    print(f"         • {price.store.name}: S/ {price.price}")
                
                # Calcular diferencia de precio
                if len(sorted_prices) >= 2:
                    cheapest = sorted_prices[0]
                    most_expensive = sorted_prices[-1]
                    difference = most_expensive.price - cheapest.price
                    savings_percent = (difference / most_expensive.price) * 100
                    
                    print(f"      💰 Ahorro: S/ {difference:.2f} ({savings_percent:.1f}%) comprando en {cheapest.store.name}")
        else:
            print("   ℹ️  No hay productos en múltiples tiendas aún")
        
        return True
            
    except Exception as e:
        print(f"   ❌ Error en consulta: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def test_no_duplicates():
    """Verificar que no hay duplicados"""
    print("\n5️⃣  Verificando duplicados...")
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        # Verificar marcas duplicadas
        brands = db.query(Brand.name, func.count(Brand.id)).group_by(Brand.name).having(func.count(Brand.id) > 1).all()
        
        if brands:
            print(f"   ⚠️  Marcas duplicadas encontradas: {len(brands)}")
            for name, count in brands:
                print(f"      - {name}: {count} veces")
        else:
            print("   ✅ No hay marcas duplicadas")
        
        # Verificar categorías duplicadas
        categories = db.query(Category.name, func.count(Category.id)).group_by(Category.name).having(func.count(Category.id) > 1).all()
        
        if categories:
            print(f"   ⚠️  Categorías duplicadas encontradas: {len(categories)}")
            for name, count in categories:
                print(f"      - {name}: {count} veces")
        else:
            print("   ✅ No hay categorías duplicadas")
        
        # Verificar productos duplicados (mismo nombre Y marca)
        duplicates = db.query(
            Product.name, 
            Product.brand_id, 
            func.count(Product.id)
        ).group_by(
            Product.name, 
            Product.brand_id
        ).having(
            func.count(Product.id) > 1
        ).all()
        
        if duplicates:
            print(f"   ⚠️  Productos duplicados encontrados: {len(duplicates)}")
        else:
            print("   ✅ No hay productos duplicados")
        
        return len(brands) == 0 and len(categories) == 0 and len(duplicates) == 0
            
    except Exception as e:
        print(f"   ❌ Error verificando duplicados: {e}")
        return False
    finally:
        db.close()

def show_database_stats():
    """Mostrar estadísticas de la base de datos"""
    print("\n6️⃣  Estadísticas de la base de datos...")
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        # Stats generales
        stores_count = db.query(Store).count()
        brands_count = db.query(Brand).count()
        categories_count = db.query(Category).count()
        products_count = db.query(Product).count()
        prices_count = db.query(StorePrice).count()
        
        print(f"\n   📊 Resumen General:")
        print(f"      • Tiendas: {stores_count}")
        print(f"      • Marcas: {brands_count}")
        print(f"      • Categorías: {categories_count}")
        print(f"      • Productos únicos: {products_count}")
        print(f"      • Precios registrados: {prices_count}")
        
        # Productos por tienda
        print(f"\n   🏪 Productos por tienda:")
        stores = db.query(Store).all()
        for store in stores:
            count = db.query(StorePrice).filter(StorePrice.store_id == store.id).count()
            print(f"      • {store.name}: {count} precios")
        
        # Productos en múltiples tiendas
        products_in_multiple = db.query(Product.id).join(StorePrice).group_by(
            Product.id
        ).having(func.count(StorePrice.store_id) > 1).count()
        
        print(f"\n   🔄 Comparación entre tiendas:")
        print(f"      • Productos en múltiples tiendas: {products_in_multiple}")
        
        if products_in_multiple > 0:
            print(f"      • Productos solo en una tienda: {products_count - products_in_multiple}")
            comparison_rate = (products_in_multiple / products_count) * 100
            print(f"      • Tasa de comparación: {comparison_rate:.1f}%")
        
        # Top marcas
        print(f"\n   🏷️  Top 5 marcas con más productos:")
        top_brands = db.query(
            Brand.name, 
            func.count(Product.id).label('count')
        ).join(Product).group_by(Brand.name).order_by(func.count(Product.id).desc()).limit(5).all()
        
        for brand, count in top_brands:
            print(f"      • {brand}: {count} productos")
        
        # Precio promedio por tienda
        if stores_count > 1:
            print(f"\n   💰 Precio promedio por tienda:")
            for store in stores:
                avg_price = db.query(func.avg(StorePrice.price)).filter(
                    StorePrice.store_id == store.id
                ).scalar()
                if avg_price:
                    print(f"      • {store.name}: S/ {float(avg_price):.2f}")
        
        return True
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        db.close()

def main():
    print("="*70)
    print("🧪 PRUEBAS REALES DE CONEXIÓN Y FUNCIONALIDAD - SUPABASE")
    print("="*70)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Conexión", test_connection()))
    results.append(("Tablas", test_tables_exist()))
    results.append(("Scraping", test_scraping_small_sample()))
    results.append(("Consultas", test_query_products()))
    results.append(("Duplicados", test_no_duplicates()))
    results.append(("Estadísticas", show_database_stats()))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    for test_name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name:20s}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! Tu base de datos está funcionando correctamente.")
        print("\nPuedes ejecutar el script completo:")
        print("   python scripts/auto_update_prices.py")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    main()