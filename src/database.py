import streamlit as st
import pandas as pd
import graph
import features
import stock_dictionary

# Sets the dictionary and dataframes
stocks = stock_dictionary.StockDictionary().stocks
features_instance1 = features.Features(stocks)

def run():

    st.empty()
    st.subheader("Database Structure & Presentation")

    expand = st.expander('Feature Details (database)')

    with expand:

        st.write("**Select Stock Database 1980-2023**")

        st.write("This page is used to demonstrate the functionality of my database.")
        st.write("""
        **How to use this database:**
        - Enter two different stocks to compare with one another
        - Enter a financial metric for each stock to compare upon
        - Enter a start date and end date
        - Depending on what you choose, a graph will be generated to visualize the data
        
        If you only see one (or neither) of the two stocks on the graph, you likely need to adjust 
        the date range as those companies weren't public yet.
        
        Also, note that  a stocks volume is comparable only to another stocks volume as it is not a 
        monetary metric like the others.
        
        **Usage:**
        
        The ability to assess stocks with one another is essential to finding correlations and
        ultimately drafting a model for learning and predicting.
        
        Play around with it and see its functionality! 💵 💶 💷 💴
        """)

    with st.form('Submit'):
        col1, col2, col3 = st.columns(3)
        selection1 = col1.selectbox(label='Stock 1', options=stocks.keys(), index=None)
        metric1 = col2.radio(label=f'Metric for Stock 1',
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric1")

        selection2 = col1.selectbox(label='Stock 2', options=stocks.keys(), index=None)
        metric2 = col3.radio(label=f'Metric for Stock 2',
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric2")

        col1.text("")
        col1.text("")
        start = col1.slider(label="Begin Date", min_value=1980, max_value=2023, value=2022)
        end = col3.slider(label="End Date", min_value=1980, max_value=2023, value=2023)

        submit_button = col3.form_submit_button("Submit")

    if submit_button:

        # Handle exceptions
        if not selection1 or not selection2:
            st.write("Please select your stocks.")
            exit(1)
        if selection1 == selection2:
            st.write("Please enter two different stocks.")
            exit(1)
        if start > end:
            st.write("Please enter a valid date range.")
            exit(1)
        if ((metric1 == 'Volume' and metric2 != 'Volume') or
                (metric1 != 'Volume' and metric2 == 'Volume')):
            st.write("To use volume, please make sure both stocks have selected 'Volume' as their metric of choice.")
            exit(1)

        start = f"{start}-01-01"
        end = f"{end + 1}-01-01"

        stock_name1 = selection1
        stock_name2 = selection2
        date_start = start
        date_end = end

        # Generate metric comparison
        subset_stock1, subset_stock2 = \
            (features_instance1.comparison(stock_name1, stock_name2, metric1, metric2, date_start, date_end))

        fig1 = graph.graph_stocks(subset_stock1, subset_stock2, stock_name1, stock_name2)

        with st.expander('Graph View'):
            st.pyplot(fig1)

        with st.expander('Relationship View'):

            avg_1 = features.get_average(subset_stock1, metric1)
            avg_2 = features.get_average(subset_stock2, metric2)

            max_1 = features.get_high(subset_stock1, metric1)
            max_2 = features.get_high(subset_stock2, metric2)

            new_start_date = pd.to_datetime(date_start).strftime('%Y')
            new_end_date = pd.to_datetime(date_end).strftime('%Y')

            avg_1 = "{:,}".format(round(avg_1))
            avg_2 = "{:,}".format(round(avg_2))
            max_1 = "{:,}".format(max_1)
            max_2 = "{:,}".format(max_2)

            st.write(f"""
            **Measurement Stats**
            
            The graph above represents two different stocks between the range of {new_start_date} and {new_end_date}.
            
            """)

            if metric1 == "Volume":
                st.write(f"The average number of trades for "
                         f"{stock_name1} from {new_start_date} to {new_end_date} was **{avg_1}**"
                         f" going as high as {max_1}")
                st.write(f"The average number of trades for "
                         f"{stock_name2} from {new_start_date} to {new_end_date} was **{avg_2}**"
                         f" going as high as {max_2}")
            else:
                st.write(f"The average {metric1.lower()} stock price for "
                         f"{stock_name1} from {new_start_date} to {new_end_date} was **{avg_1}** dollars"
                         f" going as high as {max_1} dollars")
                st.write(f"The average {metric2.lower()} stock price for "
                         f"{stock_name2} from {new_start_date} to {new_end_date} was **{avg_2}** dollars"
                         f" going as high as {max_2} dollars")

            st.write("""
            But theres a lot more we can do with this stock information now that we know how to 
            navigate the database! Take a look at the 'Correlations' tab to get some insights on our
            data and to add some data of your own.
            """)
        
        with st.expander('Table View'):
            
            ncol1, ncol2 = st.columns(2)
            ncol1.dataframe(subset_stock1)
            ncol2.dataframe(subset_stock2)
