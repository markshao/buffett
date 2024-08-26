from datetime import date, datetime
from re import A
from numpy import isin
import tushare as ts


from ..utils import Singleton
from ..config import AbstractConfig


class TushareConfig(AbstractConfig):
    CONF_FILE_NAME = "tushare.yaml"
    CONF_KEYS = ("api_key",)


def date_to_tsschema(d: date):
    return d.strftime("%Y%m%d")


class StockMarket(metaclass=Singleton):
    def __init__(self) -> None:
        self._ts_config = TushareConfig()
        self._ts = ts.pro_api(self._ts_config.api_key)

    def query_daily_stock_price(self, ts_code, curr_date: date):
        # validate data
        assert isinstance(curr_date, date)
        assert ts_code

        end_date = datetime.now().date()
        df = self._ts.daily(
            ts_code=ts_code,
            start_date=date_to_tsschema(curr_date),
            end_date=date_to_tsschema(end_date),
        )
        return df
