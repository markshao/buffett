import pytest
from agent.tools.func_call.call import FunctionCallEngine


@pytest.fixture
def fce(request) -> FunctionCallEngine:
    _fce = FunctionCallEngine()
    _fce.initialize()
    return _fce


# def test_function_call_register(fce):
#     fce.initialize()
#     assert len(fce.all_registerd_functitoins()) > 0


def test_tool_list_definition(fce):
    # fce.initialize()
    print("\n")
    print(fce.tools_definitions().json())
