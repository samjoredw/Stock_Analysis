# =============================================================================
#                              STOCK INSTANCE
# =============================================================================
import pandas as pd

class Stock:

    def __init__(self, file):
        # Initializing Stock with a file path
        self.path = file

        # Extracting stock name from the file path and loading data from CSV using pandas
        self.df = pd.read_csv(self.path)

        self.df['Date'] = pd.to_datetime(self.df['Date'])

        self.df.set_index('Date', inplace=True)


    def get_data_frame(self):

        return self.df