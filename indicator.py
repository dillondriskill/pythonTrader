# Theres LOTS of math on this page. If you feel like you can understand it, goof for you
# For the rest of us who can hardly make heads or tails of this, just read the comment, that's all you'll need to know.

import pandas as pd
import time
from robot import td_client
start = int((time.time()*1000)-1)  # For some reason this value doesnt actually change the output?
end = int(time.time()*1000)

# Frequency type vs frequency is complicated, and theres a chart somewhere that describes the numbers that can go with
# each type
frequency_type = 'minute'  # the scale of the candles
frequency = '1'  # how many of the scale wide to make the candles


def get_prices(symbol=str):  # get the prices of the last day for whatever symbol. Not getting multiple symbols
    # as the program goes on the list gets longer and longer, rather than getting the same numbers of candles.
    # No idea why... Maybe ext hours?
    raw_prices = td_client.get_price_history(
        symbol=symbol,
        start_date=start,
        end_date=end,
        frequency_type='minute',
        frequency='1',
        extended_hours='True')
    prices = pd.DataFrame(data=raw_prices['candles'], columns=['close'])

    return prices


def get_price(symbol=str):  # getting just the current price of symbol
    prices = get_prices(symbol)
    price = prices['close'][len(prices)-1]

    return price


def get_macd(symbol=str):  # get macd, and signal line, actually a lot more going on on behind the lines here.
    # Took a while to make this efficient (thanks pandas!)
    data = get_prices(symbol)
    exp1 = data['close'].ewm(span=12, adjust=False).mean()
    exp2 = data['close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data


def get_rsi(symbol=str):  # get rsi, not much to it really
    data = get_prices(symbol)
    delta = data['close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=13).mean()
    ema_down = down.ewm(com=13).mean()
    rs = ema_up/ema_down
    data['RSI'] = 100 - (100/(1+rs))

    return data
