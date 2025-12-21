import argparse

from agent import agent


def strands_agent_bedrock(user_input):
    response = agent(user_input)
    return response.message['content'][0]['text']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-user-input", type=str)
    args = parser.parse_args()
    response = strands_agent_bedrock(args.user_input)
