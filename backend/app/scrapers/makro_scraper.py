from app.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from typing import List, Dict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class MakroScraper(BaseScraper):

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.makro.plazavea.com.pe"
    
    def scrape_category(self, category_url: str) -> List[Dict]:
        self.setup_driver()
        products = []
        page = 1

        try:
            while True:
                if page == 1:
                    current_url = category_url
                else:
                    separator = "&" if "?" in category_url else "?"
                    current_url = f"{category_url}{separator}page={page}"
                
                print(f"--> Scrapeando página {page}: {current_url}")

                try:
                    self.driver.get(current_url)
                    time.sleep(3)

                    if page == 1:
                        self._close_cookies_banner()
                        time.sleep(1)

                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.showcase-grid"))
                    )
                except Exception:
                    print(f"[!] Fin de la paginación o no se encontraron más resultados en página {page}.")
                    break

                last_count = 0
                same_count_repeats = 0

                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)

                    elems = self.driver.find_elements(By.CSS_SELECTOR, "div.ga-product-item")
                    current_count = len(elems)

                    if current_count == last_count:
                        same_count_repeats += 1
                    else:
                        same_count_repeats = 0

                    if same_count_repeats >= 2:
                        break

                    last_count = current_count

                product_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.ga-product-item")

                if not product_elements:
                    print("[!] Página vacía, terminando.")
                    break
                
                print(f"Encontrados {len(product_elements)} items en página {page}")

                for item in product_elements:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                        time.sleep(0.1)

                        name = item.get_attribute("data-ga-name")
                        price = item.get_attribute("data-ga-price")
                        brand = item.get_attribute("data-ga-brand")
                        raw_category = item.get_attribute("data-ga-category") 

                        if raw_category:
                            parts = raw_category.split('/') # Cortamos por cada '/'
                            if len(parts) > 1:
                                # Tomamos el segundo elemento (índice 1), que sería "Arroz"
                                category = parts[1].strip() 
                            else:
                                # Si no hay '/', tomamos todo el texto (ej. "Arroz")
                                category = parts[0].strip() 
                        else:
                            category = "Sin categoría"

                        try:
                            # Selector específico de Makro para el enlace (tiene clase -mk también a veces)
                            # Pero el selector genérico por href suele funcionar mejor
                            link = item.find_element(By.CSS_SELECTOR, "a[href*='/p']")
                            url = link.get_attribute("href")
                        except:
                            url = None

                        # ==========================================
                        # CORRECCIÓN DE IMAGEN PARA MAKRO
                        # ==========================================
                        img_url = None
                        try:
                            # INTENTO 1: Selector específico de Makro (Showcase-mk__photo)
                            img_element = item.find_element(By.CSS_SELECTOR, "figure.Showcase-mk__photo img")
                            
                            candidato = img_element.get_attribute("src")
                            if not candidato or "data:image" in candidato:
                                candidato = img_element.get_attribute("data-src")
                            if not candidato or "data:image" in candidato:
                                candidato = self.driver.execute_script("return arguments[0].currentSrc;", img_element)
                            
                            if candidato and "http" in candidato and "data:image" not in candidato:
                                img_url = candidato
                        except:
                            # INTENTO 2: Fallback a la clase de la imagen directa (Showcase-mk__image)
                            try:
                                img_element = item.find_element(By.CSS_SELECTOR, ".Showcase-mk__image")
                                img_url = img_element.get_attribute("src")
                            except:
                                img_url = None

                        if img_url:
                            img_url = img_url.strip()

                        products.append({
                            "name": name,
                            "brand": brand,
                            "price": float(price) if price else 0.0,
                            "url": url,
                            "image_url": img_url,
                            "category": category
                        })

                    except:
                        continue
                
                page += 1

        finally:
            self.close_driver()

        return products

    def search_product(self, query: str) -> List[Dict]:
        return self.scrape_category(f"{self.base_url}/{query}")

    def _close_cookies_banner(self):
        try:
            time.sleep(1)
            btn = self.driver.find_elements(By.CSS_SELECTOR, "button#onetrust-accept-btn-handler")
            if btn:
                self.driver.execute_script("arguments[0].click();", btn[0])
                return
            
            # Banner antiguo
            banner = self.driver.find_elements(By.ID, "cookie-consent-banner")
            if banner:
                btn = banner[0].find_element(By.CSS_SELECTOR, ".CookieConsentBanner__button")
                self.driver.execute_script("arguments[0].click();", btn)
                return
        except:
            pass