"""
Copy Auctionator.lua file from SavedVariables Folder
Extract data for Lorderon Alliance Auction House
Create auctionator_output_*.csv and save data
Append auctionator_output_*.csv data to existing auctionator_output_merged.csv
"""
from datetime import datetime
import re
import string
import csv
import os
import shutil
import time
import pandas as pd
from saved_variables import last_appended_file

AUCTIONATOR_DATA_FILE_NAME = "Auctionator.lua"

ORIGINAL_FILE_PATH = (
    r"C:\wow\World of Warcraft 3.3.5a (no install)"
    r"\WTF\Account\login\SavedVariables\Auctionator.lua"
)

TARGET_FILE_PATH = r"C:\Users\user\Desktop\Work\Auctionator.lua"

MERGED_FILE = r"C:\Users\user\Desktop\Work\auctionator_output_merged.csv"

SAVED_VARIABLES = r"C:\Users\user\Desktop\Work\saved_variables.py"


def auc_entry_process():
    """
    Open Auctionator.lua file
    Search for line number containing start, end and auction last time number
    Return file creation time unix/date format
    """
    # Get needed line numbers for start, end and scan time
    with open(AUCTIONATOR_DATA_FILE_NAME, "r", encoding="utf-8") as file_1:
        for line_num, line in enumerate(file_1, 1):
            if "AUCTIONATOR_PRICE_DATABASE" in line:
                begin_num = line_num + 2
            elif "AUCTIONATOR_MEAN_PRICE_DATABASE" in line:
                end_num = line_num - 3
            elif "AUCTIONATOR_LAST_SCAN_TIME" in line:
                auc_lst_res = re.sub("[" + string.punctuation + "]", "", line).split()

        # Convert full line to auctioner last scan time in unix format
        for line_num, _ in enumerate(auc_lst_res):
            if auc_lst_res[line_num].isnumeric():
                auc_lst_time_unix = auc_lst_res[line_num]

        # Convert Auctionator Last Scan Time from unix time format to date time format
        auc_lst_time_date = datetime.fromtimestamp(float(auc_lst_time_unix)).strftime(
            "%d-%m-%Y %H:%M:%S"
        )
    return begin_num, end_num, auc_lst_time_unix, auc_lst_time_date


def auctionator_data_processing():
    """
    Open Auctionator.lua file
    Receive line numbers for Lordaeron Alliance auction house data
    Receive last scan time
    """

    begin_num, end_num, auc_lst_time_unix, auc_lst_time_date = auc_entry_process()
    file_name = r"auctionator_output_" + auc_lst_time_unix + ".csv"

    with open(AUCTIONATOR_DATA_FILE_NAME, "r", encoding="utf-8") as file_1:
        if last_appended_file != file_name:
            with open(
                file_name,
                "w",
                encoding="utf-8",
            ) as file_2:
                writer = csv.writer(file_2)
                writer.writerow(["DATE OF SCAN", "ITEM NAME", "ITEM PRICE"])
                for line_num1, line in enumerate(file_1, 1):
                    if line_num1 > begin_num:
                        res = re.sub("[" + string.punctuation + "]", "", line).split()
                        item_name = ""
                        item_price = ""

                        # Check is word is string or number
                        # Assign string as item_name and number as item_price
                        for line_num2, _ in enumerate(res):
                            if res[line_num2].isnumeric():
                                item_price = res[line_num2]
                            elif type(res[line_num2] == str):
                                item_name += res[line_num2]
                                item_name += " "
                        item_name = "".join(item_name.rstrip().lstrip())
                        writer.writerow([auc_lst_time_date, item_name, item_price])
                    if line_num1 == end_num:
                        break
            pd.read_csv(file_name).to_csv(
                MERGED_FILE, mode="a", index=False, header=False
            )

            os.remove(last_appended_file)
            sub_str = "last_appended_file = "
            sub_str.split(last_appended_file)

            with open(SAVED_VARIABLES, "r", encoding="utf-8") as file_3:
                saved_vars = file_3.read()

            with open(SAVED_VARIABLES, "w", encoding="utf-8") as file_3:
                saved_vars = saved_vars.replace(last_appended_file, file_name)
                file_3.write(saved_vars)

        else:
            print("File is already merged")

    os.remove("Auctionator.lua")


def copy_file():
    """
    Open Auctionator.lua and copy data to created auctionator_output.csv file
    """
    shutil.copyfile(ORIGINAL_FILE_PATH, TARGET_FILE_PATH)


def main():
    """
    Main function
    """
    start_time = time.time()

    copy_file()
    auctionator_data_processing()
    end_time = time.time()
    program_time = str(end_time - start_time)

    print("--- " + program_time + " seconds ---")


if __name__ == "__main__":
    main()
