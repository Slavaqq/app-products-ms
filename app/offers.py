import requests
from sqlalchemy.orm import Session

from app.crud import create_or_updated_offer
from app.models import Product
from app.config import settings


def register_product(product: Product) -> None:
    """Register a new product in the offers microservice."""
    json_data = {"id": product.id, "name": product.name, "description": product.description}
    headers = {"Bearer": settings.offers_access_token}
    requests.post(f"{settings.offers_base_url}/products/register", json=json_data, headers=headers)


def refresh_offer(db: Session, product: Product) -> None:
    """Refresh the offers for the product in the offers microservice."""
    headers = {"Bearer": settings.offers_access_token}
    response = requests.get(
        f"{settings.offers_base_url}/products/{product.id}/offers", headers=headers
    )
    if response.status_code == 200:
        for offer in response.json():
            create_or_updated_offer(db, offer, product_id=product.id)
