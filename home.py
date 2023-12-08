# =============================================================================
#                                 HOME PAGE 
#                               -------------
#      Serves as a main page demo for my project using streamlit and html.
# =============================================================================
import streamlit as st
# pages
import database
import correlation
import model
import prediction
import conclusion

# -----------------------------------------------------------------------------
# This serves as the homepage of my project. It initializes a list of pages
# that can be navigated though to see different elements of my project.
# The home page also offers general information about my project and some 
# recourses.
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

# Page key identifiers:
cor = "🔍 Correlations"
predict = "🔮 Predictions"

st.sidebar.write("# Navigation Bar")
menu_radio = st.sidebar.radio(label="Main Menu",options=[cor,predict],key='menu')
st.sidebar.write("""
**For more info, please reach out**

🧍🏻 Sam Edwards\n
📬 se2584@columbia.edu\n
📞 609.751.1524

""")

if menu_radio == predict:
    prediction.run()
if menu_radio == cor:
    st.subheader("Stock Database")
    st.write("""
    
Hello! I developed this website to demonstrate the functionality of my built-in stock database and illustrate the 
accuracy of my predictive machine-learning model on trends in the market (using my database of course).

This database GUI helps you finds trends in the market between two different stocks. Choose a date range and the 
database will show you the 180 day period with the highest correlation.
""")
    correlation.run()

st.empty()

