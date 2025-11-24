"""
Funciones de utilidad para el proyecto
"""

import re
from decimal import Decimal
from typing import Optional


def parse_price(price_text: str) -> float:
    """
    Extraer precio numérico de texto con formato peruano
    Ejemplos: 'S/ 15.90', 'S/15,90', '15.90'
    """
    if not price_text:
        return 0.0
    
    # Remover símbolos de moneda y espacios
    price_text = price_text.replace('S/', '').replace('s/', '').strip()
    
    # Reemplazar coma por punto (formato peruano)
    price_text = price_text.replace(',', '.')
    
    # Extraer número
    match = re.search(r'[\d.]+', price_text)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return 0.0
    return 0.0


def extract_brand_from_name(name: str) -> str:
    """
    Extraer marca del nombre del producto
    Por defecto usa la primera palabra
    """
    if not name:
        return "Genérico"
    
    parts = name.strip().split()
    return parts[0] if parts else "Genérico"


def normalize_product_name(name: str) -> str:
    """
    Normalizar nombre de producto para búsqueda
    """
    if not name:
        return ""
    
    # Convertir a minúsculas
    name = name.lower()
    
    # Remover caracteres especiales
    name = re.sub(r'[^\w\s]', ' ', name)
    
    # Normalizar espacios
    name = ' '.join(name.split())
    
    return name


def format_currency(amount: Decimal) -> str:
    """
    Formatear cantidad como moneda peruana
    """
    return f"S/ {amount:.2f}"


def extract_unit_from_text(text: str) -> str:
    """
    Extraer unidad de medida del texto
    Ejemplos: 'kg', 'lt', 'unidad', 'pack'
    """
    text = text.lower()
    
    units = ['kg', 'gr', 'lt', 'ml', 'unidad', 'pack', 'und']
    
    for unit in units:
        if unit in text:
            return unit
    
    return 'unidad'


def sanitize_url(url: str) -> Optional[str]:
    """
    Validar y limpiar URL
    """
    if not url:
        return None
    
    # Asegurar que tenga protocolo
    if not url.startswith('http'):
        url = 'https://' + url
    
    return url.strip()