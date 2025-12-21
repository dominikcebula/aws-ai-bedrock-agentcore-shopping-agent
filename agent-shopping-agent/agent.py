from strands import Agent
from strands.models import BedrockModel

from tools_products_catalog import get_product, list_products

model_id = "eu.amazon.nova-micro-v1:0"
model = BedrockModel(
    model_id=model_id,
)

agent = Agent(
    model=model,
    tools=[list_products, get_product],
    system_prompt="""You're a helpful shopping assistant. You can help users browse and find products from the catalog.

You have access to the following tools:
- list_products: List all products, optionally filtered by category (Mice, Keyboards, Monitors, Headsets, Cameras, Accessories, Laptops)
- get_product: Get details of a specific product by its ID

Help users find products that match their needs and provide helpful recommendations."""
)
