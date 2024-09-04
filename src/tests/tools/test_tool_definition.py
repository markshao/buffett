from pprint import pprint
from agent.tools.func_call.definition import (
    ToolDefinition,
    ToolFunction,
    ToolListDefinition,
)


def test_tool_definition():
    functions = []
    for i in range(2):
        function = ToolFunction(name=f"func-{i}", description=f"desc-{i}")
        functions.append(function)

    tool_list_definition = ToolListDefinition(
        [ToolDefinition(function=func) for func in functions]
    )

    pprint("\n")
    pprint(tool_list_definition.json())
