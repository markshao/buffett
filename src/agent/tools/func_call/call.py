from typing import Dict
from omegaconf import DictConfig
from loguru import logger

from agent.tools import StockMarket, TimeMachine
from agent.tools.func_call.definition import ToolDefinition, ToolListDefinition
from agent.utils import Singleton


class FunctionCallEngine(metaclass=Singleton):

    def __init__(self, config: DictConfig):
        self.__initialized = False
        self.__func_to_obj = dict()
        self.__method_to_tool_def: Dict[str, ToolDefinition] = dict()
        self._DEFAULT_CALLER_OBJ = [
            StockMarket(config.tushare),
            TimeMachine(config.timemachine),
        ]

    def initialize(self):
        if self.__initialized:
            return

        for obj in self._DEFAULT_CALLER_OBJ:
            self.register_obj(obj)
        self._initialized = True

    def register_obj(self, obj):
        methods = [
            func
            for func in dir(obj)
            if callable(getattr(obj, func))
            and not func.startswith("__")
            and not func.startswith("_")
        ]
        for m in methods:
            self.__func_to_obj[m] = obj
            method = getattr(obj, m)
            assert getattr(method, "_tool_def")
            self.__method_to_tool_def[m] = getattr(method, "_tool_def")

    def call_method_with_args(self, mname: str, args: dict):
        obj = self.__func_to_obj[mname]
        method = getattr(obj, mname)
        try:
            ret = method(**args)
            return ret
        except Exception as e:
            logger.error("funcation call with error: {}", e)
            return f"funcation call with error:{e}"

    def all_registerd_functitoins(self):
        return self.__func_to_obj.keys()

    def tools_definitions(self) -> ToolListDefinition:
        return ToolListDefinition(list(self.__method_to_tool_def.values()))
