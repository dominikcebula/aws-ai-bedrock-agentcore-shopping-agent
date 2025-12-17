import pytest

from products import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


def test_health_check_returns_healthy_status(client):
    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "products-catalog"


def test_list_products_returns_all_products(client):
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 30
    assert len(data["products"]) == 30


def test_list_products_filters_by_category(client):
    response = client.get("/api/v1/products?category=Laptops")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 10
    for product in data["products"]:
        assert product["category"] == "Laptops"


def test_list_products_category_filter_is_case_insensitive(client):
    response = client.get("/api/v1/products?category=laptops")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 10


def test_list_products_returns_empty_for_nonexistent_category(client):
    response = client.get("/api/v1/products?category=NonExistent")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 0
    assert data["products"] == []


def test_get_product_returns_product_when_exists(client):
    response = client.get("/api/v1/products/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Wireless Gaming Mouse"
    assert data["price"] == 59.99
    assert data["category"] == "Mice"
    assert data["stock"] == 150


def test_get_product_returns_404_when_not_found(client):
    response = client.get("/api/v1/products/999")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Product not found"


def test_product_has_all_required_fields(client):
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    data = response.get_json()
    product = data["products"][0]
    assert "id" in product
    assert "name" in product
    assert "price" in product
    assert "category" in product
    assert "stock" in product
