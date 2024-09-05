from dotenv import load_dotenv

load_dotenv()

import sys
from loguru import logger

from agent.agent import BuffetAgent


def init_logger():
    logger.remove(handler_id=None)
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time}</green> {level} <yellow>{file}</yellow> <level>{message}</level>",
    )


def main() -> int:
    init_logger()
    agent = BuffetAgent()
    logger.info("巴菲特来我大A赚钱了")
    agent.run_agent()
    return 0


if __name__ == "__main__":
    exit_code = main()
