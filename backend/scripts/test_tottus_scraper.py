"""
Script para probar y ajustar el scraper de Tottus
Inspecciona la estructura HTML y extrae productos de prueba
"""

import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def setup_driver():
    """Configurar driver de Selenium"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comentado para ver el navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    
    return driver


def inspect_page_structure(driver):
    """Inspeccionar la estructura de la página para encontrar selectores"""
    print("\n" + "="*70)
    print("🔍 INSPECCIONANDO ESTRUCTURA DE LA PÁGINA")
    print("="*70)
    
    # Esperar un momento para que cargue completamente
    time.sleep(5)
    
    # Basado en el código fuente de Tottus que vimos:
    # Los productos están en: <a href="..." data-pod="catalyst-pod" role="button">
    # Contenedor principal: div[pod-layout="4_GRID"] > a[data-pod="catalyst-pod"]
    
    tottus_selectors = [
        'a[data-pod="catalyst-pod"]',  # Selector específico de Tottus
        'div[pod-layout*="GRID"] > a',  # Contenedor grid
        'a[role="button"][data-pod]',   # Links de productos
    ]
    
    print("\n1️⃣ Buscando contenedores de productos...")
    found_containers = []
    
    # Primero probar selectores específicos de Tottus
    for selector in tottus_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements and len(elements) > 3:  # Al menos 3 elementos
                print(f"   ✅ Encontrado: {selector} ({len(elements)} elementos)")
                found_containers.append((selector, len(elements)))
        except:
            pass
    
    # Si no funcionan, probar selectores genéricos
    if not found_containers:
        generic_selectors = [
            "div[class*='product']",
            "article[class*='product']",
            "div[class*='pod']",
            "a[class*='pod-link']",
        ]
        
        for selector in generic_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and len(elements) > 3:
                    print(f"   ✅ Encontrado: {selector} ({len(elements)} elementos)")
                    found_containers.append((selector, len(elements)))
            except:
                pass
    
    if not found_containers:
        print("   ❌ No se encontraron contenedores obvios")
        print("\n   Inspeccionando HTML manualmente...")
        
        # Guardar HTML para inspección manual
        with open("tottus_page_debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("   💾 HTML guardado en: tottus_page_debug.html")
        
        return None
    
    # Usar el contenedor con más elementos
    best_selector = max(found_containers, key=lambda x: x[1])[0]
    print(f"\n   🎯 Mejor selector: {best_selector}")
    
    return best_selector


def analyze_product_elements(driver, container_selector):
    """Analizar la estructura de los elementos de productos"""
    print("\n2️⃣ Analizando estructura de productos...")
    
    try:
        products = driver.find_elements(By.CSS_SELECTOR, container_selector)
        
        if not products:
            print("   ❌ No se encontraron productos")
            return None
        
        print(f"   Analizando primer producto de {len(products)} encontrados...")
        first_product = products[0]
        
        # Scroll al elemento
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_product)
        time.sleep(1)
        
        # Obtener HTML interno
        inner_html = first_product.get_attribute('innerHTML')
        
        print("\n   📝 HTML del primer producto (primeros 800 caracteres):")
        print("   " + "-"*66)
        print(f"   {inner_html[:800]}...")
        print("   " + "-"*66)
        
        # Selectores específicos basados en el código fuente de Tottus
        selectors_to_test = {
            'nombre': [
                # El nombre completo está en el subtitle
                'b[id*="displaySubTitle"]',
                '.pod-subTitle',
                'b[class*="subTitle"]',
                # Fallback: usar el alt de la imagen
                'img[alt]',
            ],
            'precio': [
                # Basado en: <li data-internet-price="4.49">
                # y <span>S/ 4.49</span>
                'li[data-internet-price]',
                'span[class*="copy10"]',
                '.prices-0 span',
                '[data-internet-price]',
            ],
            'marca': [
                # La marca aparece en: <b class="...title1...">PACASMAYO</b>
                'b[class*="title1"][class*="secondary"]',
                'b.title1.secondary',
                'b[class*="title1"]',
                '.pod-title b',
            ],
            'imagen': [
                # <img src="https://media.tottus.com.pe/tottusPE/..." alt="...">
                'picture img',
                'img[src*="media.tottus"]',
                'img[alt]',
                'img',
            ],
            'enlace': [
                # Ya está en el contenedor: <a href="...">
                # Pero necesitamos extraer el href
                'self',  # El propio elemento es el link
            ]
        }
        
        found_selectors = {}
        
        for element_type, selectors in selectors_to_test.items():
            print(f"\n   🔍 Buscando {element_type}...")
            
            if element_type == 'enlace':
                # El contenedor mismo es el link
                try:
                    href = first_product.get_attribute('href')
                    if href:
                        print(f"      ✅ Link del contenedor: {href[:50]}...")
                        found_selectors[element_type] = 'self'
                except:
                    pass
                continue
            
            for selector in selectors:
                try:
                    if element_type == 'precio' and selector == 'li[data-internet-price]':
                        # Caso especial: el precio está en un atributo
                        elem = first_product.find_element(By.CSS_SELECTOR, selector)
                        price = elem.get_attribute('data-internet-price')
                        if price:
                            print(f"      ✅ {selector}: S/ {price}")
                            found_selectors[element_type] = selector
                            break
                    elif element_type == 'nombre' and selector == 'img[alt]':
                        # Caso especial: el nombre puede estar en el alt de la imagen
                        elem = first_product.find_element(By.CSS_SELECTOR, selector)
                        alt_text = elem.get_attribute('alt')
                        if alt_text and ' - ' in alt_text:
                            # Extraer solo la parte después del " - "
                            text = alt_text.split(' - ', 1)[1]
                            print(f"      ✅ {selector} (alt): {text[:50]}...")
                            found_selectors[element_type] = selector
                            break
                    else:
                        elem = first_product.find_element(By.CSS_SELECTOR, selector)
                        if elem:
                            if element_type == 'imagen':
                                text = elem.get_attribute('src') or elem.get_attribute('data-src')
                            else:
                                text = elem.text.strip()
                            
                            if text:
                                print(f"      ✅ {selector}: {text[:50]}...")
                                if element_type not in found_selectors:
                                    found_selectors[element_type] = selector
                                break
                except:
                    continue
        
        return found_selectors
    
    except Exception as e:
        print(f"   ❌ Error analizando productos: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_test_products(driver, container_selector, element_selectors, limit=5):
    """Extraer productos de prueba usando los selectores encontrados"""
    print(f"\n3️⃣ Extrayendo {limit} productos de prueba...")
    
    products = []
    
    try:
        product_elements = driver.find_elements(By.CSS_SELECTOR, container_selector)
        
        for i, item in enumerate(product_elements[:limit]):
            print(f"\n   Producto #{i+1}:")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", item)
            time.sleep(0.5)
            
            product = {}
            
            # URL (el contenedor es el link)
            try:
                if element_selectors.get('enlace') == 'self':
                    product['url'] = item.get_attribute('href')
                    print(f"      URL: {product['url'][:60]}...")
            except Exception as e:
                print(f"      ⚠️  Error URL: {e}")
            
            # Marca (título principal)
            if 'marca' in element_selectors:
                try:
                    brand_elem = item.find_element(By.CSS_SELECTOR, element_selectors['marca'])
                    product['brand'] = brand_elem.text.strip()
                    print(f"      Marca: {product['brand']}")
                except Exception as e:
                    print(f"      ⚠️  Error Marca: {e}")
            
            # Nombre/Descripción (subtítulo o del alt de la imagen)
            if 'nombre' in element_selectors:
                try:
                    selector = element_selectors['nombre']
                    
                    # Si el selector es para el alt de la imagen
                    if selector == 'img[alt]':
                        img_elem = item.find_element(By.CSS_SELECTOR, selector)
                        alt_text = img_elem.get_attribute('alt')
                        
                        # El alt viene como "MARCA - Descripción completa"
                        # Ej: "FARAON - Arroz Faraón Extra Bolsa 5 Kg"
                        if alt_text and ' - ' in alt_text:
                            parts = alt_text.split(' - ', 1)
                            product['name'] = parts[1].strip()  # Tomar solo la descripción
                        else:
                            product['name'] = alt_text.strip()
                    else:
                        name_elem = item.find_element(By.CSS_SELECTOR, selector)
                        product['name'] = name_elem.text.strip()
                    
                    print(f"      Nombre: {product['name']}")
                except Exception as e:
                    print(f"      ⚠️  Error Nombre: {e}")
                    
                    # Fallback: intentar obtener del alt de la imagen
                    try:
                        img_elem = item.find_element(By.CSS_SELECTOR, 'img[alt]')
                        alt_text = img_elem.get_attribute('alt')
                        if alt_text and ' - ' in alt_text:
                            parts = alt_text.split(' - ', 1)
                            product['name'] = parts[1].strip()
                            print(f"      Nombre (del alt): {product['name']}")
                    except:
                        pass
            
            # Combinar marca + nombre si tenemos ambos
            if 'brand' in product and 'name' in product:
                product['full_name'] = f"{product['brand']} {product['name']}"
                print(f"      Nombre Completo: {product['full_name']}")
            
            # Precio
            if 'precio' in element_selectors:
                try:
                    price_selector = element_selectors['precio']
                    
                    # Si el precio está en un atributo data-internet-price
                    if 'data-internet-price' in price_selector:
                        price_elem = item.find_element(By.CSS_SELECTOR, price_selector)
                        price_value = price_elem.get_attribute('data-internet-price')
                        product['price'] = price_value
                        print(f"      Precio: S/ {product['price']}")
                    else:
                        price_elem = item.find_element(By.CSS_SELECTOR, price_selector)
                        product['price'] = price_elem.text.strip()
                        print(f"      Precio: {product['price']}")
                except Exception as e:
                    print(f"      ⚠️  Error Precio: {e}")
            
            # Imagen
            if 'imagen' in element_selectors:
                try:
                    img_elem = item.find_element(By.CSS_SELECTOR, element_selectors['imagen'])
                    img_src = img_elem.get_attribute('src')
                    if not img_src or 'data:image' in img_src:
                        img_src = img_elem.get_attribute('data-src')
                    if not img_src or 'data:image' in img_src:
                        img_src = img_elem.get_attribute('srcset')
                        if img_src:
                            # Tomar la primera URL del srcset
                            img_src = img_src.split(',')[0].split()[0]
                    
                    product['image_url'] = img_src
                    print(f"      Imagen: {product['image_url'][:60] if img_src else 'No encontrada'}...")
                except Exception as e:
                    print(f"      ⚠️  Error Imagen: {e}")
            
            # Extraer datos del atributo data-key (tiene info útil)
            try:
                data_key = item.get_attribute('data-key')
                if data_key:
                    product['data_key'] = data_key
                    print(f"      Data-key: {data_key}")
            except:
                pass
            
            # Extraer categoría del atributo data-category
            try:
                data_category = item.get_attribute('data-category')
                if data_category:
                    product['category_id'] = data_category
                    print(f"      Category ID: {data_category}")
            except:
                pass
            
            if product:
                products.append(product)
    
    except Exception as e:
        print(f"   ❌ Error extrayendo productos: {e}")
        import traceback
        traceback.print_exc()
    
    return products


def test_pagination(driver):
    """Probar la paginación"""
    print("\n4️⃣ Probando paginación...")
    
    try:
        # Buscar elementos de paginación
        pagination_selectors = [
            'a[href*="page=2"]',
            'button[aria-label*="siguiente"]',
            '.pagination a',
            '[class*="pagination"] a',
            'a[class*="next"]'
        ]
        
        for selector in pagination_selectors:
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, selector)
                if next_page:
                    print(f"   ✅ Paginación encontrada: {selector}")
                    print(f"      URL: {next_page.get_attribute('href')}")
                    return True
            except:
                continue
        
        print("   ⚠️ No se encontró paginación obvia")
        
        # Verificar si la URL actual tiene parámetro page
        current_url = driver.current_url
        if 'page=' in current_url:
            print("   ℹ️ La URL parece soportar paginación por parámetro 'page='")
            return True
        
        return False
    
    except Exception as e:
        print(f"   ❌ Error probando paginación: {e}")
        return False


def close_cookies_banner(driver):
    """Cerrar banner de cookies"""
    print("\n🍪 Intentando cerrar banner de cookies...")
    
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
            btn = driver.find_element(By.CSS_SELECTOR, selector)
            if btn:
                driver.execute_script("arguments[0].click();", btn)
                print(f"   ✅ Banner cerrado con: {selector}")
                time.sleep(1)
                return True
        except:
            continue
    
    print("   ℹ️ No se encontró banner de cookies (puede que no exista)")
    return False


def main():
    print("="*70)
    print("🧪 PRUEBAS DE SCRAPER TOTTUS - INSPECCIÓN Y EXTRACCIÓN")
    print("="*70)
    
    url = "https://www.tottus.com.pe/tottus-pe/lista/CATG16815/Arroz?f.product.L2_category_paths=CATG16049%7C%7C1P+TOTTUS%2FCATG16066%7C%7CAbarrotes%2FCATG16815%7C%7CArroz"
    
    print(f"\n📍 URL de prueba: {url}")
    
    driver = setup_driver()
    
    try:
        print("\n⏳ Cargando página...")
        driver.get(url)
        
        # Cerrar cookies
        close_cookies_banner(driver)
        
        # Esperar a que cargue
        print("⏳ Esperando carga completa...")
        time.sleep(5)
        
        # Scroll para lazy loading
        print("📜 Haciendo scroll...")
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        # 1. Inspeccionar estructura
        container_selector = inspect_page_structure(driver)
        
        if not container_selector:
            print("\n❌ No se pudo identificar la estructura automáticamente")
            print("   Por favor, revisa el archivo tottus_page_debug.html")
            return
        
        # 2. Analizar elementos
        element_selectors = analyze_product_elements(driver, container_selector)
        
        if not element_selectors:
            print("\n❌ No se pudieron identificar los selectores de elementos")
            return
        
        # 3. Extraer productos de prueba
        test_products = extract_test_products(driver, container_selector, element_selectors)
        
        # 4. Probar paginación
        test_pagination(driver)
        
        # Resumen
        print("\n" + "="*70)
        print("📊 RESUMEN DE SELECTORES ENCONTRADOS")
        print("="*70)
        
        print(f"\n✅ Contenedor de productos: {container_selector}")
        
        if element_selectors:
            print("\n✅ Selectores de elementos:")
            for key, selector in element_selectors.items():
                print(f"   {key:15s}: {selector}")
        
        if test_products:
            print(f"\n✅ Productos extraídos: {len(test_products)}")
            
            # Guardar productos de prueba
            with open("tottus_test_products.json", "w", encoding="utf-8") as f:
                json.dump(test_products, f, ensure_ascii=False, indent=2)
            print("   💾 Guardados en: tottus_test_products.json")
        
        print("\n" + "="*70)
        print("✅ PRUEBAS COMPLETADAS")
        print("="*70)
        
        input("\n⏸️  Presiona ENTER para cerrar el navegador...")
    
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        
        input("\n⏸️  Presiona ENTER para cerrar...")
    
    finally:
        driver.quit()


if __name__ == "__main__":
    main()