from pathlib import Path

from bedrock_agentcore_starter_toolkit.operations.runtime import destroy_bedrock_agentcore
from boto3.session import Session

agent_name = "agent_strands_with_bedrock_model"

boto_session = Session()

region = boto_session.region_name

ssm_client = boto_session.client('ssm', region_name=region)


def cleanup():
    print("Cleaning up resources...")
    destroy_bedrock_agentcore(
        config_path=Path(".bedrock_agentcore.yaml"),
        agent_name=agent_name,
        delete_ecr_repo=True
    )

    ssm_client.delete_parameter(Name='/agent/runtime/agent_arn')

    print("Cleanup completed successfully!")


if __name__ == "__main__":
    cleanup()
