STOCK DATABASE PROJECT
Sam Edwards
2023

How to use this program:
============================================================================
This project is web based. Therefore, to run this project you can go to
https://samjoredw-stock-analysis-home-mwbstx.streamlit.app/. To interact
with the database, you can modify the variables: stock, metric, and date.
When you submit your search in the database. Two tabs will load at the bottom
of the web page. Click on each tab to view data about your choice.
Additionally, you can upload your own data in the form of a .csv file. The
recommended resource for stock csv files is through yahoo finance. In doing
so, you can find stock data for each specific company under the
"Historical Data" tab under the stock symbol. Download it to your computer
and enter the file into the database by using the upload box.

What this program does:
============================================================================
This program has a database of seven chosen stocks. Each stock has data
spanning more than 10 years. When you select two stocks to use and two
specified dates, the algorithm will find the most correlated 180 days within
that range where your two metrics correlate the most. In doing so, a graph
will be shown of this specific 180 days with both stocks present. Additionally,
there will be another tab giving some general information on the correlation.

How I created this project:
============================================================================
I created this program using only python and html. The web app is hosted
through streamlit, a python extension that streamlines the frontend process.
I first created a way to load and assign the database to a dictionary of
pandas DataFrames and then embedded this database into the frontend of my
project.
The stock_dictionary.py and stock_instance.py files work together to load the
data into the program and read the list of files I have stored in a directory
called /stock_data. Additionally, within the /stock_data directory, there is a
file called alpha_vantage_down.py which can be used to download any active
company's stock into the current working directory by its own stock symbol.
The features.py file contains the bulk of the algorithmic necessities for
accessing the database and cleaning/altering the raw data. The database.py and
correlation.py files are used to embed the data into the streamlit program.
The graph.py file implements the graph interface. Finally, home.py serves as
the frontend for my program making some html modifications and calling
functions from the other files in the source code.

Requirements:
============================================================================
To see the exact versions of each import required for this project, see the
requirements.txt file located in this project. Here are a list of the required
imports to run this project:
- numpy
- pandas
- matplotlib
- streamlit
- pillow
- requests
Please note that the requests library is only required to run
alpha_vantage_down.py to import new stocks into the database.