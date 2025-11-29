from sqlalchemy import Column, Integer, Text
from app.database.session import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True)