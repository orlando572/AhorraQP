from sqlalchemy.orm import Session
from typing import List, Dict
from app.scrapers.plaza_vea_scraper import PlazaVeaScraper
from app.scrapers.makro_scraper import MakroScraper
from app.models import Product, Brand, Category, StorePrice
from app.models.store import Store

class ScraperService:
    def __init__(self, db: Session):
        self.db = db
        self.scrapers = {
            'Plaza Vea': PlazaVeaScraper(),
            'Makro': MakroScraper()
        }
    
    def update_all_prices(self, category_urls: Dict[str, List[str]]):
        """
        Actualizar precios de todas las tiendas por categorías.
        
        category_urls = {
            'Plaza Vea': ['abarrotes/arroz', 'abarrotes/aceite'],
            'Makro': ['abarrotes/arroz', 'abarrotes/aceite']
        }
        """
        for store_name, urls in category_urls.items():
            print(f"\n{'='*60}")
            print(f"Actualizando {store_name}...")
            print(f"{'='*60}")
            
            scraper = self.scrapers.get(store_name)
            if not scraper:
                print(f"⚠️  Scraper no encontrado para {store_name}")
                continue
            
            # Obtener o crear la tienda
            store = self._get_or_create_store(store_name)
            print(f"✓ Usando tienda '{store_name}' con ID: {store.id}")
            
            for url in urls:
                try:
                    print(f"\n→ Procesando: {url}")
                    products_data = scraper.scrape_category(url)
                    
                    if products_data:
                        saved = self._save_products(products_data, store.id)
                        print(f"✓ {saved} productos guardados/actualizados")
                    else:
                        print("⚠️  No se encontraron productos")
                        
                except Exception as e:
                    print(f"❌ Error en {url}: {e}")
                    import traceback
                    traceback.print_exc()
    
    def _get_or_create_store(self, store_name: str) -> Store:
        """
        Obtener tienda existente o crear una nueva
        Evita duplicados por nombre
        """
        # Buscar tienda existente (case-insensitive)
        store = self.db.query(Store).filter(
            Store.name.ilike(store_name)
        ).first()
        
        if not store:
            store = Store(name=store_name)
            self.db.add(store)
            self.db.commit()
            self.db.refresh(store)
            print(f"  → Tienda '{store_name}' creada")
        
        return store
    
    def _get_or_create_brand(self, brand_name: str) -> Brand:
        """
        Obtener marca existente o crear una nueva
        Evita duplicados
        """
        if not brand_name or not brand_name.strip():
            brand_name = 'Genérico'
        
        brand_name = brand_name.strip()
        
        # Buscar marca existente (case-insensitive)
        brand = self.db.query(Brand).filter(
            Brand.name.ilike(brand_name)
        ).first()
        
        if not brand:
            brand = Brand(name=brand_name)
            self.db.add(brand)
            self.db.flush()  # Flush para obtener el ID sin commit
        
        return brand
    
    def _get_or_create_category(self, category_name: str) -> Category:
        """
        Obtener categoría existente o crear una nueva
        Evita duplicados
        """
        if not category_name or not category_name.strip():
            category_name = 'General'
        
        category_name = category_name.strip()
        
        # Buscar categoría existente (case-insensitive)
        category = self.db.query(Category).filter(
            Category.name.ilike(category_name)
        ).first()
        
        if not category:
            category = Category(name=category_name)
            self.db.add(category)
            self.db.flush()
        
        return category
    
    def _get_or_create_product(self, product_name: str, brand: Brand, category: Category, image_url: str = None) -> Product:
        """
        Obtener producto existente o crear uno nuevo
        Busca por nombre exacto Y marca para evitar duplicados
        """
        if not product_name or not product_name.strip():
            return None
        
        product_name = product_name.strip()
        
        # Buscar producto existente por nombre Y marca
        product = self.db.query(Product).filter(
            Product.name == product_name,
            Product.brand_id == brand.id
        ).first()
        
        if not product:
            # Crear nuevo producto
            product = Product(
                name=product_name,
                brand_id=brand.id,
                category_id=category.id,
                image_url=image_url
            )
            self.db.add(product)
            self.db.flush()
        else:
            # Actualizar imagen si no tiene o si cambió
            if image_url and not product.image_url:
                product.image_url = image_url
        
        return product
    
    def _save_products(self, products_data: List[Dict], store_id: int) -> int:
        """
        Guardar productos y precios en la base de datos
        CON LÓGICA DE DEDUPLICACIÓN MEJORADA
        """
        saved_count = 0
        errors_count = 0
        
        for data in products_data:
            try:
                # Validar datos mínimos
                product_name = data.get('name', '').strip()
                price_value = data.get('price', 0.0)
                
                if not product_name:
                    continue
                
                if price_value <= 0:
                    continue
                
                # 1. Obtener o crear MARCA
                brand = self._get_or_create_brand(data.get('brand', 'Genérico'))
                
                # 2. Obtener o crear CATEGORÍA
                category = self._get_or_create_category(data.get('category', 'General'))
                
                # 3. Obtener o crear PRODUCTO
                product = self._get_or_create_product(
                    product_name=product_name,
                    brand=brand,
                    category=category,
                    image_url=data.get('image_url')
                )
                
                if not product:
                    continue
                
                # 4. Actualizar o crear PRECIO en esta tienda
                # IMPORTANTE: Un producto tiene UN SOLO precio por tienda
                store_price = self.db.query(StorePrice).filter(
                    StorePrice.product_id == product.id,
                    StorePrice.store_id == store_id
                ).first()
                
                if store_price:
                    # ACTUALIZAR precio existente
                    store_price.price = price_value
                    store_price.url = data.get('url')
                    store_price.is_available = True
                else:
                    # CREAR nuevo precio
                    store_price = StorePrice(
                        product_id=product.id,
                        store_id=store_id,
                        price=price_value,
                        url=data.get('url'),
                        is_available=True
                    )
                    self.db.add(store_price)
                
                # Commit individual para evitar problemas de batch
                try:
                    self.db.commit()
                    saved_count += 1
                except Exception as commit_error:
                    # Si falla el commit (ej: duplicado), hacer rollback y continuar
                    self.db.rollback()
                    errors_count += 1
                    print(f"⚠️  Error guardando producto: {product_name}")
                    print(f"   Error: {commit_error}")
                    continue
                
            except Exception as e:
                errors_count += 1
                print(f"⚠️  Error procesando producto: {data.get('name', 'Unknown')}")
                print(f"   Error: {e}")
                # Hacer rollback en caso de error
                self.db.rollback()
                continue
        
        if errors_count > 0:
            print(f"   ⚠️  {errors_count} productos con errores (omitidos)")
        
        return saved_count
    
    def mark_unavailable_products(self, store_id: int, available_product_ids: List[int]):
        """
        Marcar como no disponibles los productos que no están en la lista
        Útil después de un scraping completo
        """
        try:
            # Marcar como no disponibles todos los productos que NO están en la lista
            self.db.query(StorePrice).filter(
                StorePrice.store_id == store_id,
                ~StorePrice.product_id.in_(available_product_ids)
            ).update({
                'is_available': False
            }, synchronize_session=False)
            
            self.db.commit()
            print(f"✓ Productos no encontrados marcados como no disponibles")
        except Exception as e:
            print(f"⚠️  Error marcando productos no disponibles: {e}")
            self.db.rollback()