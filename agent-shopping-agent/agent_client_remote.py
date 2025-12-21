import json

import boto3
from boto3.session import Session

boto_session = Session()
region = boto_session.region_name

ssm_client = boto_session.client('ssm', region_name=region)


def invoke_agent():
    agent_arn = ssm_client.get_parameter(Name='/agent/runtime/agent_arn')
    agent_arn = agent_arn['Parameter']['Value']
    print(f"Agent ARN: {agent_arn}")

    agentcore_client = boto3.client(
        'bedrock-agentcore',
        region_name=region
    )

    boto3_response = agentcore_client.invoke_agent_runtime(
        agentRuntimeArn=agent_arn,
        qualifier="DEFAULT",
        payload=json.dumps(
            {"prompt": "Using the provided tools, answer the questions: What is 12+50? What is the weather?"})
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
        try:
            events = []
            for event in boto3_response.get("response", []):
                events.append(event)
        except Exception as e:
            events = [f"Error reading EventStream: {e}"]
        print(json.loads(events[0].decode("utf-8")))


if __name__ == "__main__":
    invoke_agent()
