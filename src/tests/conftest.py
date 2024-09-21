from email.policy import default
from hydra import initialize, compose
from omegaconf import DictConfig
import pytest


def pytest_addoption(parser, pluginmanager):
    parser.addoption("--llm_api_key", action="store", default="")
    parser.addoption("--tushare_api_key", action="store", default="")


@pytest.fixture
def cfg(request) -> DictConfig:
    with initialize(version_base=None, config_path="../agent/conf"):
        cfg = compose(
            config_name="buffet",
            overrides=[
                f"llm_config.api_key={request.config.option.llm_api_key}",
                f"tushare.api_key={request.config.option.tushare_api_key}",
            ],
        )
        return cfg
