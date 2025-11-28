"""
Script para agregar índices a la base de datos de Supabase
Ejecutar UNA SOLA VEZ después de crear las tablas
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import engine
from sqlalchemy import text

def create_indexes():
    """Crear índices para mejor rendimiento"""
    print("="*70)
    print("CREANDO ÍNDICES EN LA BASE DE DATOS")
    print("="*70)
    
    indexes = [
        # Índice para buscar productos por nombre y marca (evita duplicados)
        """
        CREATE INDEX IF NOT EXISTS idx_product_name_brand 
        ON products(name, brand_id);
        """,
        
        # Índice único para asegurar UN precio por producto por tienda
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_product_store_unique 
        ON store_prices(product_id, store_id);
        """,
        
        # Índice para búsquedas case-insensitive en marcas
        """
        CREATE INDEX IF NOT EXISTS idx_brand_name_lower 
        ON brands(LOWER(name));
        """,
        
        # Índice para búsquedas case-insensitive en categorías
        """
        CREATE INDEX IF NOT EXISTS idx_category_name_lower 
        ON categories(LOWER(name));
        """,
        
        # Índice para filtrar productos disponibles
        """
        CREATE INDEX IF NOT EXISTS idx_store_prices_available 
        ON store_prices(is_available);
        """
    ]
    
    with engine.connect() as conn:
        for i, sql in enumerate(indexes, 1):
            try:
                print(f"\n{i}. Creando índice...")
                conn.execute(text(sql))
                conn.commit()
                print("   ✅ Índice creado exitosamente")
            except Exception as e:
                print(f"   ⚠️  Error o índice ya existe: {e}")
    
    print("\n" + "="*70)
    print("✅ PROCESO COMPLETADO")
    print("="*70)
    print("\nLos índices ayudarán a:")
    print("  • Evitar productos duplicados")
    print("  • Asegurar un solo precio por producto por tienda")
    print("  • Acelerar búsquedas por nombre, marca y categoría")
    print("  • Mejorar el rendimiento general de la base de datos")

def main():
    try:
        create_indexes()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()