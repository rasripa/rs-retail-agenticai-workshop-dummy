# Agentic AI with Strands Agents for Retail & CPG

This workshop demonstrates how to build intelligent AI agents for retail and consumer packaged goods (CPG) applications using Strands Agents and AWS services. Learn how to create specialized agents that can answer questions, search products, check inventory, and collaborate to solve complex customer queries.

## Workshop Structure

### Prerequisites
Before starting any labs, run the setup notebook in the `prereqs` folder:
- Sets up AWS resources (S3 buckets, DynamoDB tables, Bedrock Knowledge Bases)
- Loads sample product data
- Creates necessary infrastructure for all labs

### Lab 0: Fundamentals
- Introduction to Strands Agents framework
- Basic agent creation and configuration
- Working with models, tools, and observability

### Lab 1: FAQ Agents
- **Lab 1a**: Creating an FAQ agent using Amazon Bedrock Agent Builder
- **Lab 1b**: Building a custom FAQ agent with Strands Agents and Bedrock Knowledge Base

### Lab 2: Product Search Agent
- Creating a product search and recommendation agent
- Connecting to Bedrock Knowledge Base for product information
- Implementing guardrails for content safety
- Using MCP Server for product reviews

### Lab 3: Inventory Agent
- Building an inventory management agent
- Connecting to DynamoDB for real-time inventory data
- Returning structured inventory information

### Lab 4: Search Orchestrator Agent
- Implementing multi-agent collaboration
- Creating an orchestrator agent that coordinates specialized agents
- Routing queries to appropriate agents based on intent

## Key Technologies

- **Amazon Bedrock**: Foundation models for natural language understanding
- **Strands Agents**: Code-first framework for building AI agents
- **Amazon Bedrock Knowledge Base**: Vector database for semantic search
- **Amazon DynamoDB**: NoSQL database for product and inventory data
- **Model Context Protocol (MCP)**: Standard for agent-tool communication

## Getting Started

1. Start with the prerequisites notebook in the `prereqs` folder
2. Complete Lab 0 to understand the fundamentals of Strands Agents
3. Progress through Labs 1-4 in sequence
4. Each lab builds on concepts from previous labs

## Requirements

- AWS account with access to Amazon Bedrock
- Python 3.9+
- Required Python packages: strands-agents, strands-agents-tools, boto3

## Get started
Open `prereqs` folder to start the first activity.
