from sqlalchemy import Column, Integer, Text
from app.database.session import Base

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    logo_url = Column(Text)