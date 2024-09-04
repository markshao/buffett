from pprint import pformat
from typing import Dict
from ...utils import Singleton
from .definition import ToolListDefinition, ToolDefinition


class FunctionCallEngine(metaclass=Singleton):
    _DEFAULT_CALLER_OBJ = []  # 暂时不需要初始化

    def __init__(self):
        self.__func_to_obj = dict()
        self.__initialized = False
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

    def all_registerd_functitoins(self):
        return self.__func_to_obj.keys()

    def tools_definitions(self) -> ToolListDefinition:
        return ToolListDefinition(list(self.__method_to_tool_def.values()))


# ignore just for testing?
__fc_engine = FunctionCallEngine()
