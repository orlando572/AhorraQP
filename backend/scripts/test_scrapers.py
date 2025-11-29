"""
Script para probar los scrapers manualmente
Útil para desarrollo y debugging
"""

import sys
import csv
import os  # Import necesario para verificar si el archivo existe
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.scrapers.plaza_vea_scraper import PlazaVeaScraper
from app.scrapers.makro_scraper import MakroScraper

# Nombre del archivo donde se guardarán los datos
NOMBRE_ARCHIVO_CSV = "resultados_productos_pruebas.csv"

def guardar_en_csv(products, store_name):
    """
    Guarda la lista de productos en un archivo CSV.
    Si el archivo no existe, crea los encabezados.
    Si existe, agrega los datos al final (append).
    """
    columnas = ['tienda', 'nombre', 'marca', 'precio', 'stock', 'categoria', 'url', 'imagen']
    
    # Verificamos si el archivo existe para saber si escribir encabezados
    archivo_existe = os.path.isfile(NOMBRE_ARCHIVO_CSV)
    
    try:
        # mode='a' significa 'append' (agregar al final)
        with open(NOMBRE_ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            
            # Escribir encabezado solo si es archivo nuevo
            if not archivo_existe:
                writer.writeheader()
            
            for p in products:
                writer.writerow({
                    'tienda': store_name,
                    'nombre': p.get('name', 'N/A'),
                    'marca': p.get('brand', 'N/A'),
                    'precio': p.get('price', 0.0),
                    'categoria': p.get('category', 'N/A'),
                    'url': p.get('url', ''),
                    'imagen': p.get('image_url', '')
                })
        print(f"   >>> [ÉXITO] Se guardaron {len(products)} productos en '{NOMBRE_ARCHIVO_CSV}'")
    except Exception as e:
        print(f"   >>> [ERROR] No se pudo guardar en CSV: {e}")

def ejecutar_busqueda(query, scraper_class, store_name):
    """Función auxiliar para ejecutar la búsqueda e imprimir resultados"""
    scraper = scraper_class()
    
    print(f"\n--------------------------------------------------")
    print(f"Buscando: '{query}' en {store_name}...")
    
    try:
        products = scraper.search_product(query)
        total = len(products)
        print(f"Encontrados {total} productos")

        if not products:
            print("No se encontraron productos.")
            return

        # --- AQUÍ GUARDAMOS EN CSV ---
        guardar_en_csv(products, store_name)
        # -----------------------------

        print(f"\n=== RESULTADOS DE '{query.upper()}' EN {store_name.upper()} (Total: {total}) ===")

        for i, product in enumerate(products, 1):
            print(f"\n================ PRODUCTO #{i} ================")
            print(f"Nombre   : {product.get('name')}")
            print(f"Marca    : {product.get('brand')}")
            print(f"Precio   : S/ {product.get('price')}")
            print(f"Categoría: {product.get('category')}")
            print(f"URL      : {product.get('url')}")
            print(f"Imagen   : {product.get('image_url')}")
            print("===============================================")
            
    except Exception as e:
        print(f"Error durante la búsqueda: {e}")


def main():
    while True:
        print("\n" + "="*50)
        print("=== MENU PRINCIPAL ===")
        print(f"Nota: Los datos se guardan en: {NOMBRE_ARCHIVO_CSV}")
        print("Selecciona el supermercado:")
        print("1. Plaza Vea")
        print("2. Makro")
        print("3. Salir")
        
        store_opcion = input("\nElige tienda (1-3): ")

        if store_opcion == "3":
            print("¡Hasta luego!")
            break

        if store_opcion == "1":
            scraper_class = PlazaVeaScraper
            store_name = "Plaza Vea"
        elif store_opcion == "2":
            scraper_class = MakroScraper
            store_name = "Makro"
        else:
            print("Opción no válida.")
            continue

        # Sub-menú de productos
        while True:
            print(f"\n--- Buscando en {store_name} ---")
            print("1. Arroz (Categoría: abarrotes/arroz)")
            print("2. Aceites (Categoría: abarrotes/aceite)")
            print("3. Menestras (Categoría: abarrotes/menestras)")
            print("4. Búsqueda Personalizada (Escribir nombre o URL)")
            print("5. Volver al menú principal") 
            
            prod_opcion = input("\nElige opción (1-5): ")
            
            if prod_opcion == "1":
                ejecutar_busqueda("abarrotes/arroz", scraper_class, store_name)
            elif prod_opcion == "2":
                ejecutar_busqueda("abarrotes/aceite", scraper_class, store_name)
            elif prod_opcion == "3":
                ejecutar_busqueda("abarrotes/menestras", scraper_class, store_name)
            elif prod_opcion == "4":
                custom_query = input("--> Escribe lo que quieres buscar (ej. leche, fideos): ")
                if custom_query.strip():
                    ejecutar_busqueda(custom_query, scraper_class, store_name)
            elif prod_opcion == "5":
                break 
            else:
                print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()