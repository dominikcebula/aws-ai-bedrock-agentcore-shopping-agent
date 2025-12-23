# 📦 Shopping Agent

## 📝 Overview

This repository contains a code for Shopping Agent built using Strands Agents SDK and deployed to Amazon Bedrock
AgentCore Runtime. The agent uses MCP Tools that allows agent to access REST APIs
for [products catalog](../microservice-products-catalog) and [orders](../microservice-orders) microservice.

Products catalog is used to find products that agent can buy.

Orders microservice is used to create orders for products that the agent has bought.

## 🛠️ Technology

- **Python 3.10+** - Runtime environment
- **Strands Agents SDK** - open source SDK that takes a model-driven approach to building and running AI agents
- **Amazon Bedrock AgentCore** - agentic platform for building, deploying, and operating effective agents securely at
  scale

## 🚀 Usage

### ⚙️ Requirements

- Python 3.10+
- AWS credentials configured
- Docker

### ⏳ 1. Prerequisites

- Create venv
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
- Install requirements
    ```bash
    pip install -r requirements.txt
    ``` 

### 💻 2. Run Locally

- Run agent using a local runner - agent will run in an interactive mode
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  python agent_runner_local.py
  ```

- Run down-line microservices locally
  ```bash
  cd ../microservice-products-catalog
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  FLASK_RUN_PORT=5001 python application.py
  ```

  ```bash
  cd ../microservice-orders
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  FLASK_RUN_PORT=5002 python application.py
  ```

### ☁️ 3. AWS Setup

- Deploy Agent to AWS:
  ```bash
  python deploy.py
  ```

### 🌐 4. Remote Client Example

- Connect to a deployed agent on AWS, execute prompt and see results:
  ```bash
  python agent_client_remote.py
  ```

### 🧹 5. Cleanup

- Remove AWS resources and clean up:
  ```bash
  python cleanup.py
  ```

## 📄 Script Descriptions

- `deploy.py`: Deploys the Strands Agent with the Amazon Bedrock model to the AWS AgentCore runtime, setting up all
  necessary resources.
- `agent.py`: Contains the main logic for the Strands Agent, including tool integration and model configuration.
- `agent_runner_aws.py` - entrypoint that allows to run the agent on AWS using Amazon Bedrock AgentCore Runtime
- `agent_runner_local.py` - entrypoint that allows to run the agent locally
- `agent_client_remote.py`: Provides a client example for connecting to the deployed agent on AWS, sending prompts, and
  displaying results.
- `cleanup.py`: Cleans up AWS resources created during deployment. It checks if the agent runtime with the specified

## 🔗 References

- [Hosting Strands Agents with Amazon Bedrock models in Amazon Bedrock AgentCore Runtime](https://github.com/awslabs/amazon-bedrock-agentcore-samples/blob/main/01-tutorials/01-AgentCore-runtime/01-hosting-agent/01-strands-with-bedrock-model/runtime_with_strands_and_bedrock_models.ipynb)

## ✍ Author

Dominik Cebula

- https://dominikcebula.com/
- https://blog.dominikcebula.com/
- https://www.udemy.com/user/dominik-cebula/
