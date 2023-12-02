import streamlit as st
import features
import graph
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


    use_personal = st.checkbox("Would you like to use your own stock? (requires file input)", value=False)

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
        start = col1.slider(label="Begin Date", min_value=1980, max_value=2023, value=2022)
        end = col3.slider(label="End Date", min_value=1980, max_value=2023, value=2023)

        start = f"{start}-01-01"
        end = f"{end + 1}-01-01"

        submit_button = col3.form_submit_button("Submit")

    if submit_button:

        if use_personal:
            selection1 = indv_stocks.get(selection1)
        else:
            selection1 = stocks.get(selection1)

        selection2 = stocks.get(selection2)

        if selection1 is not None and selection2 is not None:

            corr1, selection1, selection2 = (
                features_instance2.correlation(selection1, selection2, metric1, metric2, start, end))

            fig1 = graph.graph_stocks(selection1, selection2, 'selection1', 'selection2')

            with st.expander("Graph View"):
                st.pyplot(fig1)

            with st.expander("Relationship View"):
                st.write(f"""
                The correlation between these two stocks is {round(corr1, 3)}.

                This means that these two stocks have a {round(corr1 * 100)}% relationship with one
                another within your date range above. Which is {describe(corr1)[0]}.
                """)

        else:
            st.write("Error: Unable to retrieve stock data. Please check your inputs.")


def describe(correlation):

    if correlation < -.8:
        descriptor = ('extremely low. They seem to be polarizing in there fluctuations. These stocks could be used to'
                      'make contrasting predictions between one another')
    elif correlation < -.5:
        descriptor = 'very low. They tend to be compliments of one another.'
    elif correlation < 0:
        descriptor = 'low and means very little correlation if any at all'
    elif correlation < .33:
        descriptor = 'somewhat average. They do not correlate very much'
    elif correlation < .6:
        descriptor = 'moderate. They have positively corresponding relationship with one another'
    elif correlation < .8:
        descriptor = ('high. They have very similar trends in their fluctuation. Definitely two stocks to keep '
                      'an eye on')
    elif correlation < .9:
        descriptor = 'very high. These two stocks could be used to make predictions upon one another'
    else:
        descriptor = 'extremely high. Are these the same stock?! If not, you might be on to something..'

    return descriptor, descriptor



