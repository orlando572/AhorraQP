from sqlalchemy import Column, Integer, Text, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text)
    
    brand = relationship("Brand")
    category = relationship("Category")
    prices = relationship("StorePrice", back_populates="product")

class StorePrice(Base):
    __tablename__ = "store_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(Text, nullable=False)
    url = Column(Text)
    is_available = Column(Boolean, default=True)
    
    product = relationship("Product", back_populates="prices")
    store = relationship("Store")