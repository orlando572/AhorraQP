"""
Script para probar los scrapers manualmente
Útil para desarrollo y debugging
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.scrapers.tottus_scraper import TottusScraper
from app.scrapers.plaza_vea_scraper import PlazaVeaScraper


def test_tottus():
    """Probar scraper de Tottus"""
    print("\n=== Probando Tottus Scraper ===")
    scraper = TottusScraper()
    
    try:
        # Buscar productos
        print("Buscando 'leche'...")
        products = scraper.search_product("leche")
        
        print(f"✓ Encontrados {len(products)} productos")
        
        # Mostrar primeros 3
        for i, product in enumerate(products[:3], 1):
            print(f"\n{i}. {product['name']}")
            print(f"   Marca: {product['brand']}")
            print(f"   Precio: S/ {product['price']}")
            print(f"   URL: {product['url'][:50]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def test_plaza_vea():
    """Probar scraper de Plaza Vea"""
    print("\n=== Probando Plaza Vea Scraper ===")
    scraper = PlazaVeaScraper()
    
    try:
        print("Buscando 'arroz'...")
        products = scraper.search_product("arroz")
        
        print(f"✓ Encontrados {len(products)} productos")
        
        # Mostrar primeros 3
        for i, product in enumerate(products[:3], 1):
            print(f"\n{i}. {product['name']}")
            print(f"   Marca: {product['brand']}")
            print(f"   Precio: S/ {product['price']}")
            print(f"   URL: {product['url'][:50]}...")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("=== Test de Scrapers ===")
    print("NOTA: Los selectores CSS necesitan ser ajustados según la estructura real de cada sitio")
    
    choice = input("\n¿Qué scraper deseas probar?\n1. Tottus\n2. Plaza Vea\n3. Ambos\nOpción: ")
    
    if choice == "1":
        test_tottus()
    elif choice == "2":
        test_plaza_vea()
    elif choice == "3":
        test_tottus()
        test_plaza_vea()
    else:
        print("Opción inválida")


if __name__ == "__main__":
    main()