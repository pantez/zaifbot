ZaifBot
=======

:chart\_with\_upwards\_trend: algorithmic trading bot for zaif exchange

|Python version| |PyPI version| |License: MIT|

| ZaifBot is a Pythonic algorithmic trading library that run on `Zaif
  Exchange <https://zaif.jp/?lang=en>`__.
| It is developed by using Python 3.5.3 and tested in Python 3.4, 3.5,
  3.6.

Features
--------

-  Easy to use: Zaifbot is library for trading beginners, so designed
   simple.
-  Support all currency pairs dealt with `Zaif
   Exchange <https://zaif.jp/?lang=en>`__
-  Technical indicators like SMA, EMA, Bollinger Bands, RSI, ADX
-  You don't have to prepare market data. Zaifbot internal get data from
   `zaif
   API <http://techbureau-api-document.readthedocs.io/ja/latest/index.html>`__

| To get started with Zaifbot take a look at the
  `tutorial <https://github.com/techbureau/zaifbot/wiki/%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB1>`__
  and the `full
  documentation <https://github.com/techbureau/zaifbot/wiki>`__.
| `『ZaifBotドキュメント』 <https://github.com/techbureau/zaifbot/wiki>`__

**Note:** ZaifBot is unofficial library of `Tech Bureau,
Inc. <http://techbureau.jp/>`__ Please use it at your own risk.

Installation
------------

instaling with pip
~~~~~~~~~~~~~~~~~~

After activating an isolated Python environment, run

.. code:: bash

    $ pip install zaifbot

currently supported platforms includes:

-  Linux 64-bits
-  OSX 64-bits
-  Windows 64-bits

**Note:** if you use **OSX**, we assume
`homebrew <https://brew.sh/index.html>`__ is installed.

Setup
-----

After installing Zaifbot, run

.. code:: bash

    $ install_ta_lib

| TA-Lib is open-source library of technical analysis indicators that
  ZaifBot is depending on.
| This command install TA-Lib in your operating system.

then,

.. code:: bash

    $ init_database

| When ``init_database`` command is executed,
| ``db/zaifbot.db`` is created for SQLite and schema is migrated.
| Your Trade records will be saved in this file.

Quick Start
-----------

See our `getting started
tutorial <https://github.com/techbureau/zaifbot/wiki/%E3%83%81%E3%83%A5%E3%83%BC%E3%83%88%E3%83%AA%E3%82%A2%E3%83%AB1>`__

The following code implements a simple trading algorithm using zaifbot

.. code:: python

    from zaifbot.trade import Strategy
    from zaifbot.rules import Entry, Exit
    from zaifbot.config import set_keys
    from zaifbot.trade.tools import last_price

    # setting your Zaif API key
    set_keys(key='your_key', secret='your_secret')


    # creating rule to buy
    class BuyWhenCheap(Entry):
        def can_entry(self):
            if last_price(self._currency_pair.name) < 25000:
                return True
            return False

    # creating rule to exit
    class ExitWhenPriceGoUp(Exit):
        def can_exit(self, trade):
            # 'trade' has the entry information
            current_price = last_price(trade.currency_pair.name)
            if current_price > trade.entry_price + 5000:
                return True
            return False

    my_entry = BuyWhenCheap(currency_pair='btc_jpy',
                            amount=0.01,
                            action='bid')
    my_exit = ExitWhenPriceGoUp()

    # strategy is an unite of automated trading
    my_strategy = Strategy(entry_rule=my_entry,
                           exit_rule=my_exit)

    my_strategy.start(sec_wait=1)

Feedback
--------

If you have a question, or find a bug, feel free to open an issue.

Contributing
------------

| Any kind of contributions are welcome.
| Please contribute by following the steps below.

1. Fork and clone this repository to your computer
2. Run ``docker build -t zaifbot .`` to create development environment
3. Edit source code and make pull request to ``depelop`` branch

.. |Python version| image:: https://img.shields.io/badge/python-3.4%2C%203.5%2C%203.6-blue.svg
   :target: https://pypi.python.org/pypi/zaifbot
.. |PyPI version| image:: https://badge.fury.io/py/zaifbot.svg
   :target: https://badge.fury.io/py/zaifbot
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
