from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

    offers = relationship("Offer", back_populates="product")


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, index=True, primary_key=True)
    price = Column(Integer)
    items_in_stock = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)

    product = relationship("Product", back_populates="offers")
