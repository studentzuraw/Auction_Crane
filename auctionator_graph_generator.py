"""
Generate data for specific item
Calculate values for graph
Graph data
"""

import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np

MERGED_FILE = r"C:\Users\krzys\Desktop\Work\auctionator_output_merged.csv"
ITEM_DATA = r"C:\Users\krzys\Desktop\Work\item_data.csv"

ITEM_NAME = "Blood Queens Crimson Choker"


def generate_item_data():
    """
    Read merged file and extract desired item data
    Sort data frame by time and save to item data csv file
    """
    if os.path.isfile(MERGED_FILE):
        # Extract data for specified item
        data_frame = pd.read_csv(MERGED_FILE)
        data_frame.sort_values(by="DATE OF SCAN")
        item = data_frame[data_frame["ITEM NAME"] == ITEM_NAME]
        item.to_csv(ITEM_DATA, encoding="utf-8", index=False)


def plot_price_change():
    """
    Plotting function
    """
    if os.path.isfile(ITEM_DATA):

        (
            x_axis,
            y_axis,
            latest_price,
            latest_price_date,
            trend,
            trend_coef,
        ) = calculation_before_plotting()
        fig, a_x = plt.plot(figsize=(15, 8), dpi=80)
        a_x.set(ylabel="Price [gold]")
        title = (
            ITEM_NAME
            + "\nPrice Over Time"
        )
        plt.title(title,loc="left",fontsize=18, pad=20)
        a_x.plot(x_axis, y_axis, linestyle="dashed", marker="o", color="purple")

        a_x.xaxis.set_major_formatter(DateFormatter("%m-%d-%Y"))
        a_x.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        plt.setp(a_x.get_xticklabels(), rotation=30, ha="right")
        plt.grid(color="green", linestyle="--", linewidth=0.5)

        if trend_coef > 0:
            trend_string = "Rising"
            color="green"
        elif trend_coef == 0:
            trend_string = "Stable"
            color="yellow"
        elif trend_coef < 0:
            trend_string = "Decreasing"
            color="red"

        price_info = ("Latest price: "
            + str(latest_price)
            + " Gold"
            + "\nDated: "
            + str(latest_price_date)
            + "\nPrice trend: ")
        plt.gcf().text(0.7, 0.9, price_info, fontsize=14)
        plt.gcf().text(0.775, 0.9, trend_string, fontsize=14,color=color)

        plt.plot(x_axis, trend(x_axis), "r--")

        plt.savefig("foo.png")
        plt.show()


def calculation_before_plotting():
    """
    Calculation function

    Returns:
        x_axis: x axis for plot - dates
        y_axis: y axis for plot - item prices
        latest_price: item latest price
        latest_price_date: date of item latest price
        trend: trend line for prices
    """
    if os.path.isfile(ITEM_DATA):

        series = pd.read_csv(ITEM_DATA, header=0, index_col=0)

        dates = series.index.values
        x_axis = mdates.date2num(pd.to_datetime(dates))
        y_series = series["ITEM PRICE"].values

        # Change from bronze to gold currency
        y_axis = [x1 / 10000 for x1 in y_series]

        latest_price_date = min(dates)
        latest_price = y_axis[-1]

        # Define trend line for prices and coefficient
        trend = np.poly1d(np.polyfit(x_axis, y_axis, 1))
        trend_coef = trend.coef[0]  # Polish: Współczynnik kierunkowy prostej

        return x_axis, y_axis, latest_price, latest_price_date, trend, trend_coef
    return None

def main():
    """
    Main Function to start functions
    """
    generate_item_data()
    plot_price_change()


if __name__ == "__main__":
    main()
