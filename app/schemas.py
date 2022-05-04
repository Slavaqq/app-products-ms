from typing import Optional

from pydantic import BaseModel


class OfferBase(BaseModel):
    price: int
    items_in_stock: int


class OfferCreate(OfferBase):
    id: int


class OfferUpdate(OfferBase):
    pass


class Offer(OfferBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(ProductBase):
    name: str
    description: str


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductOffers(ProductBase):
    id: int
    offers: list[Offer] = []

    class Config:
        orm_mode = True
