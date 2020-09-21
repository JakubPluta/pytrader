import numpy as np
import pandas as pd
import operator
from datetime import datetime, time, timezone
from typing import List, Dict, Union, Tuple, Any, Optional
from alpaca_trade_api.entity import BarSet
from pytrader.stock_frame import StockFrame
import btalib as bt
from ta import add_all_ta_features


class Indicators:
    def __init__(self, stock_prices: StockFrame):
        self._stock_prices = stock_prices
        self._current_indicators = {}
        self._indicator_signals = {}

    def calculate_price_changes(self):
        for frame in self._stock_prices.stock_frames:
            frame.data['changes'] = frame.data['close'].transform(lambda x: x.diff())

    @property
    def stock_prices(self):
        return self._stock_prices.stock_frames

    def macd(self):
        for frame in self._stock_prices.stock_frames:
            macd = bt.macd(frame.data).df
            frame.data['macd'] = macd

    def rsi(self):
        for frame in self._stock_prices.stock_frames:
            rsi = bt.rsi(frame.data).df
            frame.data['rsi'] = rsi

    def ema(self):
        for frame in self._stock_prices.stock_frames:
            ema = bt.rsi(frame.data).df
            frame.data['ema'] = ema

    def add_all_indicators(self):
        for frame in self._stock_prices:
            frame.data = add_all_ta_features(frame.data, 'open', 'high', 'low', 'close', 'volume')
            self._current_indicators[frame.symbol] = {}
            self._current_indicators[frame.symbol]['indicators'] = frame.data.iloc[:,6:]








