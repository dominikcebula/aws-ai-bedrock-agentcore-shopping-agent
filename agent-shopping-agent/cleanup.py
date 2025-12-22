import os
from pathlib import Path

from bedrock_agentcore_starter_toolkit.operations.runtime import destroy_bedrock_agentcore
from boto3.session import Session

agent_name = "agent_shopping_agent"

boto_session = Session()

region = boto_session.region_name

ssm_client = boto_session.client('ssm', region_name=region)


def cleanup():
    print("🧹 Cleaning up resources...")

    cleanup_bedrock_agentcore_runtime()
    cleanup_ssm_parameter()

    print("✅ Cleanup completed successfully!")


def cleanup_bedrock_agentcore_runtime():
    print("🗑️  Deleting Bedrock AgentCore resources...")
    if os.path.exists(".bedrock_agentcore.yaml"):
        destroy_bedrock_agentcore(
            config_path=Path(".bedrock_agentcore.yaml"),
            agent_name=agent_name,
            delete_ecr_repo=True
        )
        print("✅ Bedrock AgentCore resources deleted.")
    else:
        print("⚠️  No Bedrock AgentCore configuration file found. Skipping Bedrock AgentCore cleanup.")


def cleanup_ssm_parameter():
    try:
        print("🗑️  Deleting SSM parameter for agent ARN...")
        ssm_client.delete_parameter(Name='/agent/runtime/agent_arn')
        print("✅ SSM parameter deleted.")
    except ssm_client.exceptions.ParameterNotFound:
        print("⚠️  SSM parameter not found. Skipping SSM cleanup.")


if __name__ == "__main__":
    cleanup()
