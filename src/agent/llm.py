from openai import OpenAI
from .config import LlmConfig
from .tools import TOOLS


class LlmClient:
    def __init__(self) -> None:
        self._config = LlmConfig()
        self._client = OpenAI(
            api_key=self._config.api_key, base_url=self._config.base_url
        )

    def request_llm(self, messages):
        resp = self._client.chat.completions.create(
            model="deepseek-coder", messages=messages, tools=TOOLS
        )
        return resp
