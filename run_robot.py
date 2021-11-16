import trades
import time
from datetime import datetime

now = datetime.now()

hour = int(now.strftime("%H"))
minute = int(now.strftime("%M"))
second = int(now.strftime("%S"))

# PUT SYMBOLS YOU WANT TO TRADE BELOW
spy = trades.Instrument('SPY')
# LMT = trades.Instrument('LMT')
# QQQ = trade.Instrument('QQQ')
# TSLA = trade.Instrument('TSLA')
# GenericStock = trade.Instrument('INSERTSYMBOLHERE')
# The API does have the ability to trade options, futures, etc, but I cannot be bothered to try and implement that

# Time in seconds between updates
interval = 10

try:
    while True:
        for item in trades.portfolio:  # run everything for all the trades
            # Only operate during market hours
            if hour == 9:
                if minute < 30:
                    continue
            elif 9 > hour > 16:
                continue
            else:
                item.use_macd()  # using macd because RSI isn't super accurate for what im trying to do - pseudo HFT

                # update all the trades and P/L and the spreadsheets.
                item.update()

                # Show us the money!
                print(str(item.symbol))
                print("Trade price: $" + str(item.trade_price))
                print("Current Price: $" + str(item.current_price))
                print("Realized Profits: $" + str(item.realized_profit))
                print("Per Trade Profits: $" + str(item.unrealized_profit))
                print("Amount: " + str(item.amount))
                print('\n')

        time.sleep(interval)  # updated every interval seconds
except KeyboardInterrupt:
    for item in trades.portfolio:
        item.file.close()
