import numpy as np
import pandas as pd
import operator
from datetime import datetime, time, timezone
from typing import List, Dict, Union, Tuple, Any, Optional
from alpaca_trade_api.entity import BarSet
from pytrader.stock_frame import StockFrame


class Indicators:
    def __init__(self, stock_prices: StockFrame):
        self._stock_prices = stock_prices
        self._current_indicators = {}
        self._indicator_signals = {}

    def price_change(self) -> pd.DataFrame:
        my_locals = locals()
        del my_locals['self']

        col = 'price_change'
        self._current_indicators[col] = {}
        self._current_indicators[col]['args'] = my_locals
        self._current_indicators[col]['func'] = self.price_change

        self._stock_prices[col] = self._stock_prices['close'].transform(lambda x: x.diff())

    def rsi(self):
        pass

    def ema(self, period: int):
        locals_data = locals()
        del locals_data['self']
        column_name = 'ema'
        self._current_indicators[column_name] = {}
        self._current_indicators[column_name]['args'] = locals_data
        self._current_indicators[column_name]['func'] = self.ema

        self._stock_prices[column_name] = self._stock_prices['close'].transform(
            lambda x: x.ewm(span=period).mean()
        )

    def sma(self, period: int = 10):
        """
            Simple Moving Average

            Simple Moving Average (SMA) uses a sliding window
            to take the average over a set number of time periods.
            It is an equally weighted mean of the previous n data
        """
        my_locals = locals()
        del my_locals['self']
        col = "sma"
        self._current_indicators[col] = {}
        self._current_indicators[col]['args'] = my_locals
        self._current_indicators[col]['func'] = self.sma

        self._stock_prices[col] = self._stock_prices['close'].transform(
            lambda x: x.rolling(window=period).mean()
        )

    def cma(self, period: int = 10):
        my_locals = locals()
        del my_locals['self']
        col = 'cma'
        self._current_indicators[col] = {}
        self._current_indicators[col]['args'] = my_locals
        self._current_indicators[col]['func'] = self.cma
        self._stock_prices[col] = self._stock_prices['close'].transform(
            lambda x: x.rolling(window=period).mean()
        )

    def refresh(self):
        for indicator in self._current_indicators:
            indicator_args = self._current_indicators[indicator]['args']
            indicator_func = self._current_indicators[indicator]['func']
        # update the columns
            indicator_func(**indicator_args) # unpack dictionaries




