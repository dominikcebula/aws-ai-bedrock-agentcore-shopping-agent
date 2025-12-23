# AI Agents – Creating a Shopping Agent using Amazon Bedrock AgentCore and Strands Agents Python SDK

## Introduction

TBD - in this article I will describe how I have created a simplified version of a shopping agent using Strands Agents
Python SDK that is hosted in Amazon Bedrock AgentCore. Agent has access to a simplified Product Catalog and
Order Management System that allows agent to create orders on user behalf. It is possible to execute agent both locally
and on AWS.

## Architecture

The below diagram depicts the architecture of the solution.

![architecture.drawio.png](assets/architecture.drawio.png)

Agent is built using Strands Agents Python SDK and is hosted in Amazon Bedrock AgentCore. Agent has access to two
backing services: Products Catalog and Order Management System. Both services are implemented as simple REST APIs. Agent
accesses backing services using MCP Tools that are forwarding requests to the backing services. Backing services are
hosted using AWS Elastic Beanstalk.

Agent is using LLM hosted in Amazon Bedrock to process user prompts, decide which tools to use when processing user
requests and generate responses.

## MCP Tools

Two types of tools have been made available for the agent: Products Catalog Tools and Order Management System Tools.
Products Catalog Tasks are used to retrieve products from the Products Catalog service, and Order Management System
Tasks are used to create orders in the Order Management System service. Exposed MCP Tools are using backing services
REST APIs to execute on a given task.

Products Catalog Tools include tools like listing products in the product catalog or getting product details.

Order Management System Tools include tools like creating, listing, updating, cancelling orders.

## Microservices

Two microservices have been implemented: Products Catalog and Order Management System.

Both are used as a backing service for the MCP Tools that are exposed to the agent.

## Implementation

### Agent

TBD

### MCP Tools

TBD

### Backing Services

TBD

## Deployment

### Agent

TBD

### Backing Services

TBD

## Running the Agent locally

TBD

## Running the Agent on AWS

TBD

## Further Enhancements

TBD

## References

- [Amazon Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Amazon Bedrock AgentCore Code Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)
- [Strands Agents Python SDK](https://strandsagents.com/latest/documentation/docs/)

## Summary

TBD
