import pandas as pd
from typing import List, Dict
from pandas.core.groupby import DataFrameGroupBy
from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    data: pd.DataFrame

    def __getitem__(self, symbol):
        return self.symbol


class StockFrame:
    def __init__(self, data: List[Dict] = None):
        """
        :param data: It's a list of dictionaries that comes from alpaca_trade_api.get_barset()
        sample data:
            [{ "FB" : Bar({ 'c': 3024.155, 'h': 3027.255, 'l': 3017.67, 'o': 3018.93, 't': 1596121200, 'v': 3171})}]
        """
        self._data = data
        self._stock_frames = self.create_stock_frames()

    def __getitem__(self, key):
        return getattr(self._stock_frames, key)

    def __setitem__(self, key, value):
        self._stock_frames[key] = value

    def create_stock_frames(self):
        return [Stock(symbol, data.df) for symbol, data in self._data.items()]

    @property
    def stock_frames(self):
        return self._stock_frames

    @property
    def symbols(self):
        return [frame.symbol for frame in self._stock_frames]

    @property
    def data_frames(self):
        return [frame.data for frame in self._stock_frames]












