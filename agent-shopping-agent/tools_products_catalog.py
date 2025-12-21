import os

import requests
from strands import tool

PRODUCTS_CATALOG_BASE_URL = os.environ.get("PRODUCTS_CATALOG_BASE_URL", "http://localhost:5000")


@tool
def list_products(category: str = None) -> dict:
    """
    List all products from the catalog, optionally filtered by category.

    Args:
        category: Optional category to filter products (e.g., "Mice", "Keyboards", "Monitors",
                  "Headsets", "Cameras", "Accessories", "Laptops")

    Returns:
        A dictionary containing 'products' list and 'count' of products found.
    """
    url = f"{PRODUCTS_CATALOG_BASE_URL}/api/v1/products"
    params = {}
    if category:
        params["category"] = category

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@tool
def get_product(product_id: int) -> dict:
    """
    Get a single product by its ID.

    Args:
        product_id: The unique identifier of the product.

    Returns:
        A dictionary containing product details (id, name, price, category, stock),
        or an error message if the product is not found.
    """
    url = f"{PRODUCTS_CATALOG_BASE_URL}/api/v1/products/{product_id}"

    response = requests.get(url)
    if response.status_code == 404:
        return {"error": f"Product with ID {product_id} not found"}
    response.raise_for_status()
    return response.json()
