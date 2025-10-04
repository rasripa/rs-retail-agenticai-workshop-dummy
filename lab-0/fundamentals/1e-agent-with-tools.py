from strands import Agent, tool
from strands_tools import calculator, current_time, generate_image
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt


# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# [OPTIONAL STATEMENT] 
# Set the logging level to ERROR if the agent response is not readable with the DEBUG logs. 
# please switch back to DEBUG if you want to look at the detailed traces of the agent processing steps.

# logging.getLogger("strands").setLevel(logging.ERROR) # uncomment this statement to disable DEBUG logs and enable ERROR logs only.

# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool
agent = Agent(tools=[calculator, current_time, generate_image, letter_counter])


# Ask the agent a question that uses the available tools
message = """
I have 4 requests:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
4. Generate an image of a futuristic city with flying cars
"""

tools_agent_response = agent(message)
print(tools_agent_response)


## display the generated image. if you notice errors with the image display, check the image path ##

#Get image paths
folder_path = "output"
folder = Path(folder_path)
image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

for image_path in folder.iterdir():
    if image_path.is_file() and image_path.suffix.lower() in image_extensions:
        # Load and display
        print (image_path)
        img = Image.open(image_path)
        plt.imshow(img)
        plt.axis('off')
        plt.show()