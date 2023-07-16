"""
Search engine used to search from exact item in csv file
"""
import re
import pandas as pd

MERGED_FILE = r"C:\Users\user\Desktop\Work\auctionator_output_merged.csv"
SAVED_VARIABLES = r"C:\Users\user\Desktop\Work\saved_variables.py"


def sse_search_start(search_input):
    """
    Returning item names matching user input
    """
    item_data = pd.read_csv(MERGED_FILE, index_col=0)["ITEM NAME"]
    input_string = search_input
    input_string = input_string.split(" ")
    for _, line in enumerate(input_string, 1):
        r_var = re.compile(".*" + line, re.IGNORECASE)
        found_items = list(filter(r_var.match, item_data))
        found_items = list(set(found_items))
        item_data = found_items
    found_items.sort()
    return found_items


def sse_pick_item(choose_item, found_items):
    """
    User is choosing item from a list of items
    """
    if len(found_items) != 0:
        input_number = choose_item
        if input_number.isnumeric():
            input_number = int(input_number)
            if input_number < int(len(found_items) + 1):
                output_item_name = found_items[input_number - 1]
                return output_item_name
            else:
                return "ERR: " + "Given number is not in range"
        else:
            return "ERR: " + "Given input is not numeric"
    else:
        return "ERR: " + "No items found"
