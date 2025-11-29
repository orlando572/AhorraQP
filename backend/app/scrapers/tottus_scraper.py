from app.scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import time
import re
import unicodedata


class TottusScraper(BaseScraper):
    """
    Scraper para Tottus con normalización avanzada de datos
    para compatibilidad con la base de datos existente
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.tottus.com.pe"
    
    def normalize_text(self, text: str) -> str:
        """
        Normaliza texto eliminando tildes, caracteres especiales y espacios extra
        """
        if not text:
            return ""
        
        # Convertir a string y limpiar
        text = str(text).strip()
        
        # Remover tildes y caracteres especiales (NFD = Canonical Decomposition)
        text = unicodedata.normalize('NFD', text)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        
        # Limpiar espacios múltiples
        text = ' '.join(text.split())
        
        return text
    
    def map_category_to_existing(self, raw_category: str, category_id: str = None) -> str:
        """
        Mapea la categoría de Tottus a una de las categorías existentes en la DB
        usando el category_id o palabras clave
        """
        if not raw_category and not category_id:
            return "Packs Abarrotes"
        
        # Normalizar categoría
        category_normalized = self.normalize_text(raw_category).lower() if raw_category else ""
        
        # Mapa de category_id de Tottus a categorías de tu DB
        # Basado en los IDs que vimos: J0101010203, J0101010202
        category_id_mapping = {
            'J0101010203': 'Arroz',  # Arroz Extra
            'J0101010202': 'Arroz',  # Arroz Integral
            'J0101010201': 'Arroz',  # Otros arroces
        }
        
        # Intentar primero con category_id
        if category_id and category_id in category_id_mapping:
            return category_id_mapping[category_id]
        
        # Mapa de palabras clave a categorías existentes
        category_mapping = {
            # Abarrotes
            'arroz': 'Arroz',
            'aceite': 'Aceite',
            'azucar': 'Azúcar y Endulzantes',
            'endulzante': 'Azúcar y Endulzantes',
            'menestra': 'Menestras',
            'frijol': 'Menestras',
            'lenteja': 'Menestras',
            'garbanzo': 'Menestras',
            'fideos': 'Fideos, Pastas y Salsas',
            'pasta': 'Fideos, Pastas y Salsas',
            'salsa': 'Salsas, Cremas y Condimentos',
            'condimento': 'Salsas, Cremas y Condimentos',
            'conserva': 'Conservas',
            
            # Lácteos
            'yogurt': 'Yogurt',
            'yogur': 'Yogurt',
            'leche': 'Leche',
            'huevo': 'Huevos',
            'mantequilla': 'Mantequilla y Margarina',
            'margarina': 'Mantequilla y Margarina',
            'bebe': 'Alimentación del Bebé',
            
            # Carnes
            'res': 'Res',
            'carne': 'Res',
            'pescado': 'Pescados y Mariscos',
            'marisco': 'Pescados y Mariscos',
            'pavo': 'Pavo, Pavita y Otras Aves',
            'pavita': 'Pavo, Pavita y Otras Aves',
            'pollo': 'Pollo',
            'cerdo': 'Cerdo',
            'enrollado': 'Enrollados',
            
            # Quesos y Fiambres
            'queso': 'Quesos Semiduros',
            'jamon': 'Jamonadas y Jamones Cocidos',
            'embutido': 'Embutidos',
            'salchicha': 'Embutidos',
            'salame': 'Salames y Salchichones',
            
            # Bebidas
            'gaseosa': 'Gaseosas',
            'agua': 'Aguas',
            'jugo': 'Jugos y Otras Bebidas',
            'bebida': 'Bebidas Funcionales',
            
            # Frutas y Verduras
            'fruta': 'Frutas',
            'verdura': 'Verduras',
            'vegetal': 'Verduras',
        }
        
        # Buscar coincidencias por palabras clave
        for keyword, mapped_category in category_mapping.items():
            if keyword in category_normalized:
                return mapped_category
        
        # Default basado en el contexto
        return 'Packs Abarrotes'
    
    def scrape_category(self, category_url: str) -> List[Dict]:
        """
        Scrapea una categoría de Tottus con normalización de datos
        """
        self.setup_driver()
        products = []
        page = 1
        
        try:
            while True:
                # Construir URL con paginación
                if page == 1:
                    current_url = category_url
                else:
                    # Tottus usa page=X&store=to_com
                    separator = "&" if "?" in category_url else "?"
                    current_url = f"{category_url}{separator}page={page}&store=to_com"
                
                print(f"--> Scrapeando página {page}: {current_url}")
                
                try:
                    self.driver.get(current_url)
                    time.sleep(3)
                    
                    if page == 1:
                        self._close_cookies_banner()
                        time.sleep(1)
                    
                    # Esperar a que cargue el contenedor de productos
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-pod="catalyst-pod"]'))
                    )
                except Exception as e:
                    print(f"[!] Fin de la paginación o error en página {page}: {e}")
                    break
                
                # Scroll para cargar productos lazy-loaded
                last_count = 0
                same_count_repeats = 0
                
                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
                    elems = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-pod="catalyst-pod"]')
                    current_count = len(elems)
                    
                    if current_count == last_count:
                        same_count_repeats += 1
                    else:
                        same_count_repeats = 0
                    
                    if same_count_repeats >= 2:
                        break
                    
                    last_count = current_count
                
                # Obtener productos
                product_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-pod="catalyst-pod"]')
                
                if not product_elements:
                    print("[!] Página vacía, terminando.")
                    break
                
                print(f"Encontrados {len(product_elements)} items en página {page}")
                
                for item in product_elements:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
                        time.sleep(0.1)
                        
                        # URL del producto (el contenedor es el link)
                        url = item.get_attribute('href')
                        
                        # Marca
                        try:
                            brand_elem = item.find_element(By.CSS_SELECTOR, 'b[class*="title1"][class*="secondary"]')
                            raw_brand = brand_elem.text.strip()
                            brand = self.normalize_text(raw_brand)
                        except:
                            brand = "Generico"
                        
                        # Nombre/Descripción
                        try:
                            name_elem = item.find_element(By.CSS_SELECTOR, 'b[id*="displaySubTitle"]')
                            raw_name = name_elem.text.strip()
                            name = self.normalize_text(raw_name)
                        except:
                            # Fallback: usar el alt de la imagen
                            try:
                                img_elem = item.find_element(By.CSS_SELECTOR, 'img[alt]')
                                alt_text = img_elem.get_attribute('alt')
                                if alt_text and ' - ' in alt_text:
                                    parts = alt_text.split(' - ', 1)
                                    name = self.normalize_text(parts[1])
                                else:
                                    name = self.normalize_text(alt_text)
                            except:
                                continue
                        
                        # Precio
                        try:
                            price_elem = item.find_element(By.CSS_SELECTOR, 'li[data-internet-price]')
                            price_value = price_elem.get_attribute('data-internet-price')
                            price = float(price_value) if price_value else 0.0
                        except:
                            price = 0.0
                        
                        # Imagen
                        img_url = None
                        try:
                            img_element = item.find_element(By.CSS_SELECTOR, 'picture img')
                            img_url = img_element.get_attribute('src')
                            
                            if not img_url or "data:image" in img_url:
                                img_url = img_element.get_attribute('data-src')
                            if not img_url or "data:image" in img_url:
                                srcset = img_element.get_attribute('srcset')
                                if srcset:
                                    img_url = srcset.split(',')[0].split()[0]
                            
                            if img_url and "http" in img_url:
                                img_url = img_url.strip()
                        except:
                            pass
                        
                        # Category ID de Tottus
                        category_id = None
                        try:
                            category_id = item.get_attribute('data-category')
                        except:
                            pass
                        
                        # Extraer categoría de la URL como fallback
                        raw_category = self._extract_category_from_url(category_url)
                        
                        # Mapear a categoría existente
                        category = self.map_category_to_existing(raw_category, category_id)
                        
                        # Validar datos mínimos
                        if not name or price <= 0:
                            continue
                        
                        # Crear nombre completo
                        full_name = f"{brand} {name}"
                        
                        products.append({
                            "name": full_name,
                            "brand": brand if brand else "Generico",
                            "price": price,
                            "url": url,
                            "image_url": img_url,
                            "category": category
                        })
                    
                    except Exception as e:
                        continue
                
                page += 1
        
        finally:
            self.close_driver()
        
        return products
    
    def _extract_category_from_url(self, url: str) -> str:
        """
        Extrae la categoría de la URL
        Ej: /tottus-pe/lista/CATG16815/Arroz -> "Arroz"
        """
        if not url:
            return "General"
        
        # Buscar el nombre después del último /
        parts = url.split('/')
        
        # Buscar el patrón: /CATGXXXXX/NombreCategoria
        for i, part in enumerate(parts):
            if part.startswith('CATG') and i + 1 < len(parts):
                category_name = parts[i + 1]
                # Limpiar parámetros de query
                if '?' in category_name:
                    category_name = category_name.split('?')[0]
                return category_name.replace('-', ' ').title()
        
        return "General"
    
    def search_product(self, query: str) -> List[Dict]:
        """
        Buscar productos por nombre o URL de categoría
        """
        # Si es una URL completa, usarla directamente
        if query.startswith('http'):
            return self.scrape_category(query)
        else:
            return self.scrape_category(f"{self.base_url}/{query}")
    
    def _close_cookies_banner(self):
        """
        Cerrar banner de cookies
        """
        try:
            time.sleep(1)
            
            selectors = [
                "button#onetrust-accept-btn-handler",
                "button[class*='accept']",
                "button[class*='cookie']",
                ".cookie-banner button",
                "[class*='cookie'] button",
                "button[aria-label*='accept']",
                "button[aria-label*='aceptar']"
            ]
            
            for selector in selectors:
                try:
                    btn = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if btn:
                        self.driver.execute_script("arguments[0].click();", btn[0])
                        return
                except:
                    continue
        except:
            pass