from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage


from .prompt import SYSTEM_PROMPT

from ..tools.func_call.call import FunctionCallEngine
from ..tools import StockMarket, TimeMachine
from ..llm import Llm


class AgentContext:
    def __init__(self, llm: Llm) -> None:
        self._system_prompt = SYSTEM_PROMPT

        self._stock_market = StockMarket()
        self._tm = TimeMachine()

        # tools
        self._llm = llm
        self.fc_engine = FunctionCallEngine()

    def initializ_ctx(self):
        self.fc_engine.register_obj(self._stock_market)
        self.fc_engine.register_obj(self._tm)

    def get_prompt_messages(self):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]

        return messages
