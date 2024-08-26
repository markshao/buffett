from datetime import date, datetime
from pandas.core.series import Series
import tushare as ts

from loguru import logger

from ..utils import Singleton, str_2_date
from ..config import AbstractConfig


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


class StockMarket(metaclass=Singleton):
    def __init__(self) -> None:
        self._ts_config = TushareConfig()
        self._ts = ts.pro_api(self._ts_config.api_key)
        self._ps = StockPriceStorage()

    def query_daily_stock_price(self, ts_code, curr_date: date) -> DayPrice:
        # validate data
        assert isinstance(curr_date, date)

        stock_price_dict = self._ps.get_stock_price_dict(ts_code)

        if stock_price_dict:
            if curr_date in stock_price_dict:
                return stock_price_dict[curr_date]
        else:
            self._ps.init_stock_price_dict(ts_code)
            stock_price_dict = self._ps.get_stock_price_dict(ts_code)

        # fetch latest data
        end_date = datetime.now().date()
        df = self._ts.daily(
            ts_code=ts_code,
            start_date=date_to_tsschema(curr_date),
            end_date=date_to_tsschema(end_date),
        )

        sorted_df = df.sort_values(by="trade_date", ascending=False)
        for i in range(len(sorted_df)):
            ser = sorted_df.iloc[i]
            stock_price_dict[str_2_date(ser.trade_date)] = (
                DayPrice.parse_from_data_frame(ser)
            )

        return stock_price_dict[curr_date]
