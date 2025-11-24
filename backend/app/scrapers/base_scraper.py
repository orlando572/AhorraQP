from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Dict
from app.config import settings

class BaseScraper(ABC):
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """Configurar Selenium WebDriver"""
        chrome_options = Options()
        if settings.HEADLESS_BROWSER:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(settings.SCRAPER_TIMEOUT)
    
    def close_driver(self):
        """Cerrar el driver"""
        if self.driver:
            self.driver.quit()
    
    @abstractmethod
    def scrape_category(self, category_url: str) -> List[Dict]:
        """
        Scraping por categoría.
        Debe retornar una lista de diccionarios con:
        {
            'name': str,
            'brand': str,
            'price': float,
            'unit': str,
            'url': str,
            'image_url': str,
            'category': str
        }
        """
        pass
    
    @abstractmethod
    def search_product(self, query: str) -> List[Dict]:
        """
        Buscar productos por nombre.
        Mismo formato de retorno que scrape_category.
        """
        pass