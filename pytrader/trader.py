from datetime import datetime, time, timezone
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





