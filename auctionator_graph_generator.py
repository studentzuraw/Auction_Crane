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

MERGED_FILE = r"C:\Users\user\Desktop\Work\auctionator_output_merged.csv"
ITEM_DATA = r"C:\Users\user\Desktop\Work\item_data.csv"


def generate_item_data():
    """
    Read merged file and extract desired item data
    Sort data frame by time and save to item data csv file
    """
    if os.path.isfile(MERGED_FILE):
        # Extract data for specified item
        data_frame = pd.read_csv(MERGED_FILE, parse_dates=[0], dayfirst=True)
        data_frame.sort_values(by="DATE OF SCAN")
        item = data_frame[data_frame["ITEM NAME"] == GIVEN_ITEM_NAME]
        item.to_csv(ITEM_DATA, encoding="utf-8", index=False)
        print("Generating item data for " + GIVEN_ITEM_NAME)


def plot_price_change(
    x_axis, y_axis, latest_price, latest_price_date, trend, trend_coef
):
    """
    Plotting function
    """
    if os.path.isfile(ITEM_DATA):

        _, a_x = plt.subplots(figsize=(15, 8), dpi=80)
        a_x.set(ylabel="Price [gold]")
        title = GIVEN_ITEM_NAME + "\nPrice Over Time"
        plt.title(title, loc="left", fontsize=18, pad=20)
        a_x.plot(x_axis, y_axis, linestyle="dashed", marker="o", color="purple")

        a_x.xaxis.set_major_formatter(DateFormatter("%d-%m-%Y"))
        plt.setp(a_x.get_xticklabels(), rotation=30, ha="right")
        plt.grid(color="green", linestyle="--", linewidth=0.5)

        if trend_coef > 0:
            trend_string = "Rising"
            color = "green"
        elif trend_coef == 0:
            trend_string = "Stable"
            color = "yellow"
        elif trend_coef < 0:
            trend_string = "Decreasing"
            color = "red"

        latest_price = latest_price * 10000
        gold = int(latest_price / 10000)
        silver = int((latest_price - (gold * 10000)) / 100)
        bronze = int(latest_price - (gold * 10000) - (silver * 100))
        latest_price_prettyfied = (
            str(gold) + " Gold " + str(silver) + " Silver " + str(bronze) + " Bronze "
        )
        price_info = (
            "Latest price: "
            + str(latest_price_prettyfied)
            + "\nDated: "
            + str(latest_price_date)
            + "\nPrice trend: "
        )
        plt.gcf().text(0.65, 0.91, price_info, fontsize=12)
        plt.gcf().text(0.715, 0.91, trend_string, fontsize=12, color=color)

        plt.plot(x_axis, trend(x_axis), "r--")
        print("Created plot for " + GIVEN_ITEM_NAME)
        plt.savefig("graph.png")


def calculation_before_plotting(output_item_name):
    """
    Calculation function

    Returns:
        x_axis: x axis for plot - dates
        y_axis: y axis for plot - item prices
        latest_price: item latest price
        latest_price_date: date of item latest price
        trend: trend line for prices
    """
    global GIVEN_ITEM_NAME
    GIVEN_ITEM_NAME = output_item_name
    if os.path.isfile(ITEM_DATA):
        generate_item_data()
        series = pd.read_csv(ITEM_DATA, header=0, index_col=0)

        dates = series.index.values
        x_axis = mdates.date2num(pd.to_datetime(dates))
        y_series = series["ITEM PRICE"].values

        # Change from bronze to gold currency
        y_axis = [x1 / 10000 for x1 in y_series]

        latest_price_date = series.index.values[-1]
        latest_price = y_axis[-1]

        # Define trend line for prices and coefficient
        trend = np.poly1d(np.polyfit(x_axis, y_axis, 1))
        trend_coef = trend.coef[0]  # Polish: Współczynnik kierunkowy prostej
        print("Calulating before plotting for " + GIVEN_ITEM_NAME)
        plot_price_change(
            x_axis, y_axis, latest_price, latest_price_date, trend, trend_coef
        )
        return x_axis, y_axis, latest_price, latest_price_date, trend, trend_coef
