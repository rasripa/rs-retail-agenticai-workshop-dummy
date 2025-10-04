# Import required libraries

import boto3
import json
import os
import argparse
from strands import Agent, tool
from strands_tools import retrieve
from strands.models import BedrockModel
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Configure region, SSM client and AgentCore Gateway

# Set up AWS region and get configuration from SSM Parameter Store
region = boto3.Session().region_name
print(f"Using AWS region: {region}")

# Initialize SSM client
ssm_client = boto3.client('ssm', region_name=region)

# Retrieve configuration parameters - AgentCore Gateway has been previously created
try:
    prod_search_kb_id = ssm_client.get_parameter(Name="product_search_kb_id")['Parameter']['Value']
    prod_search_agent_model_id = ssm_client.get_parameter(Name="prod_search_agent_model_id")['Parameter']['Value']
    agentcore_mcp_gatewayURL = ssm_client.get_parameter(Name="anycomp_prod_reviews_mcp_server_url")['Parameter']['Value']
    anycomp_agcore_gw_cognito_accesstoken = ssm_client.get_parameter(Name="anycomp_agcore_gw_cognito_accesstoken")['Parameter']['Value']

    print("✅ Configuration parameters retrieved successfully!")
    print(f"Knowledge Base ID: {prod_search_kb_id}")
    print(f"Model ID: {prod_search_agent_model_id}")
    print(f"MCP Gateway URL: {agentcore_mcp_gatewayURL}")
    
except Exception as e:
    print(f"❌ Error retrieving parameters: {e}")
    print("Please ensure all required SSM parameters are configured.")

# Set environment variables
os.environ["AWS_REGION"] = region
os.environ["MIN_SCORE"] = "0.4"
os.environ["KNOWLEDGE_BASE_ID"] = prod_search_kb_id

print("✅ Environment variables configured:")
print(f"AWS_REGION: {os.environ['AWS_REGION']}")
print(f"MIN_SCORE: {os.environ['MIN_SCORE']}")
print(f"KNOWLEDGE_BASE_ID: {os.environ['KNOWLEDGE_BASE_ID']}")
    
# Create a Bedrock model instance
_bedrock_model = BedrockModel(
    model_id=prod_search_agent_model_id,
    region_name=region,
    temperature=0.3,
    top_p=0.8
)

print(f"✅ Bedrock model initialized: {prod_search_agent_model_id}")

# Define the system prompt for the AI shopping assistant
system_prompt = """
You are an AI shopping assistant that helps customers discover products and reviews. 
You have access to:
1. A knowledge base with comprehensive product information
2. MCP tools for retrieving detailed product reviews and ratings

When a customer asks about products:
1. First, search the knowledge base for relevant products using the search_products tool
2. If available and relevant, retrieve reviews for the products using MCP tools
3. Provide helpful recommendations based on the information gathered
4. Always format responses in a clear, customer-friendly manner
5. Include relevant product details like price, features, and availability when available

Guidelines:
- Be helpful, accurate, and informative
- Provide structured responses when possible
- If you cannot find specific information, clearly state this
- Always prioritize customer needs and preferences
- Suggest alternatives when the exact request cannot be fulfilled
- Include review summaries and ratings when available

Response Format:
- Start with a brief summary of findings
- List recommended products with key in the below JSON array format -
[
   { "product_id": "PROD-010", 
     "product_name": "Uniqlo Ultra Light Down Jacket", 
     "brand_name": "Uniqlo", 
     "category": "Clothing", 
     "subcategory": "Outerwear", 
     "gender": "Unisex", 
     "price": 69.90, 
     "sale_price": 49.90, 
     "size": ["XS", "S", "M", "L", "XL", "XXL"], 
     "color": ["Black", "Navy", "Red", "Olive", "Grey"], 
     "materials": ["100% Nylon", "Down filling", "Water-repellent coating"], 
     "season": "Fall/Winter",
     "product_reviews": "review of the current product"
     },
     ...
]   
- Include review highlights if available
"""

print("System prompt configured for AI shopping assistant")

# Define the main function that handles product search queries using the Knowledge Base and MCP tools.
def retrieve_product_details(input_query):
    """
    Main function to retrieve product details based on user query.
    
    Args:
        input_query (str): User's product search query
        
    Returns:
        str: Product search results in JSON format
    """
    print(f"Processing query: {input_query}")
    
    streamable_http_mcp_client = MCPClient(lambda:streamablehttp_client(agentcore_mcp_gatewayURL,headers={"Authorization": f"Bearer {anycomp_agcore_gw_cognito_accesstoken}"}))
    
    product_search_results = ''

    try:
        with streamable_http_mcp_client:
            mcp_tools = streamable_http_mcp_client.list_tools_sync()

            product_search_agent = Agent(
                tools=[retrieve, mcp_tools],
                model=_bedrock_model,
                system_prompt=_system_prompt
            )
            product_search_results = str(product_search_agent(input_query))
        
    except Exception as e:
        print(f"❌ Error during product search: {e}")
        return f"Error: {str(e)}"
    
    return product_search_results

print("✅ Product search function defined")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Print the provided argument')
    parser.add_argument('message', help='Ask any questions about AnyCompany products. Example usage: python <filename>.py "recommend me 3 jackets" ')
    
    # Parse arguments
    args = parser.parse_args()
    input_query = args.message
    
    # Test with a sample query for jackets
    print("=== Testing agent with jacket query ===")
    jacket_query = "I'm looking for a warm winter jacket under $200. What do you recommend?"
    jacket_response = retrieve_product_details(jacket_query)
    print(f"Query: {jacket_query}")
    print(f"Response: {jacket_response}")
    print()

    # Test with another query for summer clothing
    print("=== Testing with summer clothing query ===")
    summer_query = "What summer clothing options do you have for outdoor activities?"
    summer_response = retrieve_product_details(summer_query)
    print(f"Query: {summer_query}")
    print(f"Response: {summer_response}")
    print()

    # Test with a specific color request
    print("=== Testing with color-specific query ===")
    color_query = "Show me blue jackets under $100"
    color_response = retrieve_product_details(color_query)
    print(f"Query: {color_query}")
    print(f"Response: {color_response}")
    print()
    

if __name__ == "__main__":
    main()
