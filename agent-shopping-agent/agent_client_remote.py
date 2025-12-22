import json
import logging

import boto3
from boto3.session import Session

boto_session = Session()
region = boto_session.region_name

ssm_client = boto_session.client('ssm', region_name=region)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def run_interactive_mode():
    print("\nShopping Agent - Remote AWS Client\n")
    print("Agent has access to product catalog and can create, list, update orders on user behalf.")
    print("Ask about available products and order creation for those products.\n")
    print("\nOptions:")
    print("  'exit' - Exit the program")

    agent_arn = ssm_client.get_parameter(Name='/agent/runtime/agent_arn')
    agent_arn = agent_arn['Parameter']['Value']
    print(f"Agent ARN: {agent_arn}")

    agentcore_client = boto3.client('bedrock-agentcore', region_name=region)

    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            process_user_input(agent_arn, agentcore_client, user_input)
        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception:
            logger.exception("\nAn error occurred:")
            print("Please try a different request.")


def process_user_input(agent_arn, agentcore_client, user_input: str):
    boto3_response = agentcore_client.invoke_agent_runtime(
        agentRuntimeArn=agent_arn,
        qualifier="DEFAULT",
        payload=json.dumps(
            {"prompt": user_input})
    )
    if "text/event-stream" in boto3_response.get("contentType", ""):
        content = []
        for line in boto3_response["response"].iter_lines(chunk_size=1):
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    line = line[6:]
                    print(line)
                    content.append(line)
        print("\n".join(content))
    else:
        for event in boto3_response.get("response", []):
            print(f"{event.decode('utf-8').replace('\\n', '\n')}")


if __name__ == "__main__":
    run_interactive_mode()
