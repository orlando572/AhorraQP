"""
Script para probar el scraper final de Tottus
SIN guardar en la base de datos
"""

import sys
import json
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.scrapers.tottus_scraper import TottusScraper


def test_tottus_scraper():
    """
    Probar el scraper de Tottus con una categoría
    """
    print("="*70)
    print("🧪 PRUEBA FINAL - TOTTUS SCRAPER")
    print("="*70)
    
    # URL de prueba (Arroz)
    url = "https://www.tottus.com.pe/tottus-pe/lista/CATG16815/Arroz?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16815%7C%7CArroz"
    
    print(f"\n📍 URL: {url}")
    print(f"\n⏳ Iniciando scraping (esto puede tardar 1-2 minutos)...\n")
    
    scraper = TottusScraper()
    
    try:
        products = scraper.scrape_category(url)
        
        print("\n" + "="*70)
        print("✅ SCRAPING COMPLETADO")
        print("="*70)
        
        print(f"\n📦 Total de productos encontrados: {len(products)}")
        
        if products:
            # Mostrar primeros 10 productos
            print("\n" + "="*70)
            print("📋 PRIMEROS 10 PRODUCTOS:")
            print("="*70)
            
            for i, product in enumerate(products[:10], 1):
                print(f"\n{i}. {product['name']}")
                print(f"   Marca: {product['brand']}")
                print(f"   Precio: S/ {product['price']}")
                print(f"   Categoría: {product['category']}")
                print(f"   URL: {product['url'][:60]}...")
                if product.get('image_url'):
                    print(f"   Imagen: {product['image_url'][:60]}...")
            
            # Guardar todos los productos en JSON
            filename = "tottus_final_test_products.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(products, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Todos los productos guardados en: {filename}")
            
            # Estadísticas
            print("\n" + "="*70)
            print("📊 ESTADÍSTICAS:")
            print("="*70)
            
            # Contar por marca
            brands = {}
            for p in products:
                brand = p['brand']
                brands[brand] = brands.get(brand, 0) + 1
            
            print(f"\n🏷️  Marcas encontradas: {len(brands)}")
            top_brands = sorted(brands.items(), key=lambda x: x[1], reverse=True)[:5]
            for brand, count in top_brands:
                print(f"   • {brand}: {count} productos")
            
            # Contar por categoría
            categories = {}
            for p in products:
                cat = p['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            print(f"\n📂 Categorías asignadas: {len(categories)}")
            for cat, count in categories.items():
                print(f"   • {cat}: {count} productos")
            
            # Rango de precios
            prices = [p['price'] for p in products]
            print(f"\n💰 Rango de precios:")
            print(f"   • Mínimo: S/ {min(prices):.2f}")
            print(f"   • Máximo: S/ {max(prices):.2f}")
            print(f"   • Promedio: S/ {sum(prices)/len(prices):.2f}")
            
            # Verificar normalización
            print(f"\n🔤 Verificación de normalización:")
            has_tildes = any('á' in p['name'] or 'é' in p['name'] or 'í' in p['name'] 
                           or 'ó' in p['name'] or 'ú' in p['name'] for p in products)
            
            if has_tildes:
                print("   ⚠️  ADVERTENCIA: Algunos productos tienen tildes")
                print("      Esto podría causar problemas de matching")
            else:
                print("   ✅ Todos los textos están normalizados (sin tildes)")
            
            print("\n" + "="*70)
            print("✅ PRUEBA EXITOSA - Listo para guardar en DB")
            print("="*70)
            
            return True
        else:
            print("\n❌ No se encontraron productos")
            return False
    
    except Exception as e:
        print(f"\n❌ Error durante el scraping: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_tottus_scraper()
    
    if success:
        print("\n" + "="*70)
        print("🎯 SIGUIENTE PASO:")
        print("="*70)
        print("\nSi los datos se ven bien, puedes integrar con la DB usando:")
        print("  1. Actualizar ScraperService para incluir TottusScraper")
        print("  2. Usar TottusDataService para guardar con matching inteligente")
        print("\n¿Los datos se ven correctos? (marca, nombre, precio, categoría)")
    else:
        print("\n⚠️  Revisa los errores antes de continuar")