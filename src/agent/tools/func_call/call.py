from typing import Dict

from loguru import logger

from agent.tools import StockMarket, TimeMachine
from agent.tools.func_call.definition import ToolDefinition, ToolListDefinition
from agent.utils import Singleton


class FunctionCallEngine(metaclass=Singleton):
    _DEFAULT_CALLER_OBJ = [StockMarket(), TimeMachine()]

    def __init__(self):
        self.__initialized = False
        self.__func_to_obj = dict()
        self.__method_to_tool_def: Dict[str, ToolDefinition] = dict()

    def initialize(self):
        if self.__initialized:
            return

        for obj in self.__class__._DEFAULT_CALLER_OBJ:
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
        ret = None
        try:
            ret = method(**args)
        except Exception as e:
            logger.error("funcation call error {}", e)
            return f"fail to call the function {e}"
        return ret

    def all_registerd_functitoins(self):
        return self.__func_to_obj.keys()

    def tools_definitions(self) -> ToolListDefinition:
        return ToolListDefinition(list(self.__method_to_tool_def.values()))


# ignore just for testing?
__fc_engine = FunctionCallEngine()
