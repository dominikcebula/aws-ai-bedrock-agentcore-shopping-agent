import pytest

from orders import create_app
from orders.repository import clear_orders


@pytest.fixture
def client():
    app = create_app()
    clear_orders()
    with app.test_client() as client:
        yield client


def create_sample_order(client, product_id="prod-1", name="Widget", price=29.99, quantity=2):
    order_data = {
        "items": [{"product_id": product_id, "name": name, "price": price, "quantity": quantity}]
    }
    response = client.post("/api/v1/orders", json=order_data)
    return response.get_json()


def test_create_and_retrieve_order(client):
    order_data = {
        "items": [
            {"product_id": "prod-1", "name": "Widget", "price": 29.99, "quantity": 2},
            {"product_id": "prod-2", "name": "Gadget", "price": 49.99, "quantity": 1},
        ]
    }

    create_response = client.post("/api/v1/orders", json=order_data)

    assert create_response.status_code == 201
    created_order = create_response.get_json()
    assert "id" in created_order
    assert created_order["status"] == "confirmed"
    assert len(created_order["items"]) == 2
    assert created_order["total_value"] == 29.99 * 2 + 49.99 * 1

    order_id = created_order["id"]
    get_response = client.get(f"/api/v1/orders/{order_id}")

    assert get_response.status_code == 200
    retrieved_order = get_response.get_json()
    assert retrieved_order["id"] == order_id
    assert retrieved_order["status"] == "confirmed"
    assert retrieved_order["items"] == created_order["items"]
    assert retrieved_order["total_value"] == created_order["total_value"]


def test_list_orders_returns_empty_list_when_no_orders_exist(client):
    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    data = response.get_json()
    assert data["orders"] == []
    assert data["count"] == 0


def test_list_orders_returns_three_orders_when_three_orders_created(client):
    create_sample_order(client, product_id="prod-1", name="Widget")
    create_sample_order(client, product_id="prod-2", name="Gadget")
    create_sample_order(client, product_id="prod-3", name="Gizmo")

    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 3
    assert len(data["orders"]) == 3


def test_get_order_returns_404_when_order_does_not_exist(client):
    response = client.get("/api/v1/orders/non-existent-id")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Order not found"


def test_get_order_returns_correct_order_when_three_orders_exist(client):
    order1 = create_sample_order(client, product_id="prod-1", name="Widget")
    order2 = create_sample_order(client, product_id="prod-2", name="Gadget")
    order3 = create_sample_order(client, product_id="prod-3", name="Gizmo")

    response = client.get(f"/api/v1/orders/{order2['id']}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == order2["id"]
    assert data["items"][0]["name"] == "Gadget"


def test_update_order_updates_with_correct_data(client):
    order = create_sample_order(client, product_id="prod-1", name="Widget", price=10.00, quantity=1)

    update_data = {
        "items": [{"product_id": "prod-1", "name": "Updated Widget", "price": 25.00, "quantity": 3}]
    }
    response = client.put(f"/api/v1/orders/{order['id']}", json=update_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["items"][0]["name"] == "Updated Widget"
    assert data["items"][0]["price"] == 25.00
    assert data["items"][0]["quantity"] == 3
    assert data["total_value"] == 75.00


def test_update_order_returns_404_for_non_existing_order(client):
    update_data = {
        "items": [{"product_id": "prod-1", "name": "Widget", "price": 10.00, "quantity": 1}]
    }
    response = client.put("/api/v1/orders/non-existent-id", json=update_data)

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Order not found"


def test_update_order_returns_400_for_cancelled_order(client):
    order = create_sample_order(client)

    client.delete(f"/api/v1/orders/{order['id']}")

    update_data = {
        "items": [{"product_id": "prod-1", "name": "Widget", "price": 10.00, "quantity": 1}]
    }
    response = client.put(f"/api/v1/orders/{order['id']}", json=update_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Cannot update a cancelled order"


def test_cancel_order_updates_status_to_cancelled(client):
    order = create_sample_order(client)

    response = client.delete(f"/api/v1/orders/{order['id']}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "cancelled"

    get_response = client.get(f"/api/v1/orders/{order['id']}")
    assert get_response.get_json()["status"] == "cancelled"
