# =============================================================================
#                               CORRELATIONS
#                            ------------------
#         Serves to find correlations within the database by comparing
#                  different metrics and using features.py
# =============================================================================

import streamlit as st
from src import features
from src import graph
from src import stock_dictionary
from src import stock_instance
import os
from datetime import datetime

# Sets the dictionary and dataframes
stocks = stock_dictionary.StockDictionary().stocks
features_instance2 = features.Features(stocks)

def run():

    st.empty()
    expand1 = st.expander('How to use this database')

    with expand1:
        st.markdown("""
    **Searching the Database**
    
    - Pick two stocks from the drop-down menus
    - Pick two metrics to compare your stocks upon ('Volume' must be with 'Volume')
    - Pick two dates: The start date and end date that you would like to search for a 
    correlation in.
    - Submit and check your results
    
    **Submitting a File**
    
    - [Go to Yahoo Finance](https://finance.yahoo.com)
    - Search for a symbol at the top
    - Go to 'Historical Data' tab under the stock name
    - Select a time period (recommended: 'MAX')
    - Select 'Daily Frequency'
    - Hit 'Apply' and then 'Download'
    - Come back here and check the box below
    - Upload your file
    - Select your stock in the dropdown menu
    - Submit and check your results
    """)


    use_personal = st.checkbox("Add your own stock (requires file input)", value=False)

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
            selection1 = col1.selectbox(label='Your Stocks', options=indv_stocks.keys(), index=None, key='Selection 1')
        else:
            selection1 = col1.selectbox(label='First Stock', options=stocks.keys(), index=None, key='Selection 1')

        metric1 = col2.radio(label=f"Your Stock's Metric",
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric1")

        selection2 = col1.selectbox(label='Second Stock', options=stocks.keys(), index=None, key='Selection 2')
        metric2 = col3.radio(label=f'Metric for Second Stock',
                             options=('High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume'), key="metric2")

        col1.text("")
        col1.text("")
        start = col1.slider(label="Begin Date", min_value=1995, max_value=2023, value=2020)
        end = col3.slider(label="End Date", min_value=1995, max_value=2023, value=2023)

        start = f"{start}-01-01"
        end = f"{end + 1}-01-01"

        submit_button = col3.form_submit_button("Submit")

    if submit_button:

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

        stock_name1 = selection1
        stock_name2 = selection2

        if use_personal:
            selection1 = indv_stocks.get(selection1)
        else:
            selection1 = stocks.get(selection1)

        selection2 = stocks.get(selection2)

        if selection1 is not None and selection2 is not None:

            corr1, selection1, selection2 = (
                features_instance2.correlation(selection1, selection2, metric1, metric2, start, end))

            fig1 = graph.graph_stocks(selection1, selection2, stock_name1, stock_name2)


            if fig1 == 0:
                st.write("See 'How to use this database' above.")
                exit(1)

            with st.expander("Closest Correlation Over 180 Days | Graph"):
                st.pyplot(fig1)

            with st.expander("Relationship Analysis"):
                pr_start = datetime.strptime(start, "%Y-%m-%d")
                pr_start = pr_start.strftime("%Y")

                pr_end = datetime.strptime(end, "%Y-%m-%d")
                pr_end = pr_end.strftime("%Y")

                st.write(f"""
                **Correlation Stats**
                
                The graph above represents the **180 days** from {pr_start} to {pr_end} where the correlation between
                {stock_name1} and {stock_name2} is strongest.
                
                The correlation between these two stocks is **{round(corr1, 3)}** on a scale from -1 
                (opposing, negative correlation) to 1 (similar, positive correlation).

                This means that these two stocks have around a **{round(corr1 * 100)}%** relationship with one
                another within your date range above. Which is {describe(corr1)[0]}
                
                **Make Some Changes**
                
                Play around with the date ranges above to see if this number changes. To find the most correlated
                180 days between these two stocks, put the start date at 1980 and the end date at 2023.
                
                Switch up the stocks and see if you can find the highest correlation between any two metrics and
                any two dates! (Hint: the scale correlation is 0.977)
                """)

        else:
            st.write("Error: Unable to retrieve stock data. Please check your inputs.")


def describe(correlation):

    if correlation < -.8:
        descriptor = 'extremely low.'
    elif correlation < .6:
        descriptor = 'very low.'
    elif correlation < .7:
        descriptor = 'low.'
    elif correlation < .8:
        descriptor = 'average.'
    elif correlation < .85:
        descriptor = 'moderate.'
    elif correlation < .9:
        descriptor = 'high.'
    elif correlation < .95:
        descriptor = 'very high.'
    else:
        descriptor = 'extremely high.'

    return descriptor, descriptor



