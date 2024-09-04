import pytest
from datetime import datetime, timedelta

from agent.tools.stmarket import TushareConfig, StockMarket, DayPrice


def test_tushareconfig():
    tu_config = TushareConfig()
    print(tu_config.api_key)
    assert tu_config.api_key


@pytest.fixture
def stm(request) -> StockMarket:
    return StockMarket()


class TestStMarket:
    def test_query_stock_price(self, stm: StockMarket):
        ts_code = "000001.SZ"
        curr_date = datetime.now().date() - timedelta(days=10)
        dp = stm.query_daily_stock_price(ts_code=ts_code, curr_date=curr_date)
        assert isinstance(dp, DayPrice)
        print("\n")
        print(dp)
        curr_date = curr_date + timedelta(days=7)
        dp = stm.query_daily_stock_price(ts_code=ts_code, curr_date=curr_date)
        assert isinstance(dp, DayPrice)
        print(dp)
