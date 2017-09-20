import datetime
import os

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from zaifbot.config.db import Engine


Base = declarative_base()


class Trades(Base):
    __tablename__ = 'trades'
    id_ = Column('id_', Integer, primary_key=True, autoincrement=True)
    currency_pair = Column('currency_pair', String, nullable=False)
    amount = Column('amount', Float, nullable=False)
    action = Column('action', String, nullable=False)
    entry_price = Column('entry_price', Float, nullable=False)
    entry_datetime = Column('entry_datetime', DateTime, default=datetime.datetime.now(), nullable=False)
    exit_price = Column('exit_price', Float)
    exit_datetime = Column('exit_datetime', DateTime)
    strategy_name = Column('strategy_name', String, nullable=True)
    process_id = Column('process_id', String, nullable=True)
    profit = Column('profit', Float)
    closed = Column('closed', Boolean, default=False, nullable=False)


class CandleSticks(Base):
    __tablename__ = 'candle_sticks'
    time = Column('time', Integer, primary_key=True)
    currency_pair = Column('currency_pair', String, primary_key=True)
    period = Column('period', String, primary_key=True)
    open = Column('open', Float, nullable=False)
    high = Column('high', Float, nullable=False)
    low = Column('low', Float, nullable=False)
    close = Column('close', Float, nullable=False)
    average = Column('average', Float, nullable=False)
    volume = Column('volume', Float, nullable=False)
    closed = Column('closed', Boolean, nullable=False)


def init_database():
    engine = Engine
    try:
        Base.metadata.create_all(engine, checkfirst=False)
        print('Database was created, successfully')
    except OperationalError:
        print('Database already exists')


def clear_database():
    engine = Engine
    if not engine.dialect.has_table(engine, 'Trades'):
        print("you haven't created db yet, run init_database")
        return
    answer = input('Really want to clear db? All trade data will lost [y/n]')
    if answer in ('y', 'yes'):
        Base.metadata.drop_all(engine)
        print('Database was deleted, successfully')
        return True
    print('canceled')
    return False


def refresh_database():
    if clear_database():
        init_database()
