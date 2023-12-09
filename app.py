# =============================================================================
#                                 HOME PAGE 
#                               -------------
#      Serves as a main page demo for my project using streamlit and html.
# =============================================================================
import streamlit as st
# pages
from src import correlation, prediction

# -----------------------------------------------------------------------------
# This serves as the homepage of my project. It initializes a list of pages
# that can be navigated though to see different elements of my project.
# The home page shows how the database functions and some insights into
# the data itself.
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Stock Database Project - Sam Edwards", page_icon="📊")

st.empty()
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            max-width: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page key identifiers:
cor = "Correlations"
predict = "Predictions"

st.sidebar.write("# Navigation Bar")
menu_radio = st.sidebar.radio(label="Main Menu",options=[cor,predict],key='menu')

if menu_radio == predict:
    prediction.run()
if menu_radio == cor:
    st.subheader("Stock Database")
    st.write("""
    
This website demonstrates the functionality of my built-in stock database and illustrates the 
accuracy of my predictive machine-learning model on trends in the market.

This database GUI helps you finds trends in the market between two different stocks. Choose a date range and the 
database will show you the 180 day period with the highest correlation.
""")
    correlation.run()

st.empty()

