from datetime import date, datetime

import tushare as ts
from tushare.pro.client import DataApi
from pandas.core.series import Series

from agent.config import AbstractConfig
from agent.context.context import AgentContext
from agent.tools.base import BaseTool
from agent.tools.func_call.definition import (
    ToolDefinition,
    ToolFunction,
    ToolParams,
    tool_def,
)
from agent.utils import str_2_date


class TushareConfig(AbstractConfig):
    CONF_FILE_NAME = "tushare.yaml"
    CONF_KEYS = ("api_key",)


def date_to_tsschema(d: date):
    return d.strftime("%Y%m%d")


class DayPrice:
    def __init__(self, ts_code, trade_date, high, low, open, close) -> None:
        self.ts_code: str = ts_code if ts_code else ""
        self.trade_date: str = trade_date if trade_date else "00000000"
        self.high: float = high if high else 0.0
        self.low: float = low if low else 0.0
        self.open: float = open if open else 0.0
        self.close: float = close if close else 0.0

    @classmethod
    def parse_from_data_frame(cls, ser: Series):
        _open = float(ser.open)
        _close = float(ser.close)
        _high = float(ser.high)
        _low = float(ser.low)
        return cls(
            ts_code=ser.ts_code,
            trade_date=ser.trade_date,
            open=_open,
            close=_close,
            high=_high,
            low=_low,
        )

    def __str__(self) -> str:
        return f"股票代码={self.ts_code}, 交易日期={self.trade_date},high={self.high}, low={self.low}, open={self.open}, close={self.close}"


class StockPriceStorage:
    def __init__(self):
        self._stock_daily_price: dict[str, dict[date, DayPrice]] = dict()

    def get_stock_price_dict(self, ts_code: str):
        return self._stock_daily_price.get(ts_code, dict())

    def init_stock_price_dict(self, ts_code: str):
        self._stock_daily_price[ts_code] = dict()


class StockMarket(BaseTool):
    def __init__(self) -> None:
        self._ts_config = TushareConfig()
        self._ts = ts.pro_api(self._ts_config.api_key)
        self._ps = StockPriceStorage()

    @property
    def ts_api(self) -> DataApi:
        return self._ts

    @tool_def(
        ToolDefinition(
            function=ToolFunction(
                name="query_daily_stock_price",
                description="query the daily stock price by ts_code and date of today",
                parameters=ToolParams(
                    properties={
                        "ts_code": {
                            "type": "string",
                            "description": "the code of stock, pick it from interested list",
                        },
                        "curr_date": {
                            "type": "string",
                            "description": "the date of today , in format 2024-1-1",
                        },
                    },
                    required=["ts_code", "curr_date"],
                ),
            )
        )
    )
    def query_daily_stock_price(
        self, ts_code, curr_date: str, ctx: AgentContext
    ) -> DayPrice:
        # validate data
        dcurr_date = str_2_date(curr_date)
        stock_price_dict = self._ps.get_stock_price_dict(ts_code)

        if stock_price_dict:
            if curr_date in stock_price_dict:
                return stock_price_dict[dcurr_date]
        else:
            self._ps.init_stock_price_dict(ts_code)
            stock_price_dict = self._ps.get_stock_price_dict(ts_code)

        # fetch latest data
        end_date = datetime.now().date()
        df = self._ts.daily(
            ts_code=ts_code,
            start_date=date_to_tsschema(dcurr_date),
            end_date=date_to_tsschema(end_date),
        )

        sorted_df = df.sort_values(by="trade_date", ascending=False)
        for i in range(len(sorted_df)):
            ser = sorted_df.iloc[i]
            stock_price_dict[str_2_date(ser.trade_date)] = (
                DayPrice.parse_from_data_frame(ser)
            )

        return stock_price_dict[dcurr_date]

    @tool_def(
        ToolDefinition(
            function=ToolFunction(
                name="buy_stock",
                description="bid the price and volume for the target stock",
                parameters=ToolParams(
                    properties={
                        "ts_code": {
                            "type": "string",
                            "description": "the code of stock which you want to bid",
                        },
                        "price": {
                            "type": "number",
                            "description": "bid price for the stock, in format 10.00",
                        },
                        "volume": {
                            "type": "integer",
                            "description": "volume of the stock you want to buy , should using integer",
                        },
                    },
                    required=["ts_code", "price", "volume"],
                ),
            )
        )
    )
    def buy_stock(self, ts_code, price, volume, ctx: AgentContext) -> str:
        # FIXME 这里没校验价格啥的, 另外如果持续购买也有bug
        _price = float(price)
        _volume = int(volume)
        _total_expense = float(_price * _volume)
        if _total_expense > ctx.stockActCtx.total_available_money:
            return "Fail to make the deal, you dont have enough money"
        # update ctx
        ctx.stockActCtx.total_available_money = (
            ctx.stockActCtx.total_available_money - _total_expense
        )
        ctx.stockActCtx.stock_holding[ts_code] = {"price": _price, "volume": _volume}
        return "Successfully make the deal"

    @tool_def(
        ToolDefinition(
            function=ToolFunction(
                name="sell_stock",
                description="bid the price and volume for the target stock",
                parameters=ToolParams(
                    properties={
                        "ts_code": {
                            "type": "string",
                            "description": "the code of stock which you want to bid",
                        },
                        "price": {
                            "type": "number",
                            "description": "the price you want to sell the stock, in format 10.00",
                        },
                        "volume": {
                            "type": "integer",
                            "description": "the volume you want to sell, should using integer and should less than the amount you hold",
                        },
                    },
                    required=["ts_code", "price", "volume"],
                ),
            )
        )
    )
    def sell_stock(self, ts_code, price, volume, ctx: AgentContext) -> str:
        # FIXME 这里没校验价格啥的
        _price = float(price)
        _volume = int(volume)
        _total_revenue = float(_price * _volume)
        if _volume > ctx.stockActCtx.stock_holding[ts_code]["volume"]:
            return "Fail to make the deal, you dont have enough stock"
        # update ctx
        ctx.stockActCtx.total_available_money = (
            ctx.stockActCtx.total_available_money + _total_revenue
        )
        ctx.stockActCtx.stock_holding[ts_code]["volume"] = (
            ctx.stockActCtx.stock_holding[ts_code]["volume"] - _volume
        )
        if ctx.stockActCtx.stock_holding[ts_code]["volume"] == 0:
            del ctx.stockActCtx.stock_holding[ts_code]
        return "Successfully make the deal"
