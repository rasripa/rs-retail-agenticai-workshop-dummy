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

faq_agent = Agent(
    tools=[retrieve],
    model=_bedrock_model,
    system_prompt="You are a friendly agent that answers questions about AnyCompany's profile, retail policies, financial performance, annual reports, terms and conditions etc.",
)

