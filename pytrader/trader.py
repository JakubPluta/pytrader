from datetime import datetime, time, timezone, timedelta
from typing import List, Dict, Union, Optional
import pandas as pd
import alpaca_trade_api as alpaca



BASE_URL = 'https://paper-api.alpaca.markets'


class PyTrader:

    def __init__(self, key_id: str, secret_key: str, base_url: str = BASE_URL):
        self.client = alpaca.REST(key_id, secret_key, base_url)
        self.trades: dict = {}
        self.historical_prices: dict = {}

    @property
    def account(self):
        return self.client.get_account()

    def create_order(self, symbol:str, qty: int, side: str, type: str, time_in_force: str, *args):
        if qty > 0:
            order_id = self._create_order_id(symbol, side)
            self.client.submit_order(symbol, qty, side, type, time_in_force,*args)
            results = locals()
            del results['self']
            self.trades[order_id] = results
        else:
            raise ValueError("qty (quantity) needs to be positive number")

    @staticmethod
    def _create_order_id(symbol, side):
        return f"{symbol}_{side}_{datetime.now().timestamp()}"

    @staticmethod
    def _parse_datetime_column(price_df: pd.DataFrame) -> pd.DataFrame:
        price_df['datetime'] = pd.to_datetime(price_df['datetime'], unit='ms', origin='unix')
        return price_df

    @staticmethod
    def seconds_till_market_is_open(now: datetime):
        if now.weekday() <= 4:
            dt = (now + timedelta(days=1)).date()
        else:
            till_monday = 7 - now.weekday()
            dt = (now + timedelta(days=till_monday)).date()
        tomorrow = datetime.combine(dt, time(hour=9,minute=30))
        seconds_till_market_open = (tomorrow - now).total_seconds()
        return seconds_till_market_open


    def get_data_bars(self, symbols, time_frame='5Min', slow=30, fast=5):
        data = self.client.get_barset(symbols, time_frame, limit=20).df
        for symbol in symbols:
            data.loc[:, (symbol, 'fast_ema')] = data[symbol]['close'].rolling(window=fast).mean()
            data.loc[:, (symbol, 'slow_ema')] = data[symbol]['close'].rolling(window=slow).mean()
        return data

