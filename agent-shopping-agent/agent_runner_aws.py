from bedrock_agentcore.runtime import BedrockAgentCoreApp

from agent import agent

app = BedrockAgentCoreApp()


@app.entrypoint
def strands_agent_bedrock(payload):
    user_input = payload.get("prompt")
    print("User input:", user_input)
    response = agent(user_input)
    return response.message['content'][0]['text']


if __name__ == "__main__":
    app.run()
