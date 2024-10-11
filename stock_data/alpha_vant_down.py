###
# This is a .py file that successfully imports data from alpha vantage
# Its use case would be to add new stocks to our model for assessment
# However, user input of files like this was preferred to demonstrate
# accuracy of the model and its ability to learn.
#
# Ultimately, it creates a dictionary of dataframes for modeling and
# also auto creates a folder of csv files using the dataframes to the OS current
# directory.
#
# NOTE: This script should only be run and used through the backend as a means of
# retrieving data.
###

import os
import requests
import pandas as pd
from io import StringIO

def run_clean():

    input("Continue?")

    api_key = system.get("ALPHA_SECRET")

    output_folder = 'stock_data'
    os.makedirs(output_folder, exist_ok=True)
    # Get the current list of S&P500 companies and read them into a df
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url, verify=False)
    # 'False' not recommended but acceptable in the case of a single retrieval
    html_text = response.text

    html_file = StringIO(html_text)
    sp500_df = pd.read_html(html_file)[0]['Symbol']

    # Then, we get the endpoint of the alpha vantage db (TIME SERIES DAILY) as in all stocks above
    endpoint = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY'
    stock_dict = {}
    print("After requests and endpoints")

    for stock in sp500_df:
        req = f'{endpoint}&symbol={stock}&apikey={api_key}'

        # Making request to alpha vantage
        response = requests.get(req)
        data = response.json()

        # Extracting stock prices from the response
        time_series = data.get('Time Series (Daily)', {})

        # Some data cleaning
        df = pd.DataFrame(time_series).transpose()

        csv_filename = os.path.join(output_folder, f'{stock}.csv')
        df.to_csv(csv_filename, index=True, index_label='date')

        stock_dict[stock] = df
        print(f"Saved CSV for {stock}")

    print("All symbols processed.")

    return stock_dict
