import os
import boto3
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import use_aws

region = boto3.Session().region_name

# Create a Bedrock model instance
_bedrock_model = BedrockModel(
    model_id="us.amazon.nova-premier-v1:0",
    region_name=region,
    temperature=0.3,
    top_p=0.8
)


aws_agent = Agent(tools=[use_aws])

@tool
def get_product(product_id: str):
    """
    Use this tool when you need to get the details of a product to 
    see if that's available in stock or not.

    Args:
        product_id: The id of the product

    """
    print(f"Getting product from Dynamodb with the input {product_id}")

    get_item_result = aws_agent.tool.use_aws(
        service_name="dynamodb",
        operation_name="get_item",
        parameters={
            "TableName": "anycompany_product_inventory",
            "Key":{
                "product_id": {
                    "S": product_id
            }
            }
            },
        region=aws_region,
        label="Get One Item"
    )
    return get_item_result


_system_prompt = """
You are an Agent that checks if a product is available in the inventory.
Return output in the below JSON format. Do not include any other text.
{
    "product_id" : PRODUCT_ID,
    "in_stock": IN_STOCK_VALUE
}

where IN_STOCK_VALUE = "yes" if quantity_available is > 0 and "no" otherwise.
"""

# Register the tool with the agent
inventory_agent = Agent(
    model=_bedrock_model,
    tools=[get_product],
    system_prompt=_system_prompt
)

product_agent_response = inventory_agent("PROD-024?")
print(f"------------The output is {product_agent_response}")