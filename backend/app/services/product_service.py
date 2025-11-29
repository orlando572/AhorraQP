from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from decimal import Decimal
from app.models import Product, Brand, Category, StorePrice
from app.models.store import Store
from app.schemas.product import ProductResponse, PriceInfo
from app.schemas.cart import CartItem, CartTotalsResponse, StoreTotalResponse
from fastapi import HTTPException

class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    def search_products(self, query: str, category_id: int = None) -> List[ProductResponse]:
        """Buscar productos por nombre"""
        q = self.db.query(Product).join(Brand).join(Category)

        q = q.filter(
            or_(
                Product.name.ilike(f"%{query}%"),
                Brand.name.ilike(f"%{query}%")
            )
        )
        
        if category_id:
            q = q.filter(Product.category_id == category_id)
        
        products = q.limit(50).all()
        return [self._build_product_response(p) for p in products]
    
    def get_product_by_id(self, product_id: int) -> ProductResponse:
        """Obtener producto por ID"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return self._build_product_response(product)
    
    def list_products(self, skip: int, limit: int) -> List[ProductResponse]:
        """Listar productos con paginación"""
        products = self.db.query(Product).offset(skip).limit(limit).all()
        return [self._build_product_response(p) for p in products]
    
    def calculate_cart_totals(self, items: List[CartItem]) -> CartTotalsResponse:
        """Calcular totales por tienda para una lista de compras"""
        stores = self.db.query(Store).all()
        totals = []
        
        for store in stores:
            total = Decimal(0)
            available = 0
            unavailable = 0
            
            for item in items:
                price_info = self.db.query(StorePrice).filter(
                    StorePrice.product_id == item.product_id,
                    StorePrice.store_id == store.id
                ).first()
                
                if price_info and price_info.is_available:
                    total += price_info.price * item.quantity
                    available += 1
                else:
                    unavailable += 1
            
            totals.append(StoreTotalResponse(
                store_id=store.id,
                store_name=store.name,
                total=total,
                items_available=available,
                items_unavailable=unavailable
            ))
        
        totals.sort(key=lambda x: x.total)
        return CartTotalsResponse(totals=totals)
    
    def _build_product_response(self, product: Product) -> ProductResponse:
        """Construir respuesta con precios de todas las tiendas"""
        prices = []
        for sp in product.prices:
            prices.append(PriceInfo(
                store_id=sp.store_id,
                store_name=sp.store.name,
                price=sp.price,
                url=sp.url,
                is_available=sp.is_available
            ))
        
        return ProductResponse(
            id=product.id,
            name=product.name,
            brand_name=product.brand.name,
            category_name=product.category.name,
            image_url=product.image_url,
            prices=prices
        )