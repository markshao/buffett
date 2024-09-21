from datetime import date, datetime, timedelta
from typing import Optional
import time
from loguru import logger
from workalendar.asia import China

from agent.context.context import AgentContext
from agent.tools.base import BaseTool
from agent.tools.func_call.definition import (
    ToolDefinition,
    ToolFunction,
    ToolParams,
    tool_def,
)
from agent.utils import date_2_str

cal = China()


def is_working_day(d: date):
    return cal.is_working_day(d)


def next_working_day(curr_date: date) -> date:
    next_date = curr_date + timedelta(days=1)
    while not is_working_day(next_date):
        next_date = next_date + timedelta(days=1)
    return next_date


class TimeMachine(BaseTool):
    def __init__(self, config) -> None:
        self._config = config
        self._curr_date: Optional[date] = None

        self.__set_curr_date()

        # go_tomorrow_count
        self._count = 1

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
                name="next_trading_day",
                description="wait for the next trade day",
                parameters=ToolParams(
                    properties={},
                    required=[],
                ),
            )
        )
    )
    def next_trading_day(self, ctx: "AgentContext"):
        if self._curr_date:
            self._curr_date = next_working_day(self._curr_date)

            # fix me later, dont constant sleep
            time.sleep(10)
            # 保留最后一个 Message，这个是上次的 Response
            if self._count % 14 == 0:
                ctx.llm_logs = ctx.llm_logs[-1:]
                logger.info("clean history")
                self._count = 1
            else:
                self._count += 1

            return f"time passed away, now its the next trading date {date_2_str(self._curr_date)}"
        else:
            logger.error("self._curr_date is None , fail to wait for next day")
