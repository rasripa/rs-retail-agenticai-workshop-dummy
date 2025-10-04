import os
import boto3
from strands import Agent
from strands_tools import retrieve
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig

region = boto3.Session().region_name

##################################
# Modify the below line to set the FAQ Knowledge Base Id
os.environ["KNOWLEDGE_BASE_ID"] = ''
##################################

os.environ["AWS_REGION"] = "us-west-2" #Change if needed
os.environ["MIN_SCORE"] = "0.4"

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

# Create the Agent. Pass the "retrieve" tool in the tools list.
faq_agent = Agent(
    tools=[retrieve],
    model=bedrock_model,
    system_prompt="You are a friendly agent that answers questions about AnyCompany's profile, retail policies, financial performance, annual reports, terms and conditions etc.",
)

result1 = faq_agent("What is the returns policy of AnyCompany?")
print(result1)

result2 = faq_agent("When was AnyCompany established?")
print(result2)

result3 = faq_agent("What is your contact center phone number?")
print(result3)