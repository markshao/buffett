from datetime import date, datetime, timedelta
from typing import Optional

from loguru import logger
from workalendar.asia import China

from agent.context.context import AgentContext
from agent.config import AbstractConfig
from agent.tools.base import BaseTool
from agent.tools.func_call.definition import (
    ToolDefinition,
    ToolFunction,
    ToolParams,
    tool_def,
)

cal = China()


def is_working_day(d: date):
    return cal.is_working_day(d)


def next_working_day(curr_date: date) -> date:
    next_date = curr_date + timedelta(days=1)
    while not is_working_day(next_date):
        next_date = next_date + timedelta(days=1)
    return next_date


class TimeMachineConfig(AbstractConfig):
    CONF_FILE_NAME = "timemachine.yaml"
    CONF_KEYS = ("fallback_days",)


class TimeMachine(BaseTool):
    def __init__(self) -> None:
        self._config: AbstractConfig = TimeMachineConfig()
        self._curr_date: Optional[date] = None

        self.__set_curr_date()

    def __set_curr_date(self):
        now_date = datetime.now().date()
        self._curr_date = now_date - timedelta(days=int(self._config.fallback_days))
        if not is_working_day(self._curr_date):
            logger.info("curr date is not working day , time through")
            self._curr_date = next_working_day(self._curr_date)

    @tool_def(
        ToolDefinition(
            function=ToolFunction(
                name="today",
                description="get the date of today",
                parameters=ToolParams(
                    properties={},
                    required=[],
                ),
            )
        )
    )
    def today(self, ctx) -> str:
        if self._curr_date:
            return self._curr_date.strftime("%Y-%m-%d")
        else:
            raise AttributeError(f"self._curr_date is None")

    @tool_def(
        ToolDefinition(
            function=ToolFunction(
                name="go_tomorrow",
                description="wait for the next trade day",
                parameters=ToolParams(
                    properties={},
                    required=[],
                ),
            )
        )
    )
    def go_tomorrow(self, ctx: "AgentContext"):
        if self._curr_date:
            self._curr_date = next_working_day(self._curr_date)
