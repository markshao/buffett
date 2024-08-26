from datetime import date, datetime
from re import A
from pandas.core.series import Series
import tushare as ts


from ..utils import Singleton
from ..config import AbstractConfig


class TushareConfig(AbstractConfig):
    CONF_FILE_NAME = "tushare.yaml"
    CONF_KEYS = ("api_key",)


def date_to_tsschema(d: date):
    return d.strftime("%Y%m%d")


class DayPrice:
    def __init__(self, high, low, open, close) -> None:
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
        return cls(open=_open, close=_close, high=_high, low=_low)


class StockPriceStorage:
    def __init__(self):
        self._stock_daily_price: dict[str, dict[date, DayPrice]] = dict()

    def get_stock_price_dict(self, ts_code: str):
        return self._stock_daily_price.get(ts_code, dict())


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
