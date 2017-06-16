import pandas as pd
from zaifbot.bot_common.logger import logger
from pandas import DataFrame as DF
from talib import abstract as ab
from zaifbot.price.ohlc_prices import get_price_info
from .base import Indicator

_HIGH = 'high'
_LOW = 'low'
_CLOSE = 'close'
_TIME = 'time'

__all__ = ['MACD']


class MACD(Indicator):
    def __init__(self, currency_pair='btc_jpy', period='1d', short=12, long=26, signal=9):
        self._currency_pair = currency_pair
        self._period = period
        self._short = short
        self._long = long
        self._signal = signal

    def get_data(self, count=100, to_epoch_time=None):
        try:
            count_needed = count + self._long + self._signal - 2
            df = DF(get_price_info(self._currency_pair, self._period, count_needed, to_epoch_time))
            macd = ab.MACD(df, price=_CLOSE, fastperiod=self._short, slowperiod=self._long, signalperiod=self._signal)
            macd = pd.concat([df[_TIME], macd], axis=1).dropna()
            return {'success': 1, 'return': {'MACDs': macd.astype(object).to_dict(orient='records')}}
        except Exception as e:
            logger.error(e, exc_info=True)
            return {'success': 0, 'error': e}
