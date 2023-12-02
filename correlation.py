import streamlit as st
import features
import stock_dictionary
import stock_instance
import os

# Sets the dictionary and dataframes
stocks = stock_dictionary.StockDictionary().stocks
features_instance2 = features.Features(stocks)

def run():
    st.empty()
    st.title("Correlations")
    st.markdown("---")

    with st.expander('Feature Details (click to expand/shrink)'):
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


    use_personal = st.checkbox("Would you like to use your own stock? (Requires file input)", value=False)

    indv_stocks = {}

    if use_personal:
        files = st.file_uploader(label="Upload your file here.", type=['csv'], accept_multiple_files=True)
        if files is not None:
            for file in files:
                name = os.path.splitext(file.name)[0]
                df = stock_instance.Stock(file).get_data_frame()
                indv_stocks[name] = df
        else:
            st.write("Please upload at least one file.")

    with st.form('Submit'):
        col1, col2, col3 = st.columns(3)

        if use_personal:
            selection1 = col1.selectbox(label='Your Stocks', options=indv_stocks.keys(), index=None)
        else:
            selection1 = col1.selectbox(label='Second Stock', options=stocks.keys(), index=None)

        metric1 = col2.radio(label=f"Your Stock's Metric",
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric1")

        selection2 = col1.selectbox(label='Second Stock', options=stocks.keys(), index=None)
        metric2 = col3.radio(label=f'Metric for Second Stock',
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric2")

        col1.text("")
        col1.text("")
        start = col1.slider(label="Begin Date", min_value=1980, max_value=2023, value=2022)
        end = col3.slider(label="End Date", min_value=1980, max_value=2023, value=2023)

        submit_button = col3.form_submit_button("Submit")


    if submit_button:

        if selection1 in indv_stocks.keys():
            selection1 = indv_stocks[selection1]
            selection2 = stocks.get_stock(selection2)

            corr_value, selection1, selection2 = (
                features_instance2.correlation(selection1, selection2, metric1, metric2, start, end))









