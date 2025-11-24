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
    
    
