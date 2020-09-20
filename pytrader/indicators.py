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

    def calculate_price_changes(self):
        for frame in self._stock_prices.stock_frames:
            frame.data['changes'] = frame.data['close'].transform(lambda x: x.diff())

    @property
    def stock_prices(self):
        return self._stock_prices.stock_frames

    def rsi(self, period: int = 14):
        for frame in self._stock_prices.stock_frames:
            if 'changes' not in frame.data:
                self.calculate_price_changes()

            frame.data['up_day'] = frame.data['changes'].transform(lambda x: np.where(x >= 0, x, 0))
            frame.data['down_day'] = frame.data['changes'].transform(lambda x: np.where(x < 0, x.abs(), 0))
            frame.data['ewma_up'] = frame.data['up_day'].transform(lambda x: x.ewm(span=period).mean() )# rolling average)
            frame.data['ewma_down'] = frame.data['down_day'].transform(lambda x: x.ewm(span=period).mean() )# rolling average)

            rsi = frame.data['ewma_up'] / frame.data['ewma_down']
            relative_strength_idx = 100.0 - (100.0 / (1.0 + rsi))
            frame.data['rsi'] = np.where(relative_strength_idx == 0, 100, relative_strength_idx)
            frame.data.drop(
                labels=['ewma_up', 'ewma_down', 'down_day', 'up_day', 'changes'], axis=1, inplace=True
            )

    def ema(self, period: int = 10):
        for frame in self._stock_prices.stock_frames:
            frame.data[f'ema_{str(period)}'] = frame.data['close'].transform(lambda x: x.ewm(span=period).mean())

    def sma(self, period: int = 10):
        """
            Simple Moving Average

            Simple Moving Average (SMA) uses a sliding window
            to take the average over a set number of time periods.
            It is an equally weighted mean of the previous n data
        """
        for frame in self._stock_prices.stock_frames:
            frame.data[f'sma_{str(period)}'] = frame.data['close'].transform(lambda x: x.rolling(window=period).mean()
        )





