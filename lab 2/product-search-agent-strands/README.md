# Product Search Strands Agent

This lab demonstrates how to build a product search and recommendation agent using Strands Agents and AWS services. The agent helps customers discover clothing products based on their preferences and provides recommendations.

## Overview

The product search agent is designed to:
- Search for available clothing items in a catalog
- Provide recommendations for clothing based on events and seasons
- Filter products by various attributes (color, size, price, etc.)
- Return results in a structured JSON format

## Architecture

The solution uses a single agent architecture that integrates with multiple AWS services:
- **Amazon Bedrock** for the underlying LLM (Claude 3.7 Sonnet)
- **Amazon Bedrock Knowledge Base** for product information retrieval
- **Amazon Bedrock Guardrails** for content filtering and safety
- **Amazon DynamoDB** for storing product reviews
- **Model Context Protocol (MCP)** for extending agent capabilities

## Key Components

### 1. Product Search Agent
- Uses the `retrieve` tool from Strands Agents Tools to query the Knowledge Base
- Returns structured product information in JSON format
- Maintains conversation context for follow-up questions

### 2. Guardrails Integration
- Implements content filtering for inappropriate requests
- Blocks specific topics and words related to counterfeit products, competitor brands, etc.
- Provides safe responses when potentially harmful content is detected

### 3. MCP Server for Product Reviews
- Deploys a lightweight MCP server that exposes product review capabilities
- Connects to DynamoDB to retrieve product review data
- Integrates with the main agent through the MCP client

## Implementation Steps

The notebook walks through the following steps:
1. Installing necessary packages
2. Creating S3 Bucket and Bedrock Knowledge Base
3. Creating the Strands Agent with appropriate system prompt
4. Adding Guardrails to the Agent for content safety
5. Accessing a MCP Server to retrieve product reviews
6. Testing the Agent with various queries

## Getting Started

To run this lab, follow the instructions in the `product-search-agents.ipynb` notebook. Make sure you have completed the prerequisites lab to set up the necessary AWS resources.