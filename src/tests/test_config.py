import pytest
import os
from src.agent.config import LlmConfig


def test_llm_config():
    llm_config = LlmConfig()
    assert llm_config.base_url == "https://api.deepseek.com"


def test_singleton():
    c1 = LlmConfig()
    c2 = LlmConfig()
    assert c1 is c2


def test_os_env():
    c = LlmConfig()
    os.environ["llm.yaml.api_key"] = "test"
    assert c.api_key == "test"
