from dotenv import load_dotenv

load_dotenv()

import sys
from loguru import logger

from agent.agent import BuffetAgent


def init_logger():
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time}</green> <level>{message}</level>",
    )


def main() -> int:
    logger.info("start buffet agent")
    agent = BuffetAgent()
    agent.run_agent()
    return 0


if __name__ == "__main__":
    exit_code = main()
