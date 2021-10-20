import robot
import indicator
import pprint
import trades
import time
import account

crossover = 'None'
rel = 'None'
prev_rel = 'None'

portfolio = ()

spy = trades.Instrument('SPY')


while True:
    # getting macd, finding crossover, and purchasing/selling to make money
    macd = indicator.get_macd('SPY')
    round_mac = round(macd['MACD'], 2)
    round_sig = round(macd['Signal line'], 2)
    if round_mac[len(round_mac)-1] > round_sig[len(round_sig)-1]:
        rel = 'Above'
    elif round_mac[len(round_mac)-1] < round_sig[len(round_sig)-1]:
        rel = 'Below'
    elif round_mac[len(round_mac)-1] == round_sig[len(round_sig)-1]:
        rel = prev_rel

    spy.update()  # Updating the trade

    # checking whether to sell or buy
    if not rel == prev_rel:
        if rel == 'Above':
            crossover = 'Uptrend'
            spy.close()
            spy.open(100.000)
        elif rel == 'Below':
            crossover = 'Downtrend'
            spy.close()
            spy.open(-100.000)

    # debugging
    print("Trade price: $" + str(spy.trade_price))
    print("Current Price: $" + str(spy.current_price))
    print("Realized Profits: $" + str(spy.realized_profit))
    print("Per Trade Profits: $" + str(spy.per_trade_profit))
    print("Amount: " + str(spy.amount))

    prev_rel = rel  # updating prev rel for macd

    time.sleep(10)
