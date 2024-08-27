from .agent import BuffetAgent


def main() -> int:
    agent = BuffetAgent()
    agent.run_agent()


if __name__ == "__main__":
    exit_code = main()
