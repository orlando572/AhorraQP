from app.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from typing import List, Dict
import time

class PlazaVeaScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.plazavea.com.pe"
    
    def scrape_category(self, category_url: str) -> List[Dict]:
        """Scraping de Plaza Vea - Ajustar selectores según estructura real"""
        self.setup_driver()
        products = []
        
        try:
            self.driver.get(category_url)
            time.sleep(3)
            
            # Ajustar selectores según la estructura real de Plaza Vea
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-card")
            
            for elem in product_elements:
                try:
                    name = elem.find_element(By.CSS_SELECTOR, ".product-title").text
                    price_text = elem.find_element(By.CSS_SELECTOR, ".price-value").text
                    price = self._parse_price(price_text)
                    url = elem.find_element(By.TAG_NAME, "a").get_attribute("href")
                    image_url = elem.find_element(By.TAG_NAME, "img").get_attribute("src")
                    
                    products.append({
                        'name': name,
                        'brand': self._extract_brand(name),
                        'price': price,
                        'unit': 'unidad',
                        'url': url,
                        'image_url': image_url,
                        'category': 'General'
                    })
                except Exception as e:
                    print(f"Error procesando producto: {e}")
                    continue
        
        finally:
            self.close_driver()
        
        return products
    
    def search_product(self, query: str) -> List[Dict]:
        """Buscar productos en Plaza Vea"""
        search_url = f"{self.base_url}/search?q={query}"
        return self.scrape_category(search_url)
    
    def _parse_price(self, price_text: str) -> float:
        """Extraer precio numérico"""
        import re
        price_text = price_text.replace('S/', '').replace(',', '.')
        match = re.search(r'[\d.]+', price_text)
        return float(match.group()) if match else 0.0
    
    def _extract_brand(self, name: str) -> str:
        """Extraer marca del nombre"""
        return name.split()[0] if name else "Genérico"