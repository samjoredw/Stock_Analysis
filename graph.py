import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def graph_stocks(subset_stock1, subset_stock2, name1, name2):

    metric1 = subset_stock1.columns[1]
    metric2 = subset_stock2.columns[1]

    dates1 = np.array(subset_stock1.index.date)
    dates2 = np.array(subset_stock2.index.date)
    data1 = np.array(subset_stock1.values)
    data2 = np.array(subset_stock2.values)

    if len(dates1) >= len(dates2):
        use_dates = dates1
    else:
        use_dates = dates2

    fig1, ax = plt.subplots()

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
    ax.set_xticks(use_dates[::ticks])
    ax.set_xticklabels(use_dates[::ticks], rotation=75)

    ax.legend()

    return fig1

