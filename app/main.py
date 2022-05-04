from typing import Any, Generator

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi_restful.tasks import repeat_every
from sqlalchemy.orm import Session

from app import crud, models, offers, schemas
from app.config import settings
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/products/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Product,
    tags=["products"],
)
def create_product(
    product: schemas.ProductCreate, background_task: BackgroundTasks, db: Session = Depends(get_db)
) -> Any:
    """
    Create a new product:

    - **name** product name
    - **description** product description
    """
    db_product = crud.create_product(db=db, product=product)
    background_task.add_task(offers.register_product, db_product)
    return db_product


@app.get("/products/", response_model=list[schemas.Product], tags=["products"])
def read_products(db: Session = Depends(get_db)) -> Any:
    """Get a list of all products."""
    return crud.get_products(db)


@app.get("/products/{product_id}", response_model=schemas.Product, tags=["products"])
def read_product(product_id: int, db: Session = Depends(get_db)) -> Any:
    """Get a product with product_id in the path."""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/products/{product_id}", response_model=schemas.Product, tags=["products"])
def update_product(
    product_id: int, updated_product: schemas.ProductUpdate, db: Session = Depends(get_db)
) -> Any:
    """
    Update a product with product_id in the path:

    - **name** updated name
    - **description** updated description
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product = crud.update_product(db, product=db_product, updated_product=updated_product)
    return db_product


@app.delete("/products/{product_id}", response_model=schemas.Product, tags=["products"])
def remove_product(product_id: int, db: Session = Depends(get_db)) -> Any:
    """Remove a product with product_id in the path."""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.remove_product(db, product_id=product_id)
    return db_product


@app.get("/products/{product_id}/offers", response_model=schemas.ProductOffers, tags=["offers"])
def read_product_offers(product_id: int, db: Session = Depends(get_db)) -> Any:
    """Get a product with product_id in the path and a list of its offers."""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.on_event("startup")
@repeat_every(seconds=60, raise_exceptions=True)
def refresh_offers() -> None:
    """Background job refreshing the products offers data from the offers microservice."""
    with SessionLocal() as db:
        for product in crud.get_products(db):
            offers.refresh_offer(db, product)
