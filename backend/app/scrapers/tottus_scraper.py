from app.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import time

class TottusScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.tottus.com.pe"
    
    def scrape_category(self, category_url: str) -> List[Dict]:
        """
        Scraping de productos en una categoría de Tottus.
        Esta es una implementación de ejemplo - ajusta según la estructura real del sitio.
        """
        self.setup_driver()
        products = []
        
        try:
            self.driver.get(category_url)
            time.sleep(3)  # Esperar carga
            
            # Ejemplo de selectores - AJUSTAR según la estructura real
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            
            for elem in product_elements:
                try:
                    name = elem.find_element(By.CSS_SELECTOR, ".product-name").text
                    price_text = elem.find_element(By.CSS_SELECTOR, ".price").text
                    price = self._parse_price(price_text)
                    url = elem.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    image_url = elem.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    
                    products.append({
                        'name': name,
                        'brand': self._extract_brand(name),
                        'price': price,
                        'unit': 'unidad',  # Ajustar según necesidad
                        'url': url,
                        'image_url': image_url,
                        'category': 'General'  # Extraer de URL o metadata
                    })
                except Exception as e:
                    print(f"Error procesando producto: {e}")
                    continue
        
        finally:
            self.close_driver()
        
        return products
    
    def search_product(self, query: str) -> List[Dict]:
        """Buscar productos en Tottus"""
        search_url = f"{self.base_url}/search?q={query}"
        return self.scrape_category(search_url)
    
    def _parse_price(self, price_text: str) -> float:
        """Extraer precio numérico de texto"""
        import re
        price_text = price_text.replace('S/', '').replace(',', '.')
        match = re.search(r'[\d.]+', price_text)
        return float(match.group()) if match else 0.0
    
    def _extract_brand(self, name: str) -> str:
        """Extraer marca del nombre (simplificado)"""
        # Primera palabra generalmente es la marca
        return name.split()[0] if name else "Genérico"