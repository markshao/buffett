import pytest
from agent.tools.func_call.call import FunctionCallEngine


@pytest.fixture
def fce(request, cfg) -> FunctionCallEngine:
    _fce = FunctionCallEngine(cfg)
    _fce.initialize()
    return _fce


# def test_function_call_register(fce):
#     fce.initialize()
#     assert len(fce.all_registerd_functitoins()) > 0


def test_tool_list_definition(fce):
    # fce.initialize()
    print("\n")
    print(fce.tools_definitions().json())
