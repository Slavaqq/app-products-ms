from typing import Union, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from . import models, schemas


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session):
    return db.query(models.Product).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def remove_product(db: Session, product_id: int):
    db.query(models.Offer).filter(models.Offer.product_id == product_id).delete()
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product


def update_product(
    db: Session,
    product: schemas.Product,
    updated_product: Union[schemas.ProductUpdate, dict[str, Any]],
):
    product_data = jsonable_encoder(product)
    if isinstance(updated_product, dict):
        updated_data = updated_product
    else:
        updated_data = updated_product.dict(exclude_unset=True)
    for field in product_data:
        if field in updated_data:
            setattr(product, field, updated_data[field])
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_offer(db: Session, offer: dict[str, Any], product_id: int):
    db_offer = models.Offer(**offer, product_id=product_id)
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def update_offer(
    db: Session, offer: schemas.OfferUpdate, updated_offer: Union[schemas.Offer, dict[str, Any]]
):
    offer_data = jsonable_encoder(offer)
    if isinstance(updated_offer, dict):
        updated_data = updated_offer
    else:
        updated_offer.dict(exclude_unset=True)
    for field in offer_data:
        if field in updated_data:
            setattr(offer, field, updated_data[field])
        db.add(offer)
        db.commit()
        db.refresh(offer)


def create_or_updated_offer(db: Session, offer: dict[str, Any], product_id: int):
    offer_db = (
        db.query(models.Offer)
        .filter(models.Offer.product_id == product_id)
        .filter(models.Offer.id == offer["id"])
        .first()
    )
    if offer_db is None:
        create_offer(db, offer, product_id)
    else:
        update_offer(db, offer_db, offer)
