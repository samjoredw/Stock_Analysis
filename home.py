# =============================================================================
#                                 HOME PAGE 
#                               -------------
#      Serves as a main page demo for my project using streamlit and html.
# =============================================================================
import streamlit as st
from PIL import Image
# pages
from src import correlation

# -----------------------------------------------------------------------------
# This serves as the homepage of my project. It initializes a list of pages
# that can be navigated though to see different elements of my project.
# The home page shows how the database functions and some insights into
# the data itself.
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Stock Database Project - Sam Edwards", page_icon="📊")

st.empty()

banner = Image.open('./stck_database.jpg')
st.image(banner, use_column_width=True)

st.write("""
    
This website demonstrates the functionality of my built-in stock database and illustrates the 
accuracy of my correlation algorithm.

This database GUI helps you finds trends in the market between two different stocks. Choose a date range and the 
database will show you the 180 day period with the highest correlation.

""")

correlation.run()
st.markdown('<div style="display: flex; justify-content: center;">'
            '<a href="https://github.com/samjoredw/Stock_Analysis" target="_blank"> '
            '<img src="https://github.com/favicon.ico" alt="GitHub" width="20"/> '
            '</a>'
            '</div>', unsafe_allow_html=True)

custom_css = """
<style>
    h1 {
        margin-top: 0; /* Adjust this value as needed */
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
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
st.markdown(
    """
    <style>
        .viewerBadge_link__qRIco {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
        .viewerBadge_container__r5tak {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
        [data-testid="stActionButtonIcon"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
        [data-testid="stActionButtonLabel"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
        [data-testid="stHeader"] {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.empty()

