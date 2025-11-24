from sqlalchemy.orm import Session
from typing import List, Dict
from app.scrapers.tottus_scraper import TottusScraper
from app.scrapers.plaza_vea_scraper import PlazaVeaScraper
from app.models.product import Product, Brand, Category, StorePrice
from app.models.store import Store

class ScraperService:
    def __init__(self, db: Session):
        self.db = db
        self.scrapers = {
            'Tottus': TottusScraper(),
            'Plaza Vea': PlazaVeaScraper()
        }
    
    def update_all_prices(self, category_urls: Dict[str, List[str]]):
        """
        Actualizar precios de todas las tiendas por categorías.
        
        category_urls = {
            'Tottus': ['url1', 'url2'],
            'Plaza Vea': ['url1', 'url2']
        }
        """
        for store_name, urls in category_urls.items():
            print(f"Actualizando {store_name}...")
            scraper = self.scrapers.get(store_name)
            if not scraper:
                continue
            
            store = self.db.query(Store).filter(Store.name == store_name).first()
            if not store:
                store = Store(name=store_name)
                self.db.add(store)
                self.db.commit()
            
            for url in urls:
                try:
                    products_data = scraper.scrape_category(url)
                    self._save_products(products_data, store.id)
                except Exception as e:
                    print(f"Error en {url}: {e}")
    
    def _save_products(self, products_data: List[Dict], store_id: int):
        """Guardar productos y precios en la base de datos"""
        for data in products_data:
            # Obtener o crear marca
            brand = self.db.query(Brand).filter(Brand.name == data['brand']).first()
            if not brand:
                brand = Brand(name=data['brand'])
                self.db.add(brand)
                self.db.flush()
            
            # Obtener o crear categoría
            category = self.db.query(Category).filter(Category.name == data['category']).first()
            if not category:
                category = Category(name=data['category'])
                self.db.add(category)
                self.db.flush()
            
            # Buscar producto existente
            product = self.db.query(Product).filter(
                Product.name == data['name'],
                Product.brand_id == brand.id
            ).first()
            
            if not product:
                product = Product(
                    name=data['name'],
                    brand_id=brand.id,
                    category_id=category.id,
                    image_url=data.get('image_url')
                )
                self.db.add(product)
                self.db.flush()
            
            # Actualizar o crear precio
            price = self.db.query(StorePrice).filter(
                StorePrice.product_id == product.id,
                StorePrice.store_id == store_id
            ).first()
            
            if price:
                price.price = data['price']
                price.unit = data['unit']
                price.url = data['url']
                price.is_available = True
            else:
                price = StorePrice(
                    product_id=product.id,
                    store_id=store_id,
                    price=data['price'],
                    unit=data['unit'],
                    url=data['url'],
                    is_available=True
                )
                self.db.add(price)
        
        self.db.commit()
        print(f"✓ Guardados {len(products_data)} productos")