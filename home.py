# =============================================================================
#                              MAIN METHOD DEMO
# =============================================================================
import streamlit as st
# pages
import database
import correlation
import model
import prediction
import conclusion

st.set_page_config(page_title="Stock Database Project - Sam Edwards", page_icon="📊")

st.empty()
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

home = "🏠 Home"
data = "📈 Database"
cor = "🔍 Correlations"
learn = "🦾 ML Model"
predict = "🔮 Predictions"
conclude = "📊 Conclusions"

st.sidebar.write("# Navigation Bar")
menu_radio = st.sidebar.radio(label="Main Menu",options=[home,data,cor,learn,predict,conclude],key='menu')
st.sidebar.write("""
**Click 'Feature Details' on each page!** 💡

Its best to go in this order:
- Database
- Predictions
- Conclusions

for a streamlined understanding of
my project.


**For more info, please reach out**

🧍🏻 Sam Edwards\n
📬 se2584@columbia.edu\n
📞 609.751.1524

""")

if menu_radio == data:
    database.run()
if menu_radio == cor:
    correlation.run()
if menu_radio == learn:
    model.run()
if menu_radio == predict:
    prediction.run()
if menu_radio == conclude:
    conclusion.run()
if menu_radio == home:
    st.write("# 📈 Stock Data Analysis 📉")
    st.write("BY: SAM EDWARDS")
    st.subheader("Pricing Databases and Machine Learning")
    st.write("""
    
Hello! I developed this website to demonstrate the functionality of my built-in stock database and illustrate the 
accuracy of my predictive machine-learning model on trends in the market (using my database of course).


**To simply play with these tools, check out the 'Database' and 'Predictions' tabs of my webapp.**
""")

    st.write("Project Outline:")
    with st.expander('📗\tNavigation'):
        # Display the plot in Streamlit
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

    with st.expander('📕\tGoals'):
        # Display the plot in Streamlit
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

    with st.expander('📘\tInspiration'):
        # Display the plot in Streamlit
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

    with st.expander('📙\tResources and More'):
        st.write("""
        **How I built this website:**
        
        I built this webapp from scratch using solely Python and HTML. I am hosting my app through a python extension
        known as streamlit. 
        I wanted a simplistic look so as to highlight the features and dynamism of my data structures and ML model.
        For a more detailed look at my code, feel free to visit my github at:
        
        https://github.com/samjoredw
        
        **Python libraries used in this project:**
        - numpy
        - matplotlib
        - pandas
        - os and sys
        - requests
        - streamlit
        
        """)

st.empty()

