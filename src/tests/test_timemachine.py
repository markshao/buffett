import pytest

from agent.tools.timemachine import TimeMachine
from agent.context.context import AgentContext


def test_current_date():
    tc = TimeMachine()
    print(tc.today)


def test_tomorrow():
    ctx = AgentContext()
    tc = TimeMachine()
    print(tc.today(ctx))
    tc.go_tomorrow(ctx)
    print(tc.today(ctx))
