from abc import ABCMeta
import pandas as pd
from .indicator import Indicator


class _MA(Indicator, metaclass=ABCMeta):
    def __init__(self, currency_pair='btc_jpy', period='1d', length=25):
        super().__init__(currency_pair, period)
        self._length = self._bounded_length(length)

    def request_data(self, count=100, to_epoch_time=None):
        candlesticks_df = self._get_candlesticks_df(count, to_epoch_time)
        ma = self._exec_talib_func(candlesticks_df, timeperiod=self._length)
        formatted_ma = self._formatting(candlesticks_df['time'], ma)
        return formatted_ma

    def is_increasing(self):
        previous, last = self.request_data(count=2)
        return last[self.name] > previous[self.name]

    def is_decreasing(self):
        return not self.is_increasing()

    def _required_candlesticks_count(self, count):
        return self._bounded_count(count) + self._length - 1

    def _formatting(self, time_df, ma):
        ma = ma.rename(self.name).dropna()
        return pd.concat([time_df, ma], axis=1).dropna().astype(object).to_dict(orient='records')


class EMA(_MA):
    _NAME = 'ema'


class SMA(_MA):
    _NAME = 'sma'
