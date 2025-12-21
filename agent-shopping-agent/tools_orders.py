import os

import requests
from strands import tool

ORDERS_BASE_URL = os.environ.get("ORDERS_BASE_URL", "http://localhost:5002")


@tool(description="Create a new order with the specified items")
def create_order(items: list[dict]) -> dict:
    """
    Tool description - Create a new order with the specified items.

    #Args:
        items: List of order items. Each item must have:
               - product_id: The product ID (string)
               - name: Product name (string)
               - price: Product price (float)
               - quantity: Number of items to order (int)

    #Returns:
        The created order with id, items, total_value, status, created_at, and updated_at.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders"

    response = requests.post(url, json={"items": items})
    if response.status_code == 400:
        return {"error": response.json().get("error", "Invalid order data")}
    response.raise_for_status()
    return response.json()


@tool(description="List all orders")
def list_orders() -> dict:
    """
    Tool description - List all orders

    #Returns:
        A dictionary containing 'orders' list and 'count' of orders found.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders"

    response = requests.get(url)
    if response.status_code == 400:
        return {"error": response.json().get("error", "Invalid status")}
    response.raise_for_status()
    return response.json()


@tool(description="List orders, filtered by status")
def list_orders_filtered_by_status(status: str) -> dict:
    """
    Tool description - List orders, filtered by status.

    #Args:
        status: Optional status filter ("confirmed" or "cancelled")

    #Returns:
        A dictionary containing 'orders' list and 'count' of orders found.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders"
    params = {"status": status}

    response = requests.get(url, params=params)
    if response.status_code == 400:
        return {"error": response.json().get("error", "Invalid status")}
    response.raise_for_status()
    return response.json()


@tool(description="Get a single order by its ID")
def get_order(order_id: str) -> dict:
    """
    Tool description - Get a single order by its ID.

    #Args:
        order_id: The unique identifier of the order.

    #Returns:
        The order details (id, items, total_value, status, created_at, updated_at),
        or an error message if the order is not found.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders/{order_id}"

    response = requests.get(url)
    if response.status_code == 404:
        return {"error": f"Order with ID {order_id} not found"}
    response.raise_for_status()
    return response.json()


@tool(description="Update an existing order's items or status")
def update_order(order_id: str, items: list[dict] = None, status: str = None) -> dict:
    """
    Tool description - Update an existing order's items or status.

    #Args:
        order_id: The unique identifier of the order to update.
        items: Optional new list of order items. Each item must have:
               - product_id: The product ID (string)
               - name: Product name (string)
               - price: Product price (float)
               - quantity: Number of items (int)
        status: Optional new status ("confirmed" or "cancelled")

    #Returns:
        The updated order, or an error message if the order is not found or cannot be updated.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders/{order_id}"

    data = {}
    if items is not None:
        data["items"] = items
    if status is not None:
        data["status"] = status

    if not data:
        return {"error": "No update data provided. Specify items or status."}

    response = requests.put(url, json=data)
    if response.status_code == 404:
        return {"error": f"Order with ID {order_id} not found"}
    if response.status_code == 400:
        return {"error": response.json().get("error", "Invalid update data")}
    response.raise_for_status()
    return response.json()


@tool(description="Cancel an existing order")
def cancel_order(order_id: str) -> dict:
    """
    Tool description - Cancel an existing order.

    #Args:
        order_id: The unique identifier of the order to cancel.

    #Returns:
        The cancelled order, or an error message if the order is not found or already cancelled.
    """
    url = f"{ORDERS_BASE_URL}/api/v1/orders/{order_id}"

    response = requests.delete(url)
    if response.status_code == 404:
        return {"error": f"Order with ID {order_id} not found"}
    if response.status_code == 400:
        return {"error": response.json().get("error", "Order is already cancelled")}
    response.raise_for_status()
    return response.json()
