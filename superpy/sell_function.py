"""Because the process to sell things have to use diffrent function and actions,
    I deside to make a separte file from it and import it in the main.py"""

import csv
from datetime import date, datetime, timedelta
import sys
import os
from get_highest_number import get_new_id

# first we want to check if there are items in the inventory

def get_items_to_be_sold():
    items_to_be_sold = []
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():  # Is always an interger
                    price = float(row[3].replace(",", "."))
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    items_to_be_sold.append({"id": int(row[0]),
                                             "product_name": row[1],
                                             "buy_date": datetime.strptime(row[2], '%d%m%Y'),
                                             "buy_price": price,
                                             "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                             "sold": row[5]})
        csvfile.close()
    except:
        None
    return items_to_be_sold

#print(get_items_to_be_sold())

"""Now we will check the oldest sellable item, with the follow function call.
    Why? because you always want to sell the oldest item first. Normally in the supermarket you will do this with FIFO method"""

def get_oldest_sellable_item(items_to_be_sold, args, dates):
    item_found = "N"
    bought_id = 0
    index = -1
    index_found = -1
    bought_price = 0
    # Searching between a match from sell item in inventory. oldest item should be sold first
    for item in items_to_be_sold:
        index = index+1
        if (item["product_name"] == args.product_name and item["expiration_date"] >= dates.today and item["sold"] == "N" and item_found == "N"):
            index_found = index
            item_found = "Y"
            bought_id = item["id"]
            bought_price = item["buy_price"]
    return bought_id, bought_price, index_found

#print(get_oldest_sellable_item(get_items_to_be_sold(), 'milk', '2021-05-28'))

"""After we found the item we want to rewrite the bought.csv file and change the sold row in the sold_Date.
    We will do this because we need this data for the reports, after a talk with Thomas i decide to skip this function"""


def rewrite_bought_file(items_to_be_sold):
    with open('./bought.csv', 'w', newline='') as csvfile:
        bought_items = csv.writer(csvfile, delimiter=';',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in items_to_be_sold:
            bought_items.writerow(
                [str(item["id"])]+[item["product_name"]]+[item["buy_date"].strftime("%d%m%Y")]+[str(item["buy_price"]).replace(".", ",")] +
                [item["expiration_date"].strftime("%d%m%Y")]+[item["sold"]])
    csvfile.close()

def add_sold_item_to_list(max_id, bought_id, args, dates, bought_price):
    success = False
    file_name = os.path.isfile('./sold.csv')
    with open('./sold.csv', 'a', newline='') as csvfile:
        field_names = ['id', 'buy-id', 'product-name', 'sell-date', 'sell-price', 'buy-price']
        sold_items = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if not file_name:
            sold_items.writerow(field_names)
        else:
            pass
        sold_items.writerow(
            [str(max_id)]+[str(bought_id)]+[args.product_name]+[dates.today_str]+[]+[str(args.price).replace(".", ",")] +
            [str(bought_price).replace(".", ",")])
        success = True
    csvfile.close()
    return success


def process_sell_instruction(args, dates):
    items_to_be_sold = []
    args.product_name = args.product_name.lower()
    # Collecting the inventory
    items_to_be_sold = get_items_to_be_sold()
    bought_id, bought_price, index_found = get_oldest_sellable_item(
        items_to_be_sold, args, dates)
    # Put the items in the sold.csv
    if index_found != -1:
        items_to_be_sold[index_found]["sold"] = dates.today_str
    rewrite_bought_file(items_to_be_sold)

    if bought_id == 0:
        success = False  # variabel if the process was successfull
    else:
        max_id = get_new_id("sold.csv")
        success = add_sold_item_to_list(
            max_id, bought_id, args, dates, bought_price)
    return success

