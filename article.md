# AI Agents – Shopping Agent using Amazon Bedrock AgentCore and Strands Agents Python SDK

## Introduction

In this article, I'll describe how I created a simplified shopping agent using the Strands Agents Python SDK, hosted in
Amazon Bedrock AgentCore.

The agent has access to a simplified Products Catalog and Order Management System, allowing it to create orders on the
user's behalf using products from the catalog. You can run the agent both locally and on AWS.

The end result is a functional agent that helps users find the right products for their needs and create orders using
prompts like:

```text
I would like to buy a budget laptop for daily usage with at least 8GB RAM and 512 GB of storage.
Please also include a monitor, mouse and a keyboard.
Select product that match my criteria and create the order.
```

The agent processes the user's request using an LLM and MCP Tools. The result is a created order reported by the agent:

```text
Your order has been created successfully! Here are the details:

- **Dell Inspiron 14 Laptop** - Price: $699.99
- **Wireless Gaming Mouse** - Price: $59.99
- **Mechanical Gaming Keyboard** - Price: $129.99
- **27-inch 4K Monitor** - Price: $349.99

**Order ID:** 9f992c3d-2af9-4de4-b8e2-1f939237866f

**Total Value:** $1239.96
```

The created order can then be managed further using the agent or traditional REST API calls.

The full source code is available on GitHub:
[https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent).

## Architecture

The diagram below depicts the architecture of the solution.

![architecture.drawio.png](assets/architecture.drawio.png)

The agent is built using the Strands Agents Python SDK and hosted in Amazon Bedrock AgentCore. It has access to two
backing services: Products Catalog and Order Management System. Both services are implemented as simple REST APIs. The
agent accesses these backing services through MCP Tools that forward requests accordingly. The backing services are
hosted on AWS Elastic Beanstalk, while the LLM runs in Amazon Bedrock.

## MCP Tools

The agent has access to two types of tools: Products Catalog Tools and Order Management Tools.

The Products Catalog Tools retrieve products from the Products Catalog service, while the Order Management Tools handle
order operations. Each MCP Tool acts as a proxy, calling the corresponding backing service REST API to execute its task.

Products Catalog Tools include listing products and retrieving product details.

Order Management Tools include creating, listing, updating, and canceling orders.

## Microservices

Two microservices have been implemented: Products Catalog and Order Management System.

Both serve as backing services for the MCP Tools exposed to the agent.

For simplicity, these microservices don't use any database storage. All data is kept in memory.

## Implementation

### Technology

The following technologies have been used:

- Python 3.12
- Strands Agents Python SDK
- Amazon Bedrock AgentCore
- Flask
- AWS Elastic Beanstalk

### Agent

At the heart of the solution is the agent, which uses an LLM and MCP Tools to process user requests.

```python
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
```

You can find the full source code
in [agent.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/agent.py).

### MCP Tools

The agent accesses data from the backing services through REST APIs exposed as MCP Tools. The following code snippet
shows the MCP Tools available to the agent. Each MCP Tool acts as a proxy to the corresponding backing service REST API.

```python
@tool(description="List all products from the catalog")
def list_products() -> dict:
    """
    Tool description - List all products from the catalog

    #Returns:
        A dictionary containing 'products' list and 'count' of products found.
    """
    url = f"{PRODUCTS_CATALOG_BASE_URL}/api/v1/products"

    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@tool(description="List products from the catalog filtered by category")
def list_products_by_category(category: str) -> dict:
    """
    Tool description - List products from the catalog filtered by category.

    #Args:
        category: category to filter products (e.g., "Mice", "Keyboards", "Monitors",
                  "Headsets", "Cameras", "Accessories", "Laptops")

    #Returns:
        A dictionary containing 'products' list and 'count' of products found.
    """
    url = f"{PRODUCTS_CATALOG_BASE_URL}/api/v1/products"
    params = {"category": category}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


@tool(description="Get a single product by its ID")
def get_product(product_id: int) -> dict:
    """
    Tool description - Get a single product by its ID.

    #Args:
        product_id: The unique identifier of the product.

    #Returns:
        A dictionary containing product details (id, name, price, category, stock),
        or an error message if the product is not found.
    """
    url = f"{PRODUCTS_CATALOG_BASE_URL}/api/v1/products/{product_id}"

    response = requests.get(url)
    if response.status_code == 404:
        return {"error": f"Product with ID {product_id} not found"}
    response.raise_for_status()
    return response.json()
```

```python
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
```

You can find the full source code
in [tools_products_catalog.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/tools_products_catalog.py)
and [tools_orders.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/tools_orders.py).

The microservice URLs are exposed as environment variables. Their values are set during deployment by automatically
fetching them based on the AWS Elastic Beanstalk environment name.

### Backing Services

The backing services are implemented as REST API microservices using Python Flask.

The Products Catalog microservice exposes endpoints for retrieving product information from the catalog. The code
snippet below shows sample Products Catalog operations.

```python
@app.route("/api/v1/products", methods=["GET"])
def list_products():
    category_filter = request.args.get("category")
    products = get_all_products(category_filter)
    return jsonify({"products": [p.to_dict() for p in products], "count": len(products)})


@app.route("/api/v1/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id: int):
    product = get_product(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())
```

Similarly, the Order Management microservice exposes endpoints for creating, listing, updating, and canceling orders.
The code snippet below shows sample order management operations.

```python
@app.route("/api/v1/orders", methods=["POST"])
def create_order_route():
    data = request.get_json()

    if not data or "items" not in data or not data["items"]:
        return jsonify({"error": "Order must contain at least one item"}), 400

    try:
        items = parse_order_items(data["items"])
    except (KeyError, ValueError) as e:
        return jsonify({"error": f"Invalid item data: {str(e)}"}), 400

    order = create_order(items)
    return jsonify(order.to_dict()), 201


@app.route("/api/v1/orders/<order_id>", methods=["GET"])
def get_order_route(order_id: str):
    order = get_order(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order.to_dict())
```

You can find the full source code
in [microservice-products-catalog](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/tree/main/microservice-products-catalog)
and [microservice-orders](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/tree/main/microservice-orders).

## Usage

### Prerequisites

- Linux
- Bash
- Python 3.12 with pip installed on your machine
- AWS CLI installed and configured
- EB CLI installed and configured

### Running the Agent Locally

You can run the agent and backing services locally. Note that you still need AWS credentials configured since the LLM
runs in Amazon Bedrock.

First, start the agent using the local runner – it will run in interactive mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python agent_runner_local.py
```

Then, run the Products Catalog microservice locally:

```bash
cd ../microservice-products-catalog
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
FLASK_RUN_PORT=5001 python application.py
```

Finally, run the Orders microservice locally:

```bash
cd ../microservice-orders
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
FLASK_RUN_PORT=5002 python application.py
```

Now you can interact with the agent using prompts like the following:

![demo-01.png](assets/demo-01.png)

This will produce the following response:

![demo-02.png](assets/demo-02.png)

### Running the Agent on AWS

To run the agent on AWS, the backing microservices need to be deployed to AWS Elastic Beanstalk first, and then the
agent can be deployed to Bedrock AgentCore.

The backing microservices are deployed using the EB CLI. To simplify deployment, I created a script like the one below:

```bash
#!/bin/bash

AWS_REGION=$(aws configure get region)

if [ ! -d ".elasticbeanstalk" ]; then
	echo "⚙️  Initializing Elastic Beanstalk Environment ..."
	eb init -p python-3.12 microservice-orders --region ${AWS_REGION} || {
		echo "❌ Error occurred while initializing Elastic Beanstalk Environment"
		exit 1
	}
	echo "✅ Done"
else
	echo "⏭️  Elastic Beanstalk already initialized, skipping ..."
fi

if ! eb status microservice-orders &>/dev/null; then
	echo "📦 Creating Elastic Beanstalk Environment ..."
	eb create microservice-orders || {
		echo "❌ Error occurred while creating Elastic Beanstalk Environment"
		exit 1
	}
	echo "✅ Done"
else
	echo "⏭️  Elastic Beanstalk environment already exists, skipping ..."
fi

echo "🚀 Deploying to Elastic Beanstalk Environment ..."
eb deploy || {
  echo "❌ Error occurred while deploying to Elastic Beanstalk Environment"
  exit 1
}
echo "✅ Done"
```

This script for `microservice-products-catalog` is
available [here](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/microservice-products-catalog/deploy.sh)
and for
`microservice-orders` [here](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/microservice-orders/deploy.sh).

Running `deploy.sh` for each microservice deploys it to AWS Elastic Beanstalk.

![demo-03.png](assets/demo-03.png)

Once the backing microservices are deployed, the agent can be deployed to Bedrock AgentCore
using [deploy.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/deploy.py).

The main part of this script is the AgentCore Starter Toolkit invocation for deploying the agent:

```python
def configure_agentcore_runtime():
    print("⚙️  Configuring AgentCore Runtime...")
    agentcore_runtime = Runtime()
    agentcore_runtime.configure(
        entrypoint="agent_runner_aws.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region=region,
        agent_name=agent_name
    )
    print("✅ AgentCore Runtime configured successfully.")

    return agentcore_runtime


def launch_agentcore_runtime(agentcore_runtime, env_vars: dict):
    print("🚀 Launching Agent to AgentCore Runtime...")
    print("⏳ This may take several minutes...")
    print(f"🔧 Environment variables: {env_vars}")
    launch_result = agentcore_runtime.launch(env_vars=env_vars)
    print("✅ Launch completed")
    print(f"🤖 Agent ARN: {launch_result.agent_arn}")
    print(f"🆔 Agent ID: {launch_result.agent_id}")

    return launch_result
```

Additionally, [deploy.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/deploy.py)
dynamically discovers the URLs of the backing microservices deployed to AWS Elastic Beanstalk and exposes them as
environment variables for the agent to use when invoking MCP Tools.

See the full source code
in [deploy.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/deploy.py).

To deploy the agent, execute the following commands:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python deploy.py
```

The deployment process will look similar to this:

![demo-04.png](assets/demo-04.png)

With both the backing microservices and agent deployed to AWS, you can invoke the agent in the cloud.

There are two ways to do this.

The first is to
use [agent_client_remote.py](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent/blob/main/agent-shopping-agent/agent_client_remote.py),
which runs a client locally and sends requests to the agent hosted in AWS Bedrock AgentCore.

Usage is similar to running locally, except that all operations are executed in the cloud via the remote AWS client:

![demo-05.png](assets/demo-05.png)

The second option is to use the Amazon Bedrock AgentCore web console to send requests to the agent.

![demo-06.png](assets/demo-06.png)

## Further Enhancements

Here are some enhancements that could be implemented in the future:

- Short-term memory (STM) and long-term memory (LTM) support, including user preference extraction and storage
- Observability: metrics, traces, and logs
- Agent correctness evaluation
- Security hardening
- Amazon Bedrock AgentCore Gateway integration

## Summary

In this article, I demonstrated how to build a shopping agent using the Strands Agents Python SDK and deploy it to
Amazon Bedrock AgentCore. The solution consists of three components: an AI agent that processes natural language
requests, and two backing microservices (Products Catalog and Order Management) that provide the data and business
logic.

The agent leverages MCP Tools to interact with the backing services, allowing it to browse products, understand user
requirements, and create orders autonomously. By using the `@tool` decorator from the Strands SDK, integrating REST APIs
as agent tools becomes straightforward.

The architecture supports both local development and cloud deployment. Locally, the agent runs in interactive mode while
microservices run on separate ports. In production, microservices are deployed to AWS Elastic Beanstalk, and the agent
is hosted in Amazon Bedrock AgentCore Runtime, with environment discovery handled automatically during deployment.

This approach demonstrates the power of combining LLMs with traditional microservices. The agent can interpret complex
user requests like "find me a budget laptop with specific requirements and create an order" and execute multi-step
workflows by orchestrating calls to the appropriate tools.

The full source code is available on
[https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent).

## References

- [Source Code on GitHub](https://github.com/dominikcebula/aws-ai-bedrock-agentcore-shopping-agent)
- [Amazon Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Amazon Bedrock AgentCore Code Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)
- [Strands Agents Python SDK](https://strandsagents.com/latest/documentation/docs/)
