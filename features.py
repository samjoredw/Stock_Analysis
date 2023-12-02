# =============================================================================
#                                 FEATURES
# =============================================================================
import pandas as pd
from stock_dictionary import StockDictionary

class Features:

    def __init__(self, dictionary):
        self.db = dictionary

    # Compares two general metrics to one another
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

    # IMPORTANT:
    # This CANNOT call comparison function even though it has similar code.
    # This would result in each stock being indexed inside the built-in db.
    def correlation(self, dat1, dat2, met1, met2, t1, t2):

        # Finding the correlation metric
        # ------------------------------------------------------------------------
        column_to_find = 'Date'
        column_names = dat1.columns

        date_column = next((col for col in column_names
                            if col.lower() == column_to_find.lower()), None)

        if date_column is None:
            return 0

        dat1.set_index(date_column, inplace=True)
        dat2.set_index('Date', inplace=True)

        dat1 = dat1[[date_column, met1]]
        dat2 = dat2[['Date', met2]]

        # Setting date range
        sub_1 = dat1[dat1.index >= pd.to_datetime(t1)]
        sub_2 = dat2[dat2.index >= pd.to_datetime(t1)]
        sub_1 = sub_1[sub_1.index <= pd.to_datetime(t2)]
        sub_2 = sub_2[sub_2.index <= pd.to_datetime(t2)]

        sub_1 = sub_1.reset_index()
        sub_2 = sub_2.reset_index()

        sub_1 = sub_1[['Date', met1]]
        sub_2 = sub_2[['Date', met2]]

        correlation = sub_1[met1].corr(sub_2[met2])


        # Finding instance of closest correlation
        # ------------------------------------------------------------------------
        window_size = 30

        rolling = sub_1[met1].rolling(window=window_size).corr(sub_2[met2])

        max_rolling = rolling.idxmax()

        t1 = max_rolling - pd.DateOffset(days=window_size - 1)
        t2 = max_rolling

        sub_1 = sub_1.loc[(sub_1.index >= t1) & (sub_1.index <= t2)]
        sub_2 = sub_2.loc[(sub_2.index >= t1) & (sub_2.index <= t2)]

        return correlation, sub_1, sub_2

    # 2 company comparison of (O+H+L+C)/4
    def ohlc(self, df):

        ohlc = df[['Open', 'High', 'Low', 'Close']].iloc[1:].sum(axis=1) / 4
        new_df = pd.DataFrame({'OHLC': ohlc, 'Date': df.index[1:]})

        if 'Date' not in df.index.names:
            new_df.set_index('Date', inplace=True)

        return new_df

    # 2 company comparison of (H-L)
    def volatility_compar(self, df):

        volatility = df['High'].subtract(df['Low']).iloc[1:]
        new_df = pd.DataFrame({'Volatility': volatility, 'Date': df.index[1:]})

        if 'Date' not in df.index.names:
            new_df.set_index('Date', inplace=True)

        return new_df


    def search_stock(self, name):

        stock_list = [key for key in self.db.keys() if key.lower().startswith(name.lower())]

        return stock_list


    def search_highest(self):

        # Assuming self.db is a dictionary of Stock objects where each Stock has a DataFrame
        # and the 'close' column starts with 'close'
        close_values = [
            (name, stock.df.filter(like='Close').iloc[-1].max()) for name, stock in self.db.items()
        ]

        # Sort the list based on the 'close' values in descending order
        sorted_close_values = sorted(close_values, key=lambda x: x[1], reverse=True)

        # Take the top ten entries from the sorted list
        top_ten_entries = sorted_close_values[:10]

        return top_ten_entries

# ==================================================================================================
# GETTER functions for streamlit output, not part of specific features of the dataframes
# ==================================================================================================
def get_average(subset_stock1, metric1):

    val = subset_stock1[metric1].sum()
    size = subset_stock1.size
    avg = round((val / size), 2)

    return avg

def get_high(subset_stock1, metric1):

    val = subset_stock1[metric1].max()
    return round(val, 2)



