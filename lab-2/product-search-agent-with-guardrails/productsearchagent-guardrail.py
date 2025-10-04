import boto3
import argparse
from strands import Agent
from strands_tools import retrieve
from strands.models import BedrockModel

region = boto3.Session().region_name

# Define the system prompt for the AI shopping assistant
_system_prompt = """
You are an AI shopping assistant that helps customers discover products and reviews. 
You have access to:
1. A knowledge base with comprehensive product information

When a customer asks about products:
1. First, search the knowledge base for relevant products using the search_products tool
2. Provide helpful recommendations based on the information gathered
3. Always format responses in a clear, customer-friendly manner
4. Include relevant product details like price, features, and availability when available

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
     "season": "Fall/Winter"
     },
     ...
]
"""

# Create a Bedrock guardrail
bedrock_client = boto3.client('bedrock')
response = bedrock_client.create_guardrail(
    name='product-specific-restrictions',
    description='Prevents the model from providing recommendations on specific products.',
    topicPolicyConfig={
        'topicsConfig': [
            {
                'name': 'Product restrictions',
                'definition': 'Providing recommendations on product restricted by anycompany and not related to the products available in anycompany.',
                'examples': ['Competitor brands', 'Inappropriate or offensive clothing', 'fake','counterfeit'
                ],
                'type': 'DENY'
            }
        ]
    },
    contentPolicyConfig={
        'filtersConfig': [
            {
                'type': 'SEXUAL',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'VIOLENCE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'HATE',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'INSULTS',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'MISCONDUCT',
                'inputStrength': 'HIGH',
                'outputStrength': 'HIGH'
            },
            {
                'type': 'PROMPT_ATTACK',
                'inputStrength': 'HIGH',
                'outputStrength': 'NONE'
            }
        ]
    },
    wordPolicyConfig={
        'wordsConfig': [
            {'text': 'counterfeit'},
            {'text': 'fake'},
            {'text': 'sexy'},
            {'text': 'h&m'},
            {'text': 'nazi'},
            {'text': 'lolita'},
            {'text': 'dupe'}
        ],
        'managedWordListsConfig': [
            {
                'type': 'PROFANITY'
            }
        ]
    },
    blockedInputMessaging='Dear customer, I apologize, but I am not able to provide any recommendations related to your request. Please modify your input and try again.',
    blockedOutputsMessaging='Dear customer, I apologize, but I am not able to provide any recommendations related to your request. Please modify your input and try again.',
)

# Print the response to get the guardrail ID
print("Guardrail ID:", response.get('guardrailId'))
print("Guardrail ARN:", response.get('guardrailArn'))

guardrail_id = response.get('guardrailId')
guardrail_version = "DRAFT"  # Initial version is always 1


# Test function to check if input/output is blocked by guardrail
bedrock_runtime = boto3.client('bedrock-runtime')
def test_guardrail(text, source_type='INPUT'):
      response = bedrock_runtime.apply_guardrail(
          guardrailIdentifier=guardrail_id,
          guardrailVersion=guardrail_version,
          source=source_type,  # can be 'INPUT' or 'OUTPUT'
          content=[{"text": {"text": text}}]
      )

      # New response format uses different fields
      print(f"Action: {response.get('action')}")
      print(f"Action Reason: {response.get('actionReason', 'None')}")

      # Check if content was blocked
      is_blocked = response.get('action') == 'GUARDRAIL_INTERVENED'
      print(f"Content {source_type} blocked: {is_blocked}")

      if is_blocked:
          # Print topic policies that were triggered
          assessments = response.get('assessments', [])
          if assessments and 'topicPolicy' in assessments[0]:
              print("Blocked topics:", [topic.get('name') for topic in
          assessments[0]['topicPolicy'].get('topics', [])
                                       if topic.get('action') == 'BLOCKED'])

          # Print the modified output if available
          if 'outputs' in response and response['outputs']:
              print("Modified content:", response['outputs'][0].get('text', 'None'))

      return response

# Test input that will be blocked. This will be blocked since the input contains the word "lolita".
print("\nTesting input that will be blocked:")
test_guardrail("Can you recommend me a dress lolita style?")

# Test input that will be blocked. This will be blocked since the input contains the word "dupe".
print("\nTesting input that will be blocked:")
test_guardrail("Where can I find a dupe of Chanel jacket?")

# Test some safe input. This will not be blocked.
print("Testing safe input:")
test_guardrail("I am looking for a swimming suit for my holidays in Bali. What can you recommend? I want a 2 pieces")


# Create a Bedrock model with guardrail configuration
bedrock_model = BedrockModel(
    model_id="us.amazon.nova-premier-v1:0",
    region_name=region,
    guardrail_id=guardrail_id,
    guardrail_version=guardrail_version,
    guardrail_trace="enabled",
    temperature=0.3,
    top_p=0.8
)

# Create agent with the guardrail-protected model
product_search_agent_with_guardrail = Agent(
    system_prompt=_system_prompt,
    model=bedrock_model,
    tools=[retrieve]
)

# Helper function to test the agent and check for guardrail interventions
def test_agent_with_guardrail(prompt):
    print(f"\nUser: {prompt}")

    # Get agent response
    response = product_search_agent_with_guardrail(prompt)

    # Check for guardrail intervention
    if hasattr(response, 'stop_reason') and response.stop_reason == "guardrail_intervened":
        print("\n ⚠️ GUARDRAIL INTERVENED!")
        #print(f"Response: {response}")
    else:
        return response


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Print the provided argument')
    parser.add_argument('message', help='Ask any questions about AnyCompany products. Example usage: python <filename>.py "recommend me 3 jackets" ')
    
    # Parse arguments
    args = parser.parse_args()
    input_query = args.message
    
    # Test with a safe question 
    test_agent_with_guardrail("What colors are available for pants?")

    # Test with a question that asks about hate recommendation. This will get blocked.
    test_agent_with_guardrail("Find me a t-shirt with the nazi symbol on it")

if __name__ == "__main__":
    main()
