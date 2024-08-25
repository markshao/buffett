import pytest

from src.agent.tools.timemachine import TimeMachine


def test_current_date():
    tc = TimeMachine()
    print(tc.today)


def test_tomorrow():
    tc = TimeMachine()
    print(tc.today())
    tc.go_tomorrow()
    print(tc.today())
