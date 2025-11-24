"""
Script para inicializar la base de datos
Crea las tablas y datos iniciales
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import engine, Base, SessionLocal
from app.models.store import Store
from app.models.product import Brand, Category


def create_tables():
    """Crear todas las tablas"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas")


def seed_initial_data():
    """Insertar datos iniciales"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        if db.query(Store).count() > 0:
            print("La base de datos ya tiene datos iniciales")
            return
        
        print("Insertando datos iniciales...")
        
        # Tiendas
        stores = [
            Store(name="Tottus", logo_url="https://example.com/tottus-logo.png"),
            Store(name="Plaza Vea", logo_url="https://example.com/plazavea-logo.png"),
            Store(name="Metro", logo_url="https://example.com/metro-logo.png"),
        ]
        db.add_all(stores)
        
        # Categorías comunes
        categories = [
            Category(name="Abarrotes"),
            Category(name="Lácteos"),
            Category(name="Bebidas"),
            Category(name="Carnes"),
            Category(name="Frutas y Verduras"),
            Category(name="Limpieza"),
            Category(name="Cuidado Personal"),
            Category(name="Panadería"),
            Category(name="Congelados"),
            Category(name="General"),
        ]
        db.add_all(categories)
        
        # Marcas comunes (ejemplos)
        brands = [
            Brand(name="Gloria"),
            Brand(name="Laive"),
            Brand(name="Donofrio"),
            Brand(name="San Fernando"),
            Brand(name="Inca Kola"),
            Brand(name="Coca Cola"),
            Brand(name="Sapolio"),
            Brand(name="Opal"),
            Brand(name="Genérico"),
        ]
        db.add_all(brands)
        
        db.commit()
        print("✓ Datos iniciales insertados")
        print(f"  - {len(stores)} tiendas")
        print(f"  - {len(categories)} categorías")
        print(f"  - {len(brands)} marcas")
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    print("=== Inicialización de Base de Datos ===")
    
    try:
        create_tables()
        seed_initial_data()
        print("=== Inicialización completada ===")
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()