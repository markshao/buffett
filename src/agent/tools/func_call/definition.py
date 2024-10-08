from typing import List

from pydantic import BaseModel, Field, RootModel

# [
#     {
#         "type": "function",
#         "function": {
#             "name": "WaitNextTradeDay",
#             "description": "wait for the next trade day",
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#             },
#         },
#     },
# ]


class ToolParams(BaseModel):
    type: str = Field(default="object")
    properties: dict = Field(default={})
    required: List[str] = Field(default=[])


class ToolFunction(BaseModel):
    name: str = Field(description="Function Name")
    description: str = Field(description="Function Desc")
    parameters: ToolParams = Field(default=ToolParams())


class ToolDefinition(BaseModel):
    type: str = Field(default="function")
    function: ToolFunction = Field(description="function definition")


class ToolListDefinition(RootModel[List[ToolDefinition]]):
    pass


# decorator
def tool_def(tool_def: ToolDefinition):
    def deco(func):
        func._tool_def = tool_def
        return func

    return deco
