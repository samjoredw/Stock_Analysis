import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# BEFORE USING THIS:
# Ensure that subset stocks have been converted to dataframes of
# either size 1 (index, value) or that the required value column has been
# assigned to index[1] beforehand.
def graph_stocks(subset_stock1, subset_stock2, name1, name2):
    metric1 = subset_stock1.columns[0]
    metric2 = subset_stock2.columns[0]

    dates1 = np.array(subset_stock1.index.date)
    dates2 = np.array(subset_stock2.index.date)
    data1 = np.array(subset_stock1.values)
    data2 = np.array(subset_stock2.values)

    # Only relevant in comparison cases not correlation cases
    if len(dates1) >= len(dates2):
        use_dates = dates1
    else:
        use_dates = dates2

    fig, ax = plt.subplots()

    plt.title(f"{name1}: {metric1.upper()} vs. {name2}: {metric2.upper()}")
    plt.ylabel("Price ($)")
    if metric1 == 'Volume':
        plt.ylabel("Trades (100 Million)")
    plt.xlabel("Date")

    # Use actual date arrays for x-axis values
    ax.plot(dates1, data1, 'b-', label=name1)
    ax.plot(dates2, data2, 'r-', label=name2)

    # Set ticks based on the length of the chosen date array
    ticks = int(len(use_dates) / 15)

    try:
        ax.set_xticks(use_dates[::ticks])
    except:
        st.write("Please make sure you are uploading a valid stock csv."
                 "\nEnsure that it has the necessary metrics above and that it has **daily** records!")
        return 0
    ax.set_xticklabels(use_dates[::ticks], rotation=75)

    ax.legend()

    return fig
