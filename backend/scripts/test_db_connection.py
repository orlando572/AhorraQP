"""
Script mínimo para probar la conexión a Supabase usando SQLAlchemy.
"""

import sys
from pathlib import Path
from sqlalchemy import text

# Rutas
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.database.session import engine


def test_connection():
    print("🔌 Probando conexión con Supabase...\n")

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]

            print("✅ Conexión exitosa")
            print(f"🛢️  PostgreSQL versión: {version}")
            return True

    except Exception as e:
        print("❌ Error de conexión")
        print(e)
        return False


if __name__ == "__main__":
    ok = test_connection()
    print("\nResultado:", "✔ OK" if ok else "✘ ERROR")
