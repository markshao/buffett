import pytest

from agent.tools.timemachine import TimeMachine
from agent.context.context import AgentContext


def test_current_date(cfg):
    tc = TimeMachine(cfg.timemachine)
    print(tc.today)

