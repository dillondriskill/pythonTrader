import pprint

import pandas as pd
import time
from robot import td_client
start = int((time.time()*1000)-1)  # For some reason this value doesnt actually change the output?
end = int(time.time()*1000)


def get_prices(symbol=str):  # as the program goes on the list gets longer and longer. No idea why. Maybe ext hours?
    raw_prices = td_client.get_price_history(
        symbol=symbol,
        start_date=start,
        end_date=end,
        frequency_type='minute',
        frequency='1',
        extended_hours='True')
    prices = pd.DataFrame(data=raw_prices['candles'], columns=['close'])

    return prices


def get_price(symbol=str):
    prices = get_prices(symbol)
    price = prices['close'][len(prices)-1]

    return price


def get_macd(symbol=str):  # get macd, and signal line
    data = get_prices(symbol)
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data


def get_rsi(symbol=str):
    data = get_prices(symbol)
    delta = data['close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=13).mean()
    ema_down = down.ewm(com=13).mean()
    rs = ema_up/ema_down
    data['RSI'] = 100 - (100/(1+rs))

    return data
