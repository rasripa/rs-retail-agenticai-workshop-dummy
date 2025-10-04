import os
import boto3
from strands import Agent, tool
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig

# Import the FAQAgent from the local python in lab 4. This has the code that we saw in the FAQ Agents lab.
from FAQAgent import faq_agent

# Import Product Search and Inventory Agents from local python files.
from ProductSearchAgent import product_search_agent
from InventoryAgent import inventory_agent

region = boto3.Session().region_name
print(f"Using AWS region: {region}")

# Initialize SSM client
ssm_client = boto3.client('ssm', region_name=region)


###############################
# Set the Knowledge Base Id of the FAQ Bedrock Knowledge Base
faq_kb_id = "INSERT HERE"
print(f"faq_kb_id variable: {faq_kb_id}")
###############################

# Get the Knowledge Base Id of the Product Search Knowledge Base from SSM parameter store
product_search_kb_id = ssm_client.get_parameter(Name="product_search_kb_id")['Parameter']['Value']
print(f"product_search_kb_id variable: {product_search_kb_id}")

# Create a boto client config with custom settings
boto_config = BotocoreConfig(
    retries={"max_attempts": 3, "mode": "standard"},
    connect_timeout=5,
    read_timeout=60
)

# Create a Bedrock model instance
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-premier-v1:0",
    region_name=region,
    temperature=0.3,
    top_p=0.8,
    boto_client_config=boto_config,
)

@tool
def faq_agent_tool(query: str) -> str:
    """
    Answers questions about AnyCompany.
    
    Use this tool when you need to find answers to general questions about the
    policies, procedures, or common inquiries of AnyCompany.

    Args:
        query: The search question. (String)
    
    Returns:
        The answer to the question (String)

    """
    print("Fetching from FAQ Knowledge Base")
    response = faq_agent(f"Use the knowledge base id {faq_kb_id}. {query}")
    print(f"The response from FAQ Agent is {response}")
    return response


@tool
def product_search_agent_tool(query: str) -> str:
    """ 
    Discovers products for customers based on their requirements.

    Use this tool when you need to discover some products based
    on the requirements of the customer.

    This tool uses the Product Search Agent to find products.

    Example response:
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
       "season": "Fall/Winter" 
       },
       ...
    ]  

    Notes:
        - This tool only searches the products and does not provide
          inventory or availability information

    Args:
        query: The search requirements from the customer

    Returns:
        A list of matching product records, each containing:
        - id: Unique product identifier (string)
        - product_name: Product name
        - brand_name: Brand name
        - category: Category of the product
        - subcategory: Sub category
        - gender: Gender that the product applies to
        - price: Price
        - sale_price: Sales price
        - size: Available sizes as an array
        - color: Available colors as an array
        - materials: Materials
        - season: Season
    """
    print("Fetching from Product Search Knowledge Base using the query " + query)

    kbRes = product_search_agent(f"Use the knowledge base id {product_search_kb_id}. {query}")

    print(f"Products fetched from KB are : {kbRes}")
    return kbRes


@tool
def inventory_agent_tool(query: str) -> str:
    """ 
    Checks the inventory of products.

    Use this tool if you want to check if a product is in stock or not.

    This tool uses the Inventory Agent to find out if the product
    is in stock or not.

    Example response:
        {
            "product_id" : PRODUCT_ID,
            "in_stock": IN_STOCK_VALUE
        }
    
    Args:
        query: The product Id (String
    
    Returns:
        A JSON containing the fields:
        - product_id: Unique product identifier (string)
        - in_stock: "yes" or "no" indicating if the product is in stock or not.

    """
    print("Fetching from Inventory Agent with the query " + query)
    result = inventory_agent(query)
    print(f"Result from inventory_agent_tool is \" {result} \"")
    print("----------------------------")
    return result

# Search Orchestrator
ORCHESTRATOR_SYSTEM_PROMPT = """You are the Search Orchestrator Agent, a sophisticated AI coordinator 
responsible for managing and directing queries to three specialized collaborator agents: the FAQ Agent, 
the Product Search Agent, and the Inventory Agent. Your primary role is to efficiently handle user 
inquiries by determining which agent(s) to engage and in what order.

Your key responsibilities include:
1. Analyze incoming user queries to understand their intent and requirements.
2. Decide which tool(s) to consult based on the nature of the query:
   - FAQ Agent Tool: For general questions about policies, procedures, or common inquiries. This tool does 
                     not have product or product availability related information.
   - Product Search Agent Tool: For queries related to finding specific products or product categories.
   - Inventory Agent Tool: For questions about stock levels and availability.
3. Determine the optimal sequence for consulting these tools if multiple tools are needed.
4. Formulate clear, concise sub-queries for each relevant tool.
5. Collect and synthesize responses from the collaborator tools.
6. Generate a comprehensive, coherent response for the user based on the information gathered.

Note:
1. Fetch product availability information only when explicitly asked by the customer. 
2. FAQ Agent Tool does not have product or product availability related information.

Remember, your goal is to provide accurate, helpful, and efficient responses to user queries by 
leveraging the specialized knowledge of each collaborator tool. Always strive for clarity, 
conciseness, and relevance in your communications with both users and collaborator tools.
"""

# Create the orchestrator agent with the collaborator Agents as tools.
orchestrator = Agent(
    system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
    tools=[faq_agent_tool, product_search_agent_tool, inventory_agent_tool],
    model=bedrock_model
)

result1 = orchestrator("What is the returns policy of AnyCompany?")
print(result1)

result2 = orchestrator("Product recommendations for clothes")
print(result2)

result3 = orchestrator("Hello, I am going to attend a cocktail party, and would like some suggestions for smart casual jacket. What can you recommend me? Also check if that's in inventory.")
print(result3)