# Inventory Agent with AWS Services

This lab demonstrates how to build an inventory management agent using Strands Agents and AWS services. The agent helps customers check product availability in the inventory.

## Overview

The inventory agent is designed to:
- Check if specific products are available in stock
- Return inventory information in a structured JSON format
- Connect directly to DynamoDB to retrieve real-time inventory data

## Architecture

The solution uses a single agent architecture that integrates with AWS services:
- **Amazon Bedrock** for the underlying LLM (Nova Premier)
- **Amazon DynamoDB** for storing product inventory information
- **Strands Agents Tools** for AWS service integration

## Key Components

### 1. AWS Integration
- Uses the `use_aws` tool from Strands Agents Tools to interact with AWS services
- Connects directly to DynamoDB to query inventory data

### 2. Custom Tool
- Implements a custom `get_product` tool that retrieves product details from DynamoDB
- Formats the response to show product availability

### 3. Structured Output
- Returns inventory information in a consistent JSON format
- Includes product ID and availability status (in_stock: "yes"/"no")

## Implementation Steps

The notebook walks through the following steps:
1. Installing necessary packages (strands-agents, strands-agents-tools, boto3)
2. Setting up the Bedrock model configuration
3. Creating a custom tool to query DynamoDB
4. Defining the agent with appropriate system prompt
5. Testing the agent with product availability queries

## Getting Started

To run this lab, follow the instructions in the `Inventory-agent.ipynb` notebook. The agent uses DynamoDB to check product inventory in real-time.