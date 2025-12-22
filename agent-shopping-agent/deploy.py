from bedrock_agentcore_starter_toolkit import Runtime
from boto3.session import Session

boto_session = Session()
region = boto_session.region_name

agent_name = "agent_shopping_agent"

ssm_client = boto_session.client('ssm', region_name=region)
eb_client = boto_session.client('elasticbeanstalk', region_name=region)


def discover_microservice_urls():
    print("Discovering microservice URLs from Elastic Beanstalk...")

    products_url = get_elastic_beanstalk_url("microservice-products-catalog")
    print(f"Products Catalog URL: {products_url}")

    orders_url = get_elastic_beanstalk_url("microservice-orders")
    print(f"Orders URL: {orders_url}")

    return {
        "PRODUCTS_CATALOG_BASE_URL": products_url,
        "ORDERS_BASE_URL": orders_url
    }


def get_elastic_beanstalk_url(application_name: str) -> str:
    response = eb_client.describe_environments(
        ApplicationName=application_name,
        IncludeDeleted=False
    )

    environments = response.get('Environments', [])
    if not environments:
        raise ValueError(f"No active environment found for application: {application_name}")

    for env in environments:
        if env.get('Status') in ['Ready', 'Launching', 'Updating']:
            cname = env.get('CNAME')
            if cname:
                return f"http://{cname}"

    raise ValueError(f"No ready environment with CNAME found for application: {application_name}")


def configure_agentcore_runtime():
    print("Configuring AgentCore Runtime...")
    agentcore_runtime = Runtime()
    agentcore_runtime.configure(
        entrypoint="agent_runner_aws.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region=region,
        agent_name=agent_name
    )
    print("AgentCore Runtime configured successfully.")

    return agentcore_runtime


def launch_agentcore_runtime(agentcore_runtime, env_vars: dict):
    print("Launching Agent to AgentCore Runtime...")
    print("This may take several minutes...")
    print(f"Environment variables: {env_vars}")
    launch_result = agentcore_runtime.launch(env_vars=env_vars)
    print("Launch completed")
    print(f"Agent ARN: {launch_result.agent_arn}")
    print(f"Agent ID: {launch_result.agent_id}")

    return launch_result


def store_agent_arn(launch_result):
    ssm_client.put_parameter(
        Name='/agent/runtime/agent_arn',
        Value=launch_result.agent_arn,
        Type='String',
        Description='Agent ARN',
        Overwrite=True
    )
    print("✓ Agent ARN stored in Parameter Store")

    print("\nConfiguration stored successfully!")
    print(f"Agent ARN: {launch_result.agent_arn}")


def main():
    env_vars = discover_microservice_urls()
    agentcore_runtime = configure_agentcore_runtime()
    launch_result = launch_agentcore_runtime(agentcore_runtime, env_vars)
    store_agent_arn(launch_result)


if __name__ == "__main__":
    main()
