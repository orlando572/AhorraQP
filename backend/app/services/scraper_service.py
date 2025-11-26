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
            store = self.db.query(Store).filter(Store.name == store_name).first()
            if not store:
                store = Store(name=store_name)
                self.db.add(store)
                self.db.commit()
                self.db.refresh(store)
                print(f"✓ Tienda '{store_name}' creada con ID: {store.id}")
            
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
    
    def _save_products(self, products_data: List[Dict], store_id: int) -> int:
        """
        Guardar productos y precios en la base de datos
        CON LÓGICA DE DEDUPLICACIÓN
        """
        saved_count = 0
        
        for data in products_data:
            try:
                # 1. OBTENER O CREAR MARCA
                brand_name = data.get('brand', 'Genérico').strip()
                if not brand_name:
                    brand_name = 'Genérico'
                    
                brand = self.db.query(Brand).filter(
                    Brand.name.ilike(brand_name)
                ).first()
                
                if not brand:
                    brand = Brand(name=brand_name)
                    self.db.add(brand)
                    self.db.flush()
                
                # 2. OBTENER O CREAR CATEGORÍA
                category_name = data.get('category', 'General').strip()
                if not category_name:
                    category_name = 'General'
                    
                category = self.db.query(Category).filter(
                    Category.name.ilike(category_name)
                ).first()
                
                if not category:
                    category = Category(name=category_name)
                    self.db.add(category)
                    self.db.flush()
                
                # 3. BUSCAR PRODUCTO EXISTENTE
                # Importante: buscar por nombre exacto Y marca para evitar duplicados
                product_name = data.get('name', '').strip()
                if not product_name:
                    continue  # Saltar si no hay nombre
                
                product = self.db.query(Product).filter(
                    Product.name == product_name,
                    Product.brand_id == brand.id
                ).first()
                
                # 4. CREAR PRODUCTO SI NO EXISTE
                if not product:
                    product = Product(
                        name=product_name,
                        brand_id=brand.id,
                        category_id=category.id,
                        image_url=data.get('image_url')
                    )
                    self.db.add(product)
                    self.db.flush()
                else:
                    # Actualizar imagen si no tiene o si cambió
                    if data.get('image_url') and not product.image_url:
                        product.image_url = data.get('image_url')
                
                # 5. ACTUALIZAR O CREAR PRECIO EN ESTA TIENDA
                # IMPORTANTE: Un producto puede tener UN SOLO precio por tienda
                price_value = data.get('price', 0.0)
                if price_value <= 0:
                    continue  # Saltar precios inválidos
                
                # Buscar precio existente para este producto en esta tienda
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
                
                saved_count += 1
                
            except Exception as e:
                print(f"⚠️  Error procesando producto: {data.get('name', 'Unknown')}")
                print(f"   Error: {e}")
                continue
        
        # Commit al final de todo el lote
        try:
            self.db.commit()
        except Exception as e:
            print(f"❌ Error al hacer commit: {e}")
            self.db.rollback()
            raise
        
        return saved_count
    
    def mark_unavailable_products(self, store_id: int):
        """
        Marcar como no disponibles los productos que no se encontraron
        en el último scraping
        """
        # Esta función se puede ejecutar después del scraping
        # para marcar productos que ya no están disponibles
        pass