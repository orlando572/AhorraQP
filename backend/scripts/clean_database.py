"""
Script para limpiar completamente la base de datos
USAR CON PRECAUCIÓN - Elimina TODOS los datos
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import SessionLocal, engine
from sqlalchemy import text

def clean_database():
    """Eliminar todos los datos de todas las tablas"""
    print("="*70)
    print("⚠️  LIMPIEZA COMPLETA DE LA BASE DE DATOS")
    print("="*70)
    
    # Confirmación
    print("\n🚨 ADVERTENCIA: Esta operación eliminará TODOS los datos.")
    confirm = input("¿Estás seguro? Escribe 'SI' para continuar: ")
    
    if confirm != "SI":
        print("❌ Operación cancelada")
        return
    
    print("\nLimpiando base de datos...")
    
    with engine.connect() as conn:
        try:
            # El orden es importante por las foreign keys
            tables = [
                'store_prices',
                'products',
                'categories',
                'brands',
                'stores',
                'search_queries'
            ]
            
            for table in tables:
                print(f"  → Limpiando tabla: {table}")
                conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
                conn.commit()
            
            print("\n" + "="*70)
            print("✅ BASE DE DATOS LIMPIA")
            print("="*70)
            print("\nTodas las tablas han sido vaciadas.")
            print("Los IDs se han reiniciado desde 1.")
            print("\nAhora puedes ejecutar:")
            print("  python scripts/test_supabase_real.py")
            print("  python scripts/auto_update_prices.py")
            
        except Exception as e:
            print(f"\n❌ Error limpiando base de datos: {e}")
            conn.rollback()

def main():
    clean_database()

if __name__ == "__main__":
    main()