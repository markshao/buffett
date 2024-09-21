from omegaconf import DictConfig
from ratelimit import limits, sleep_and_retry
from langchain_openai import ChatOpenAI


class Llm:
    def __init__(self, config: DictConfig) -> None:
        self._config = config
        self._llm = ChatOpenAI(
            model=self._config.model,
            api_key=self._config.api_key,
            base_url=self._config.base_url,
        )

    @sleep_and_retry
    @limits(calls=2, period=60)
    def invoke_with_tools(self, messages=[], tools=[]):
        llm_with_tools = self._llm.bind_tools(tools=tools)
        return llm_with_tools.invoke(messages)
