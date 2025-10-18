from strands import Agent

agent = Agent(model="us.amazon.nova-premier-v1:0", system_prompt="You are a helpful assistant that provides concise answers. ")
print(agent("Tell me about agentic AI"))

