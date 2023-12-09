# =============================================================================
#                              STOCK DICTIONARY
# =============================================================================
from collections import OrderedDict
from src.stock_instance import Stock
import os

class StockDictionary:

    stocks = None

    def __init__(self):
        if StockDictionary.stocks is None:
            self.load_stocks()


    def load_stocks(self):
        self.stocks = OrderedDict()

        files = os.listdir("./stock_data/select_stocks")

        for file in files:
            if file.endswith(".csv"):
                stock = Stock(os.path.join("./stock_data/select_stocks", file))
                self.stocks[file[:-4]] = stock

        self.stocks = OrderedDict(sorted(self.stocks.items()))


    def get_stock(self, name):

        return self.stocks[name]

