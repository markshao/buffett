from re import A
import pytest
from datetime import datetime, timedelta

from src.agent.tools.stmarket import TushareConfig, StockMarket


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
        curr_date = datetime.now().date() - timedelta(days=100)
        df = stm.query_daily_stock_price(ts_code=ts_code, curr_date=curr_date)
        print(df)
