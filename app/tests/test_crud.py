from sqlalchemy.orm import Session

from app import crud
from app.schemas import ProductCreate, ProductUpdate
from app.tests import utils


def test_create_product(db: Session) -> None:
    product = ProductCreate(name="product1", description="product1 description")
    product_db = crud.create_product(db, product=product)
    assert product_db.name == product.name
    assert product_db.description == product.description

def test_read_product(db: Session) -> None:
    product = utils.create_product(db)
    product_db = crud.get_product(db, product.id)
    assert product_db.id == product.id
    assert product_db.name == product.name
    assert product_db.description == product.description


def test_update_product(db: Session) -> None:
    product = utils.create_product(db)
    updated_product = ProductUpdate(name="product updated", description="description updated")
    product_db = crud.update_product(db, product, updated_product=updated_product)
    assert product_db.id == product.id
    assert product_db.name == updated_product.name
    assert product_db.description == updated_product.description


def test_remove_product(db: Session) -> None:
    product = utils.create_product(db)
    product_db = crud.remove_product(db, product.id)
    assert product_db.id == product.id
    removed_product_db = crud.get_product(db, product_db.id)
    assert removed_product_db is None
