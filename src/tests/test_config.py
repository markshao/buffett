import pytest
from src.agent.config import LlmConfig


def test_llm_config():
    llm_config = LlmConfig()
    assert llm_config.base_url == "https://api.deepseek.com"


def test_singleton():
    c1 = LlmConfig()
    c2 = LlmConfig()
    assert c1 is c2
