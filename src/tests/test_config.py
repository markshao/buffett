import pytest
from src.agent.config import LlmConfig


def test_llm_config():
    llm_config = LlmConfig()
    assert llm_config.base_url == "https://api.deepseek.com"
