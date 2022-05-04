from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests import utils


def test_create_product(client: TestClient) -> None:
    json_data = {"name": "product1", "description": "product1 description"}
    response = client.post("/products/", json=json_data)
    assert response.status_code == 201
    content = response.json()
    assert "id" in content
    assert content["name"] == json_data["name"]
    assert content["description"] == json_data["description"]


def test_read_product(client: TestClient, db: Session) -> None:
    product = utils.create_product(db)
    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == product.id
    assert content["name"] == product.name
    assert content["description"] == product.description


def test_read_product_not_found(client: TestClient, db: Session) -> None:
    response = client.get(f"/products/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_update_product(client: TestClient, db: Session) -> None:
    json_data = {"name": "product updated", "description": "description updated"}
    product = utils.create_product(db)
    response = client.put(f"/products/{product.id}", json=json_data)
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == product.id
    assert content["name"] == json_data["name"]
    assert content["description"] == json_data["description"]


def test_remove_product(client: TestClient, db: Session) -> None:
    product = utils.create_product(db)
    response = client.delete(f"/products/{product.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == product.id
    assert content["name"] == product.name
    assert content["description"] == product.description
    response = client.get(f"/products/{product.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_remove_product_not_found(client: TestClient, db: Session) -> None:
    response = client.delete(f"/products/{-1}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
