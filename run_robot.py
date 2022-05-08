#! /usr/bin/python3

import trades
import time
from datetime import datetime

# PUT SYMBOLS YOU WANT TO TRADE BELOW
spy = trades.Instrument('SPY')
# LMT = trades.Instrument('LMT')
# QQQ = trade.Instrument('QQQ')
# TSLA = trade.Instrument('TSLA')
# GenericStock = trade.Instrument('INSERTSYMBOLHERE')
# The API does have the ability to trade options, futures, etc, but I cannot be bothered to try and implement that

# Time in seconds between updates
interval = 10

errors = 0


def main_fcn():
    now = datetime.now()  # getting the time in seconds since epoch

    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    second = int(now.strftime("%S"))
    clock = (str(hour) + ':' + str(minute) + ':' + str(second))

    print(clock)
    for item in trades.portfolio:  # run everything for all the trades
        # Only operate during market hours
        if hour == 9:
            if minute < 30:
                continue
        if 9 > hour > 16:
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

def mainloop():
    while True:  # Basically going to run
        try:
            main_fcn()
        except Exception as e:  # Crashes a lot.
            errors += 1
            if errors == 3:
                for i in trades.portfolio:
                    i.file.close()
                    print(e)
                    print('Closed')
                    exit(1)
            else:
                print(e)

        time.sleep(interval)
 
if __name__ == "__main__":
    mainloop()
