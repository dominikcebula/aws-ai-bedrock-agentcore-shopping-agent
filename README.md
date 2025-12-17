# 📦 Amazon Bedrock AgentCore Shopping Agent Code Sample

## 📝 Overview

This repository contains code for an AWS Bedrock AgentCore Agent that uses a products catalog to create orders on the
user's behalf. It demonstrates how to build microservices that can be orchestrated by an AI agent to perform e-commerce
operations.

## 🏗️ Architecture

The project consists of two independent microservices:

### Products Catalog (`microservice-products-catalog`)

A REST API providing a catalog of 30 computer products across 7 categories (Mice, Keyboards, Monitors, Headsets,
Cameras, Accessories, Laptops).

**Endpoints:**

- `GET /api/v1/products` - List all products (supports `?category=` filter)
- `GET /api/v1/products/<id>` - Get a single product

### Orders Service (`microservice-orders`)

A REST API for managing customer orders with full CRUD operations.

**Endpoints:**

- `POST /api/v1/orders` - Create a new order
- `GET /api/v1/orders` - List all orders (supports `?status=` filter)
- `GET /api/v1/orders/<id>` - Get a single order
- `PUT /api/v1/orders/<id>` - Update an order
- `DELETE /api/v1/orders/<id>` - Cancel an order

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Framework:** Flask 3.1.2
- **Testing:** pytest 8.3.4
- **Deployment:** AWS Elastic Beanstalk
- **Storage:** In-memory (no database required)

## 🚀 Getting Started

Each microservice can be run independently:

```bash
cd microservice-products-catalog  # or microservice-orders

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally (starts on port 5000)
python application.py

# Run tests
pytest -v
```

## ☁️ AWS Deployment

Each microservice includes deployment scripts for AWS Elastic Beanstalk:

```bash
# Deploy to AWS
./deploy.sh

# Terminate environment
./destroy.sh
```

Requires AWS CLI and EB CLI configured with valid credentials.

## ✍ Author

Dominik Cebula

- https://dominikcebula.com/
- https://blog.dominikcebula.com/
- https://www.udemy.com/user/dominik-cebula/
