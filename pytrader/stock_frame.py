import pandas as pd
from typing import List, Dict
from pandas.core.groupby import DataFrameGroupBy


class StockFrame:

    def __init__(self, data: List[Dict] = None):
        self._data = data
        self._frame = self.create_stock_frame()
        self._symbols_groups = None
        self._symbol_rolling_groups = None

    def __getitem__(self, key):
        return getattr(self._frame, key)

    def __setitem__(self, key, value):
        self._frame[key] = value

    def create_stock_frame(self):
        pre_list = []
        for key, value in self._data.items():
            frame = value.df
            frame['symbol'] = key
            pre_list.append(frame)
        results = pd.concat(pre_list)
        return results.reset_index().set_index(keys=['symbol', 'time'])

    @property
    def frame(self):
        return self._frame

    @property
    def symbol_groups(self) -> DataFrameGroupBy:
        self._symbols_groups = self._frame.groupby(
            by='symbol', as_index=False, sort=True,
        )
        return self._symbols_groups

