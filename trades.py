from robot import td_client
import indicator

# All this is really just paper trading, since the TD api doesn't have any paper trading capabilities.
class Instrument:

    def __init__(self, symbol=str):
        # stuff that will be used outside of the class
        self.symbol = symbol
        self.realized_profit = 0.0
        self.positional_value = 0.0
        self.current_price = 0.0
        # stuff that will be used only within this
        self.per_trade_profit = 0.0
        self.trade_price = 0.0
        self.amount = 0

    def update(self):  # update all the data that needs to be a per frame basis
        self.current_price = indicator.get_price(self.symbol)
        self.positional_value = self.current_price*self.amount
        if self.amount > 0.0:
            self.per_trade_profit = (self.current_price * self.amount) - (self.trade_price * self.amount)
        elif self.amount < 0.0:
            self.per_trade_profit = (self.trade_price * abs(self.amount)) - (self.current_price*abs(self.amount))

    def open(self, amount):  # Opening a trade, not really opening a trade per se, but just doing something that isn't closing a position. 
        self.amount = amount
        self.trade_price = self.current_price

    def close(self):  # actually closing a position. Pretty much just the best way I could figure how to calculate these types of things.
        self.realized_profit += self.per_trade_profit
        self.per_trade_profit = 0.0
        self.amount = 0
        self.trade_price = 0

