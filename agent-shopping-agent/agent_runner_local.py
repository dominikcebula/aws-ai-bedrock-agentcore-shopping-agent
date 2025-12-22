import logging

from agent import agent

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def strands_agent_bedrock(user_input):
    response = agent(user_input)
    return response.message['content'][0]['text']


def run_interactive_mode():
    print("\nShopping Agent - Local Runner\n")
    print("Agent has access to product catalog and can create, list, update orders on user behalf.")
    print("Ask about available products and order creation for those products.\n")
    print("\nOptions:")
    print("  'exit' - Exit the program")

    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = strands_agent_bedrock(user_input)

            print(str(response))

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception:
            logger.exception("\nAn error occurred:")
            print("Please try a different request.")


if __name__ == "__main__":
    run_interactive_mode()
