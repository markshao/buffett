import pytest
from datetime import datetime, timedelta

from agent.context.context import AgentContext
from agent.tools.stmarket import StockMarket, DayPrice
from agent.utils import date_2_str


@pytest.fixture
def stm(request, cfg) -> StockMarket:
    return StockMarket(cfg.tushare)


### Error due to the api not existed
# def test_realtime_snapshot(stm: StockMarket):
#     df = stm.ts_api.realtime_tick(ts_code="600000.SH")
#     print(df[0])

@pytest.mark.skip("need tushare apikey")
class TestStMarket:
    def test_query_stock_price(self, stm: StockMarket):
        ts_code = "000001.SZ"
        curr_date = datetime.now().date() - timedelta(days=10)
        dp = stm.query_daily_stock_price(
            ts_code=ts_code, curr_date=date_2_str(curr_date), ctx=AgentContext()
        )
        assert isinstance(dp, DayPrice)
        print("\n")
        print(dp)
        curr_date = curr_date + timedelta(days=7)
        dp = stm.query_daily_stock_price(
            ts_code=ts_code, curr_date=date_2_str(curr_date), ctx=AgentContext()
        )
        assert isinstance(dp, DayPrice)
        print(dp)
