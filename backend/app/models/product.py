from sqlalchemy import Column, Integer, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(Text)
    
    # Referencias
    brand = relationship("Brand")
    category = relationship("Category")
    prices = relationship("StorePrice", back_populates="product")
    
    # Índice compuesto para evitar duplicados y acelerar búsquedas
    __table_args__ = (
        Index('idx_product_name_brand', 'name', 'brand_id'),
    )