""" The 'local' and 'global' variables are just nicknames; just a way to organize what i want to be used inside
and outside of the class, but i might need the 'local' ones for debugging, so just organizing them. """

import indicator
from datetime import datetime
import xlsxwriter

now = datetime.now()
portfolio = []


class Instrument:
    # This function is a mess
    def __init__(self, symbol=str):
        # 'global' variables
        self.symbol = symbol
        self.realized_profit = 0.0
        self.positional_value = 0.0
        self.current_price = 0.0
        self.unrealized_profit = 0.0
        self.trade_price = 0.0
        self.amount = 0
        portfolio.append(self)
        self.textName = (str(self.symbol) + '.xlsx')
        self.file = xlsxwriter.Workbook(self.textName)
        self.spreadsheet = self.file.add_worksheet()
        self.row = 2

        # 'local' variables - mainly for macd LOL
        self.rel = None
        self.prev_rel = None
        self.macd = None
        self.round_mac = None
        self.round_sig = None

        # initializing the spreadsheet
        self.spreadsheet.write('A1', 'Time')
        self.spreadsheet.write('B1', 'Unrealized Profit')
        self.spreadsheet.write('C1', 'Realized Profit')

    def update(self):  # update all the data that needs to be a per frame basis
        self.current_price = indicator.get_price(self.symbol)
        self.positional_value = self.current_price*self.amount
        if self.amount > 0.0:
            self.unrealized_profit = (self.current_price * self.amount) - (self.trade_price * self.amount)
        elif self.amount < 0.0:
            self.unrealized_profit = (self.trade_price * abs(self.amount)) - (self.current_price*abs(self.amount))
        self.spreadsheet.write(('A' + str(self.row)), now)
        self.spreadsheet.write(('B' + str(self.row)), self.unrealized_profit)
        self.spreadsheet.write(('C' + str(self.row)), self.realized_profit)
        self.row += 1

    def open(self, amount):
        self.current_price = indicator.get_price(self.symbol)
        self.amount = amount
        self.trade_price = self.current_price

    def close(self):
        self.realized_profit += self.unrealized_profit
        self.unrealized_profit = 0.0
        self.amount = 0
        self.trade_price = 0


    def use_macd(self):
        # Getting the MACD and signal line
        self.macd = indicator.get_macd(self.symbol)
        self.round_mac = round(self.macd['MACD'], 2)
        self.round_sig = round(self.macd['Signal line'], 2)

        # Getting the relation between the two
        if self.round_mac[len(self.round_mac) - 1] > self.round_sig[len(self.round_sig) - 1]:
            self.rel = 'Above'
        elif self.round_mac[len(self.round_mac) - 1] < self.round_sig[len(self.round_sig) - 1]:
            self.rel = 'Below'
        elif self.round_mac[len(self.round_mac) - 1] == self.round_sig[len(self.round_sig) - 1]:
            self.rel = self.prev_rel

        # checking whether to sell or buy
        if self.rel != self.prev_rel:
            if self.rel == 'Above':
                self.close()
                self.open(100.000)
            elif self.rel == 'Below':
                self.close()
                self.open(-100.000)

        # Setting up for the next iteration
        self.prev_rel = self.rel
