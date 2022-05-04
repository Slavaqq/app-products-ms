from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas

def create_product(db: Session) -> models.Product:
    product = schemas.ProductCreate(name="product1", description="product1 description") 
    return crud.create_product(db, product) 

