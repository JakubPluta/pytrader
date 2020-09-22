import alpaca_trade_api as alpaca
from pytrader.trader import PyTrader
import time
import datetime
from datetime import timedelta
from pytz import timezone
from configparser import ConfigParser
from ta import add_all_ta_features, trend, momentum, volume, volatility, add_trend_ta, add_momentum_ta
from btalib import sma, ema, macd, rsi, beta, kama, roc
import pandas as pd
pd.options.mode.chained_assignment = None


tz = timezone('US/Eastern')

import logging
logging.basicConfig(filename='./apca_algo.log', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('{} logging started'.format(datetime.datetime.now().strftime("%x %X")))

config = ConfigParser()
config.read(r'C:\Repository\priv\trader\config\config.ini')

KEY = config.get('api', 'KEY')
SECRET = config.get('api', 'SECRET')
BASE = config.get('api', 'BASE')


pyt = PyTrader(KEY, SECRET, BASE)


def get_data_bars(symbols, timeframe='5Min'):
    data = pyt.client.get_barset(symbols, timeframe, limit=50).df
    for symbol in symbols:
        feats = add_momentum_ta(data.get(symbol),'high', 'low', 'close', 'volume')
        feats = add_trend_ta(feats,'high', 'low', 'close')
        for f in feats:
            data.loc[:, (symbol, f)] = feats.loc[:,f]
    return data


def get_signal_bars(symbol_list, rate):
    data = get_data_bars(symbol_list, rate)
    signals = {}
    for x in symbol_list:
        if data[x].iloc[-1]['trend_sma_fast'] > data[x].iloc[-1]['trend_sma_slow']: signal = 1
        else: signal = 0
        signals[x] = signal
    return signals


def time_to_open(current_time):
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30,tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds


def run(stocks):

    while True:
        if 0 <= datetime.datetime.now(tz).weekday() <= 4:
            print("Trading Session!")
            if datetime.time(9, 30) < datetime.datetime.now(tz).time() <= datetime.time(15, 30):
                signals = get_signal_bars(stocks, '5Min')
                for signal in signals:
                    if signals[signal] == 1:
                        if signal not in [x.symbol for x in pyt.client.list_positions()]:
                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal,
                                                                signals[signal]))
                            pyt.client.submit_order(signal, 1, 'buy', 'market', 'day')
                    else:
                        try:
                            pyt.client.submit_order(signal, 1, 'sell', 'market', 'day')
                            logging.warning('{} {} - {}'.format(datetime.datetime.now(tz).strftime("%x %X"), signal,
                                                                signals[signal]))
                        except Exception as e:
                            pass
                time.sleep(60)
            else:
                # Get time amount until open, sleep that amount
                print('Market closed ({})'.format(datetime.datetime.now(tz)))
                print('Sleeping', round(time_to_open(datetime.datetime.now(tz))/60/60, 2), 'hours')
                time.sleep(time_to_open(datetime.datetime.now(tz)))



stocks = ['AAPL', 'FB', 'AT', 'CSCO',"BEN", "HPE", "IBM",'AMD','MO']

print('test:')

run(stocks)

