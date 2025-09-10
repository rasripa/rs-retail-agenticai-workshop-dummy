from strands import Agent, tool
from strands_tools import retrieve
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig

# Create a boto client config with custom settings
_boto_config = BotocoreConfig(
    retries={"max_attempts": 3, "mode": "standard"},
    connect_timeout=5,
    read_timeout=60
)

# Create a Bedrock model instance
_bedrock_model = BedrockModel(
    model_id="us.amazon.nova-premier-v1:0",
    region_name="us-west-2",  # try with different regions than the default - make sure you enable model access in the region you use
    temperature=0.3,
    top_p=0.8,
    boto_client_config=_boto_config,
)

_system_prompt = """You are an \"AI shopping assistant\", that helps customers discover
  products. You use a Knowledge Base to search for products based on user preferences 
  and recommends them to the customers. You respond in the below JSON array format - 
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

"""

product_search_agent = Agent(
    tools=[retrieve],
    model=_bedrock_model,
    system_prompt=_system_prompt
)
