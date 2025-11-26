"""
Script para probar la conexión a Supabase y realizar pruebas básicas
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
            result = conn.execute(text("SELECT 1"))
            print("   ✅ Conexión exitosa a Supabase")
            return True
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def test_tables():
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

def test_insert_sample():
    """Insertar datos de prueba"""
    print("\n3️⃣  Insertando datos de prueba...")
    db = SessionLocal()
    try:
        # Verificar si ya existen datos de prueba
        test_store = db.query(Store).filter(Store.name == "Test Store").first()
        if test_store:
            print("   ℹ️  Datos de prueba ya existen, limpiando...")
            db.delete(test_store)
            db.commit()
        
        # Crear tienda de prueba
        store = Store(name="Test Store", logo_url="https://example.com/logo.png")
        db.add(store)
        db.commit()
        db.refresh(store)
        print(f"   ✅ Tienda creada con ID: {store.id}")
        
        # Crear marca de prueba
        brand = Brand(name="Test Brand")
        db.add(brand)
        db.commit()
        db.refresh(brand)
        print(f"   ✅ Marca creada con ID: {brand.id}")
        
        # Crear categoría de prueba
        category = Category(name="Test Category")
        db.add(category)
        db.commit()
        db.refresh(category)
        print(f"   ✅ Categoría creada con ID: {category.id}")
        
        # Crear producto de prueba
        product = Product(
            name="Producto de Prueba",
            brand_id=brand.id,
            category_id=category.id,
            image_url="https://example.com/product.jpg"
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        print(f"   ✅ Producto creado con ID: {product.id}")
        
        # Crear precio de prueba
        price = StorePrice(
            product_id=product.id,
            store_id=store.id,
            price=19.99,
            url="https://example.com/product",
            is_available=True
        )
        db.add(price)
        db.commit()
        print(f"   ✅ Precio creado correctamente")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error insertando datos: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def test_query_relationships():
    """Probar consultas con relaciones"""
    print("\n4️⃣  Probando consultas con relaciones...")
    db = SessionLocal()
    try:
        # Buscar producto con sus relaciones
        product = db.query(Product).filter(
            Product.name == "Producto de Prueba"
        ).first()
        
        if product:
            print(f"   ✅ Producto: {product.name}")
            print(f"      Marca: {product.brand.name}")
            print(f"      Categoría: {product.category.name}")
            print(f"      Precios en tiendas:")
            for price in product.prices:
                print(f"        → {price.store.name}: S/ {price.price}")
            return True
        else:
            print("   ⚠️  No se encontró el producto de prueba")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en consulta: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

def test_deduplication():
    """Probar que no se crean duplicados"""
    print("\n5️⃣  Probando lógica de deduplicación...")
    db = SessionLocal()
    try:
        # Intentar crear una marca duplicada
        existing_count = db.query(Brand).filter(Brand.name == "Test Brand").count()
        print(f"   📊 Marcas 'Test Brand' antes: {existing_count}")
        
        # Intentar crear duplicado (debe usar el existente)
        brand = db.query(Brand).filter(Brand.name == "Test Brand").first()
        if not brand:
            brand = Brand(name="Test Brand")
            db.add(brand)
            db.commit()
        
        after_count = db.query(Brand).filter(Brand.name == "Test Brand").count()
        print(f"   📊 Marcas 'Test Brand' después: {after_count}")
        
        if after_count == existing_count:
            print("   ✅ No se crearon duplicados")
            return True
        else:
            print("   ⚠️  Se creó un duplicado")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        db.close()

def cleanup_test_data():
    """Limpiar datos de prueba"""
    print("\n6️⃣  Limpiando datos de prueba...")
    db = SessionLocal()
    try:
        # Eliminar en orden (precios -> productos -> marcas/categorías -> tiendas)
        test_store = db.query(Store).filter(Store.name == "Test Store").first()
        if test_store:
            db.delete(test_store)
        
        test_brand = db.query(Brand).filter(Brand.name == "Test Brand").first()
        if test_brand:
            db.delete(test_brand)
        
        test_category = db.query(Category).filter(Category.name == "Test Category").first()
        if test_category:
            db.delete(test_category)
        
        db.commit()
        print("   ✅ Datos de prueba eliminados")
        
    except Exception as e:
        print(f"   ⚠️  Error limpiando: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("="*70)
    print("🧪 PRUEBAS DE CONEXIÓN Y FUNCIONALIDAD - SUPABASE")
    print("="*70)
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Conexión", test_connection()))
    results.append(("Tablas", test_tables()))
    results.append(("Inserción", test_insert_sample()))
    results.append(("Relaciones", test_query_relationships()))
    results.append(("Deduplicación", test_deduplication()))
    
    # Limpiar
    cleanup_test_data()
    
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
        print("\n🎉 ¡Todas las pruebas pasaron! Tu configuración está lista.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    main()