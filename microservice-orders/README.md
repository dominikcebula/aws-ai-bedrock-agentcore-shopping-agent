# 📦 Orders Microservice

## 📝 Overview

A RESTful microservice for managing customer orders. Provides endpoints to create, retrieve, update, list, and cancel
orders. Each order contains product items with pricing and quantity information, with automatic calculation of order
totals.

## Technology

- **Python 3.12** - Runtime environment
- **Flask** - Lightweight web framework for building the REST API
- **AWS Elastic Beanstalk** - Cloud deployment platform for hosting the microservice

## Usage

### Requirements

- Python 3.12
- AWS CLI configured with valid credentials
- AWS Elastic Beanstalk CLI (`eb`) installed and configured

### Running locally

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python application.py
   ```

4. Test the endpoints:

   **Create an order:**
   ```bash
   curl -X POST http://localhost:5000/api/v1/orders \
     -H "Content-Type: application/json" \
     -d '{
       "items": [
         {"product_id": "KB-MX-001", "name": "Logitech MX Keys Wireless Keyboard", "price": 119.99, "quantity": 1},
         {"product_id": "MS-MX-003", "name": "Logitech MX Master 3S Mouse", "price": 99.99, "quantity": 1}
       ]
     }'
   ```

   **Update the order** (replace `{order_id}` with the ID from the create response):
   ```bash
   curl -X PUT http://localhost:5000/api/v1/orders/{order_id} \
     -H "Content-Type: application/json" \
     -d '{
       "items": [
         {"product_id": "KB-MX-001", "name": "Logitech MX Keys Wireless Keyboard", "price": 119.99, "quantity": 1},
         {"product_id": "MS-MX-003", "name": "Logitech MX Master 3S Mouse", "price": 99.99, "quantity": 1},
         {"product_id": "MON-DELL-27", "name": "Dell UltraSharp 27\" 4K Monitor", "price": 449.99, "quantity": 2}
       ]
     }'
   ```

   **Get a single order:**
   ```bash
   curl http://localhost:5000/api/v1/orders/{order_id}
   ```

   **List all orders:**
   ```bash
   curl http://localhost:5000/api/v1/orders
   ```

   **Cancel an order:**
   ```bash
   curl -X DELETE http://localhost:5000/api/v1/orders/{order_id}
   ```

### Deployment

Run the deployment script to deploy the microservice to AWS Elastic Beanstalk:

```bash
./deploy.sh
```

The script will automatically:

- Initialize Elastic Beanstalk (if not already initialized)
- Create the environment (if not already created)
- Deploy the application

### Terminating

Run the destroy script to terminate the AWS Elastic Beanstalk environment:

```bash
./destroy.sh
```

## ✍ Author

Dominik Cebula

- https://dominikcebula.com/
- https://blog.dominikcebula.com/
- https://www.udemy.com/user/dominik-cebula/
