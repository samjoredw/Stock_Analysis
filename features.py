# =============================================================================
#                                 FEATURES
#                              --------------
#         Defines characteristics about a set of stocks and provides 
#                  infmormation about their similarities.
# =============================================================================
import pandas as pd
from stock_dictionary import StockDictionary
from stock_instance import Stock
import streamlit as st
import numpy as np

# -----------------------------------------------------------------------------
# This is where all the good stuff is. This class takes in a dictionary of
# dataframes and performs several different modifications based on the input.
# -----------------------------------------------------------------------------
class Features:


    # Initialization, taking in a dictionary of dfs
    # -----------------------------------------------------
    def __init__(self, dictionary):
        self.db = dictionary


    # Compares two general metrics to one another of two 
    # different dataframes. Then subsequently shrinking 
    # the dataframes based off of date and the needed columns.
    # -----------------------------------------------------
    def comparison(self, dat1, dat2, met1, met2, t1, t2):

        dat1 = self.db.get(dat1).get_data_frame()
        dat2 = self.db.get(dat2).get_data_frame()

        sub_1 = dat1[dat1.index >= pd.to_datetime(t1)]
        sub_2 = dat2[dat2.index >= pd.to_datetime(t1)]

        sub_1 = sub_1[sub_1.index <= pd.to_datetime(t2)]
        sub_2 = sub_2[sub_2.index <= pd.to_datetime(t2)]

        if met1 == 'OHLC':
            sub_1 = self.ohlc(sub_1)
            sub_2 = self.ohlc(sub_2)
        elif met1 == 'Volatility':
            sub_1 = self.volatility_compar(sub_1)
            sub_2 = self.volatility_compar(sub_2)
        else:
            sub_1 = sub_1.reset_index()
            sub_2 = sub_2.reset_index()

            sub_1 = sub_1[['Date', met1]]
            sub_2 = sub_2[['Date', met2]]

        sub_1.set_index('Date', inplace=True)
        sub_2.set_index('Date', inplace=True)

        return sub_1, sub_2


    # Finds the correlation 'scale' of two different stocks
    # and returns the scale number as well as two dataframes
    # of the 180 days that were most closely correlated
    # with one another based on the date range.
    # NOTE:
    # This CANNOT call comparison() function even though it 
    # has similar code. This would result in each stock being 
    # indexed inside the built-in db.
    # -----------------------------------------------------
    def correlation(self, dat1, dat2, met1, met2, t1, t2):

        # Data cleaning for input file:
        if isinstance(dat1, Stock):
            dat1 = Stock.get_data_frame(dat1)

        dat2 = Stock.get_data_frame(dat2)

        dat1 = dat1[[met1]]
        dat2 = dat2[[met2]]

        dat1.replace('null', np.nan, inplace=True)
        dat2.replace('null', np.nan, inplace=True)

        dat1.fillna(dat1.mean(), inplace=True)
        dat2.fillna(dat2.mean(), inplace=True)

        # Finding the correlation metric
        # Setting date range
        sub_1 = dat1[dat1.index >= pd.to_datetime(t1)]
        sub_2 = dat2[dat2.index >= pd.to_datetime(t1)]

        sub_1 = sub_1[sub_1.index <= pd.to_datetime(t2)]
        sub_2 = sub_2[sub_2.index <= pd.to_datetime(t2)]

        correlation = sub_1[met1].corr(sub_2[met2])

        # Finding instance of closest correlation
        # Original location of the following block
        window_size = 180

        rolling = sub_1[met1].rolling(window=window_size).corr(sub_2[met2])

        if not rolling.empty:
            max_rolling = rolling.idxmax()

            t1 = max_rolling - pd.DateOffset(days=window_size - 1)
            t2 = max_rolling
        else:
            st.write("The rolling object is empty. Unable to calculate correlation.")
            exit(1)

        sub_1 = sub_1.loc[(sub_1.index >= t1) & (sub_1.index <= t2)]
        sub_2 = sub_2.loc[(sub_2.index >= t1) & (sub_2.index <= t2)]

        return correlation, sub_1, sub_2


    # 2 company comparison of (O+H+L+C)/4
    # Takes the average and returns a new dataframe of one 
    # column.
    # -----------------------------------------------------
    def ohlc(self, df):

        ohlc = df[['Open', 'High', 'Low', 'Close']].iloc[1:].sum(axis=1) / 4
        new_df = pd.DataFrame({'OHLC': ohlc, 'Date': df.index[1:]})

        if 'Date' not in df.index.names:
            new_df.set_index('Date', inplace=True)

        return new_df


    # 2 company comparison of (H-L)
    # Takes the volitily of a single dataframe based off 
    # of high and low then returns a new dataframe with the 
    # newly created column.
    # -----------------------------------------------------
    def volatility_compar(self, df):

        volatility = df['High'].subtract(df['Low']).iloc[1:]
        new_df = pd.DataFrame({'Volatility': volatility, 'Date': df.index[1:]})

        if 'Date' not in df.index.names:
            new_df.set_index('Date', inplace=True)

        return new_df


    # Searches the imbedded dictionary for a dataframe based
    # on a given input name.
    # -----------------------------------------------------
    def search_stock(self, name):

        stock_list = [
            key
            for key in self.db.keys()
            if key.lower().startswith(name.lower())
        ]

        return stock_list


    # Returns the top ten highest entries of a dataframes
    # 'Close' metric. Takes in no parameters so it must only
    # be called with comparison()
    # -----------------------------------------------------
    def search_highest(self):

        # Assuming self.db is a dictionary of Stock 
        # objects where each Stock has a DataFrame
        # and the 'close' column starts with 'close'
        close_values = [
            (name, stock.df.filter(like='Close').iloc[-1].max()) for name, stock in self.db.items()
        ]

        # Sorts the list based on the 'close' values in descending order
        sorted_close_values = sorted(close_values, key=lambda x: x[1], reverse=True)

        # Takes the top ten entries from the sorted list
        top_ten_entries = sorted_close_values[:10]

        return top_ten_entries


# --------------------------------------------------------------------------------------
# GETTER functions for streamlit output, not part of specific features of the
# dataframes.
# --------------------------------------------------------------------------------------
def get_average(subset_stock1, metric1):

    val = subset_stock1[metric1].sum()
    size = subset_stock1.size
    avg = round((val / size), 2)

    return avg

def get_high(subset_stock1, metric1):

    val = subset_stock1[metric1].max()
    return round(val, 2)



