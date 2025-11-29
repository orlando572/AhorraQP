from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from difflib import SequenceMatcher
import unicodedata
import re
from app.models import Product, Brand, Category, StorePrice, Store


class TottusDataService:
    """
    Servicio especializado para guardar datos de Tottus
    con matching inteligente de productos existentes
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Cache de categorías existentes
        self.existing_categories = {
            self.normalize_text(cat.name).lower(): cat 
            for cat in db.query(Category).all()
        }
        
        # Cache de marcas existentes
        self.existing_brands = {
            self.normalize_text(brand.name).lower(): brand 
            for brand in db.query(Brand).all()
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normaliza texto eliminando tildes y caracteres especiales
        """
        if not text:
            return ""
        
        text = str(text).strip()
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        text = ' '.join(text.split())
        
        return text
    
    def similarity_ratio(self, str1: str, str2: str) -> float:
        """
        Calcula la similitud entre dos strings (0.0 a 1.0)
        """
        str1_norm = self.normalize_text(str1).lower()
        str2_norm = self.normalize_text(str2).lower()
        
        return SequenceMatcher(None, str1_norm, str2_norm).ratio()
    
    def find_matching_category(self, category_name: str) -> Optional[Category]:
        """
        Busca la categoría más similar en la base de datos
        """
        if not category_name:
            # Default: Packs Abarrotes
            return self.db.query(Category).filter(Category.name == 'Packs Abarrotes').first()
        
        category_norm = self.normalize_text(category_name).lower()
        
        # Búsqueda exacta primero
        if category_norm in self.existing_categories:
            return self.existing_categories[category_norm]
        
        # Búsqueda fuzzy
        best_match = None
        best_ratio = 0.0
        threshold = 0.7  # 70% de similitud mínima
        
        for existing_cat_name, existing_cat in self.existing_categories.items():
            ratio = self.similarity_ratio(category_name, existing_cat_name)
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = existing_cat
        
        if best_match:
            print(f"      Categoría '{category_name}' → '{best_match.name}' (similitud: {best_ratio:.2f})")
            return best_match
        
        # Si no hay match, usar categoría por defecto
        print(f"      Categoría '{category_name}' → 'Packs Abarrotes' (sin match)")
        return self.db.query(Category).filter(Category.name == 'Packs Abarrotes').first()
    
    def find_matching_brand(self, brand_name: str) -> Brand:
        """
        Busca o crea marca con normalización
        """
        if not brand_name or not brand_name.strip():
            brand_name = 'Generico'
        
        brand_norm = self.normalize_text(brand_name).lower()
        
        # Búsqueda exacta
        if brand_norm in self.existing_brands:
            return self.existing_brands[brand_norm]
        
        # Búsqueda fuzzy para marcas
        best_match = None
        best_ratio = 0.0
        threshold = 0.85  # 85% de similitud para marcas (más estricto)
        
        for existing_brand_name, existing_brand in self.existing_brands.items():
            ratio = self.similarity_ratio(brand_name, existing_brand_name)
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = existing_brand
        
        if best_match:
            print(f"      Marca '{brand_name}' → '{best_match.name}' (similitud: {best_ratio:.2f})")
            return best_match
        
        # Crear nueva marca si no hay match
        print(f"      Marca nueva: '{brand_name}'")
        brand = Brand(name=brand_name)
        self.db.add(brand)
        self.db.flush()
        
        # Actualizar cache
        self.existing_brands[brand_norm] = brand
        
        return brand
    
    def find_matching_product(self, product_name: str, brand: Brand) -> Optional[Product]:
        """
        Busca un producto similar en la base de datos
        Usa nombre + marca para mejor precisión
        """
        product_norm = self.normalize_text(product_name).lower()
        
        # 1. Búsqueda exacta por nombre y marca
        exact_match = self.db.query(Product).filter(
            Product.name == product_name,
            Product.brand_id == brand.id
        ).first()
        
        if exact_match:
            return exact_match
        
        # 2. Búsqueda por nombre normalizado
        all_products = self.db.query(Product).filter(
            Product.brand_id == brand.id
        ).all()
        
        best_match = None
        best_ratio = 0.0
        threshold = 0.85  # 85% de similitud mínima
        
        for existing_product in all_products:
            ratio = self.similarity_ratio(product_name, existing_product.name)
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = existing_product
        
        if best_match:
            print(f"      Producto '{product_name}' → '{best_match.name}' (similitud: {best_ratio:.2f})")
            return best_match
        
        # 3. Búsqueda por palabras clave (para casos como "Arroz Extra" vs "Arroz Extra Faraon")
        # Tokenizar y buscar coincidencias
        product_tokens = set(product_norm.split())
        
        for existing_product in all_products:
            existing_tokens = set(self.normalize_text(existing_product.name).lower().split())
            
            # Calcular intersección de tokens
            common_tokens = product_tokens.intersection(existing_tokens)
            if len(common_tokens) >= 2:  # Al menos 2 palabras en común
                token_ratio = len(common_tokens) / max(len(product_tokens), len(existing_tokens))
                if token_ratio >= 0.6:  # 60% de tokens en común
                    print(f"      Producto '{product_name}' → '{existing_product.name}' (tokens: {token_ratio:.2f})")
                    return existing_product
        
        return None
    
    def save_tottus_products(self, products_data: List[Dict], store_id: int) -> int:
        """
        Guarda productos de Tottus con matching inteligente
        """
        saved_count = 0
        updated_count = 0
        errors_count = 0
        
        print(f"\n🔍 Procesando {len(products_data)} productos de Tottus...")
        
        for i, data in enumerate(products_data, 1):
            try:
                # Validar datos mínimos
                product_name = data.get('name', '').strip()
                price_value = data.get('price', 0.0)
                
                if not product_name or price_value <= 0:
                    continue
                
                if i % 10 == 0:
                    print(f"   Procesando producto {i}/{len(products_data)}...")
                
                # 1. Encontrar o mapear CATEGORÍA
                category = self.find_matching_category(data.get('category', ''))
                
                # 2. Encontrar o crear MARCA
                brand = self.find_matching_brand(data.get('brand', 'Generico'))
                
                # 3. Buscar PRODUCTO EXISTENTE o crear nuevo
                product = self.find_matching_product(product_name, brand)
                
                if not product:
                    # Crear nuevo producto
                    product = Product(
                        name=product_name,
                        brand_id=brand.id,
                        category_id=category.id,
                        image_url=data.get('image_url')
                    )
                    self.db.add(product)
                    self.db.flush()
                    saved_count += 1
                else:
                    # Actualizar imagen si no tiene
                    if data.get('image_url') and not product.image_url:
                        product.image_url = data.get('image_url')
                    updated_count += 1
                
                # 4. Actualizar o crear PRECIO en Tottus
                store_price = self.db.query(StorePrice).filter(
                    StorePrice.product_id == product.id,
                    StorePrice.store_id == store_id
                ).first()
                
                if store_price:
                    # Actualizar precio existente
                    store_price.price = price_value
                    store_price.url = data.get('url')
                    store_price.is_available = True
                else:
                    # Crear nuevo precio
                    store_price = StorePrice(
                        product_id=product.id,
                        store_id=store_id,
                        price=price_value,
                        url=data.get('url'),
                        is_available=True
                    )
                    self.db.add(store_price)
                
                # Commit individual
                try:
                    self.db.commit()
                except Exception as commit_error:
                    self.db.rollback()
                    errors_count += 1
                    print(f"⚠️  Error guardando: {product_name} - {commit_error}")
                    continue
            
            except Exception as e:
                errors_count += 1
                print(f"⚠️  Error procesando: {data.get('name', 'Unknown')} - {e}")
                self.db.rollback()
                continue
        
        print(f"\n✅ Proceso completado:")
        print(f"   • Productos nuevos: {saved_count}")
        print(f"   • Productos actualizados: {updated_count}")
        if errors_count > 0:
            print(f"   ⚠️  Errores: {errors_count}")
        
        return saved_count + updated_count