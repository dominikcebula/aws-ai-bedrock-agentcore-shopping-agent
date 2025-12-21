from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator  # Import the calculator tool


@tool
def weather():
    """ Get weather """
    return "sunny"


model_id = "eu.amazon.nova-micro-v1:0"
model = BedrockModel(
    model_id=model_id,
)

agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)
