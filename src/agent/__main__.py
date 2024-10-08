import hydra
from omegaconf import DictConfig

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


@hydra.main(version_base=None, config_path="conf", config_name="buffet")
def main(cfg: DictConfig) -> int:
    init_logger()
    agent = BuffetAgent(cfg)
    agent.run_agent()
    return 0


if __name__ == "__main__":
    exit_code = main()
