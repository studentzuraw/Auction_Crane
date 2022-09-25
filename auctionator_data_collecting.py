"""
Copy Auctionator.lua file from SavedVariables Folder
Extract data for Lorderon Alliance Auction House
Create auctionator_output_*.csv and save data
Merge auctionator_output data with existing data
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

start_time = time.time()

AUCTIONATOR_DATA_FILE_NAME = "Auctionator.lua"

ORIGINAL = (
    r"C:\wow\World of Warcraft 3.3.5a (no install)"
    r"\WTF\Account\U9Y8RB7XZ45CXER\SavedVariables\Auctionator.lua"
)

TARGET = r"C:\Users\krzys\Desktop\Work\Auctionator.lua"

shutil.copyfile(ORIGINAL, TARGET)

MERGED_FILE = "auctionator_output_merged.csv"

# Open Auctionator.lua file
# Receive line numbers for Lordaeron Alliance auction house data
# Receive last scan time
with open(AUCTIONATOR_DATA_FILE_NAME, "r", encoding="utf-8") as f:
    for num, line in enumerate(f, 1):
        if "Lordaeron_Alliance" in line:
            begin_num = num
        elif "Lordaeron_Horde" in line:
            end_num = num - 2
        elif "AUCTIONATOR_LAST_SCAN_TIME" in line:
            auc_lst = line

# Convert Auctionator Last Scan Time
auc_lst_res = re.sub("[" + string.punctuation + "]", "", auc_lst).split()
for i, _ in enumerate(auc_lst_res):
    if auc_lst_res[i].isnumeric():
        auc_lst_time_unix = auc_lst_res[i]

auc_lst_time_date = datetime.fromtimestamp(float(auc_lst_time_unix)).strftime(
    "%d-%m-%Y %H:%M:%S"
)

file_name = r"auctionator_output_" + auc_lst_time_unix + ".csv"

# Open Auctionator.lua and copy data to created auctionator_output.csv file
if last_appended_file != file_name:
    with open(AUCTIONATOR_DATA_FILE_NAME, "r", encoding="utf-8") as f:
        with open(
            r"C:\Users\krzys\Desktop\Work\auctionator_output_"
            + auc_lst_time_unix
            + ".csv",
            "w",
            encoding="utf-8",
        ) as f1:
            writer = csv.writer(f1)
            writer.writerow(["DATE OF SCAN", "ITEM NAME", "ITEM PRICE"])
            for i, line in enumerate(f, 1):
                if i > begin_num:
                    res = re.sub("[" + string.punctuation + "]", "", line).split()
                    ITEM_NAME = ""
                    ITEM_PRICE = ""
                    column_ids = []

                    # Check is word is string or number
                    # Assign string as item_name and number as item_price
                    for x, _ in enumerate(res):
                        if res[x].isnumeric():
                            ITEM_PRICE = res[x]
                        elif type(res[x] == str):
                            ITEM_NAME += res[x]
                            ITEM_NAME += " "
                    ITEM_NAME = "".join(ITEM_NAME.rstrip().lstrip())
                    DATE_OF_SCAN = "".join(auc_lst_time_date)
                    column_ids = [DATE_OF_SCAN, ITEM_NAME, ITEM_PRICE]
                    writer.writerow(column_ids)
                if i == end_num:
                    break
    last_file = pd.read_csv(file_name)
    last_file.to_csv(MERGED_FILE, mode="a", index=False, header=False)

    os.remove(last_appended_file)

    with open(
        "saved_variables.py",
        "w",
        encoding="utf-8",
    ) as fpy:
        fpy.write(
            'last_appended_file = "auctionator_output_' + auc_lst_time_unix + '.csv"'
        )
else:
    print("File is already merged")

os.remove("Auctionator.lua")

end_time = time.time()
program_time = str(end_time - start_time)

print("--- " + program_time + " seconds ---")
