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

    def ema(self):
        pass

    def sma(self, period: int = 10):
        """
            Simple Moving Average

            Simple Moving Average (SMA) uses a sliding window
            to take the average over a set number of time periods.
            It is an equally weighted mean of the previous n data
        """
        #self._current_indicators['']

        pass

    def cma(self, period: int = 10):
        pass


