from langchain_core.pydantic_v1 import BaseModel, Field


class WaitNextTradeDay(BaseModel):
    """Wait for the next trading date"""


class GetStockPriceOfToday(BaseModel):
    """Query the open/close stock price of today, input the stock code"""

    ts_code: str = Field(description="The stock you want to query")


class ListTheStocksToWatch(BaseModel):
    """list the stocks you are watching"""
