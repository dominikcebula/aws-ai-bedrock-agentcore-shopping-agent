from strands import Agent
from strands.models import BedrockModel

from tools_orders import cancel_order, create_order, get_order, list_orders, update_order
from tools_products_catalog import get_product, list_products

model_id = "eu.amazon.nova-micro-v1:0"
model = BedrockModel(
    model_id=model_id,
)

agent = Agent(
    model=model,
    tools=[
        list_products,
        get_product,
        create_order,
        list_orders,
        get_order,
        update_order,
        cancel_order,
    ],
    system_prompt="""You're a helpful shopping assistant. You can help users browse products and manage their orders.

You have access to the following tools:

Product Catalog:
- list_products: List all products from the catalog
- list_products_by_category: List products from the catalog filtered by category (Mice, Keyboards, Monitors, Headsets, Cameras, Accessories, Laptops)
- get_product: Get details of a specific product by its ID

Order Management:
- create_order: Create a new order with items (requires product_id, name, price, quantity for each item)
- list_orders: List all orders
- list_orders_filtered_by_status: List orders, filtered by status
- get_order: Get details of a specific order by its ID
- update_order: Update an order's items or status
- cancel_order: Cancel an existing order

When helping users place orders, first look up products to get accurate product_id, name, and price information.
"""
)
