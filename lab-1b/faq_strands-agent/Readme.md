# Creating Strands Agent with a Single Knowledge Base

In this Lab, we will create a [Strands agent](https://strandsagents.com/) and integrate it with [Amazon Bedrock Knowledge Bases](https://aws.amazon.com/bedrock/knowledge-bases/). With this integration, the Agent will be able to respond to user queries about AnyCompany by finding answers from the Knowledge Base.

![Agents with Knowledge Bases for Amazon Bedrock](FAQ-agent-v2.png)


# Running the code
View the code `faq_strands_agent.py`. 

Modify the code and set the Knowledge Base Id of the FAQ Bedrock Knowledge Base created in Lab 1a. 

`os.environ["KNOWLEDGE_BASE_ID"] = '<KNOWLEDGE_BASE-id>'`

Finally run the code using -

```
python faq_strands_agent.py
```