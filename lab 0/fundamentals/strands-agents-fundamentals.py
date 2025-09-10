from strands import Agent

def firstagent():

    # Create an agent with default settings
    agent = Agent()
    # Ask the agent a question
    response = agent("Tell me about agentic AI")
    print (response)


def main():
    # Step 1.a
    firstagent()



if __name__ == '__main__':
    main()