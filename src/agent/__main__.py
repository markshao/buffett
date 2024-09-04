from dotenv import load_dotenv

load_dotenv()
from agent.agent import BuffetAgent


def main() -> int:
    agent = BuffetAgent()
    agent.run_agent()
    return 0


if __name__ == "__main__":
    exit_code = main()
