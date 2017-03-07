from abc import abstractmethod
from zaifbot.bot_common.utils import get_current_last_price
from zaifbot.modules.processes.process_common import ProcessBase
from zaifbot.modules.processes.buy import get_auto_trade_dataset
from zaifbot.bollinger_bands import get_bollinger_bands
from time import time
from zaifbot.modules.dao.auto_trade import AutoTradeDao


class SellByPrice(ProcessBase):
    def get_name(self):
        return 'sell_by_price'

    def is_started(self):
        last_price = get_current_last_price()
        if last_price >= self.config.event.sell.target_value:
            return True
        return False

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class SellByBollingerBands(ProcessBase):
    def __init__(self, length, to_currency_amount, active=True, continue_=False, start_time=None):
        super().__init__()
        self._length = length
        self._continue = continue_
        self._sell_active = active
        self._to_currency_amount = to_currency_amount
        self._start_time = start_time
        if continue_ and active:
            self._auto_trade_record = []
            self._auto_trade = AutoTradeDao(self._start_time)
            auto_trade_dataset = get_auto_trade_dataset(
                self._start_time,
                self._sell_active,
                False,
                self._to_currency_amount,
                0.0
            )
            self._auto_trade.create_data(auto_trade_dataset)

    def get_name(self):
        return 'sell_by_bolinger_bands'

    def is_started(self):
        self._last_price = get_current_last_price()
        self._bollinger_bands = get_bollinger_bands(
            self.config.system.currency_pair,
            self.config.system.sleep_time,
            1,
            int(time()),
            self._length
        )
        if self._bollinger_bands['success'] == 0:
            return False
        if self._continue:
            self._auto_trade_record = self._auto_trade.get_record(self._start_time)
            self._sell_active = self._auto_trade_record[0].sell_active
        if self._sell_active \
                and self._last_price >= self._bollinger_bands['return']['bollinger_bands'][0]['sd2p']:
            print('\nsell')
            print('current price:' + str(self._last_price))
            print('bollinger band sd2p:' + str(self._bollinger_bands['return']['bollinger_bands'][0]['sd2p']))
            return True
        return False

    def execute(self):
        # implement trade order here
        if self._continue:
            auto_trade_dataset = get_auto_trade_dataset(
                self._start_time,
                False,
                True,
                0.0,
                0.0
            )
            self._auto_trade.create_data(auto_trade_dataset)
            return False
        else:
            return True
