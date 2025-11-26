from sqlalchemy import Column, Integer, Text, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base

class StorePrice(Base):
    __tablename__ = "store_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    url = Column(Text)
    is_available = Column(Boolean, default=True)
    
    # Referencias como string para evitar ciclos
    product = relationship("Product", back_populates="prices")
    store = relationship("Store")