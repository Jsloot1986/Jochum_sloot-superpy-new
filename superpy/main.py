# Imports
import argparse
import csv
from datetime import timedelta, datetime
import os
from types import SimpleNamespace as Namespace

from process_stats_function import process_stats
from make_report_function import make_report_profit, make_report_inventory, make_report_revenue
from sell_function import process_sell_instruction
from print_helplist import print_helplist
from get_highest_number import get_new_id

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
"""We need a class to set the date, so we can use it for the buy and sell functions"""
class setDates:
    def __init__(self, day):
        self.today = day
        self.yesterday = self.today+timedelta(days=-1)
        self.tomorrow = self.today+timedelta(days=1)
        self.fortnight_day = self.today+timedelta(days=2)
        self.today_str = self.today.strftime('%d%m%Y')
        self.yesterday_str = self.yesterday.strftime('%d%m%Y')
        self.tomorrow_str = self.tomorrow.strftime('%d%m%Y')
        self.fortnight_day_str = self.fortnight_day.strftime('%d%m%Y')

def parser_():
    parser = argparse.ArgumentParser(add_help=False)
    subparser = parser.add_subparsers(dest='command')
    buy = subparser.add_parser('buy')
    buy.add_argument('--product-name', type=str)
    buy.add_argument('--price', type=float)
    buy.add_argument('--expiration-date', type=str)
    sell = subparser.add_parser('sell')
    sell.add_argument('--product-name', type=str)
    sell.add_argument('--price', type=float)
    report = subparser.add_parser("report")
    subparser_subdivided = report.add_subparsers(dest="command")
    inventory = subparser_subdivided.add_parser("inventory")
    inventory.add_argument("--now", action="store_true")
    inventory.add_argument("--yesterday", action="store_true")
    inventory.add_argument("--date", type=str)
    revenue = subparser_subdivided.add_parser("revenue")
    revenue.add_argument("--yesterday", action="store_true")
    revenue.add_argument("--today", action="store_true")
    revenue.add_argument("--date", type=str)
    profit = subparser_subdivided.add_parser("profit")
    profit.add_argument("--yesterday", action="store_true")
    profit.add_argument("--today", action="store_true")
    profit.add_argument("--date", type=str)
    parser.add_argument("--advance-time", type=int)
    parser.add_argument("--reset-date", action="store_true")
    parser.add_argument("--h", action="store_true")
    parser.add_argument("--help", action="store_true")
    stats = subparser.add_parser("stats")
    stats.add_argument("--product-name", type=str)
    stats.add_argument("--start-date", type=str)
    stats.add_argument("--end-date", type=str)
    stats.add_argument("--number", action="store_true")
    stats.add_argument("--buy-price", action="store_true")
    stats.add_argument("--sell-price", action="store_true")
    stats.add_argument("--profit", action="store_true")
    stats.add_argument("--revenue", action="store_true")
    return parser.parse_args()

"""First we want to set the date. This can be the date for today,
    because we want to test the superpy we will set the date back.
    Thats why I make a function to reset the date."""
def get_referred_date(shift_number_of_days=0, reset='N'):
    #the first parameter is for to set the day backwords(or to the next day)
    #the second parameter is to reset the referred_day to system date
    f_get_date = None
    date_validated = 'N'
    try:
        f = open('referred-date.txt', 'r')
        date_line = f.readline().lstrip()[0:10]
        f_get_date = datetime.strptime(date_line, '%d%m%Y')
        f.close()
    except:
        this_moment = datetime.now()
        this_moment_str = this_moment.strftime('%d%m%Y')
        f_get_date = datetime.strptime(this_moment_str, '%d%m%Y')
    if shift_number_of_days != 0:
        f_get_date = f_get_date+timedelta(shift_number_of_days)
    elif reset == 'Y':
        f_get_date = datetime.strptime(datetime.now().strftime('%d%m%Y'), '%d%m%Y')
    f = open('./referred-date.txt', 'w')
    f.write(f_get_date.strftime('%d%m%Y'))
    f.close()
    date_validated = 'Y'
    return f_get_date, date_validated

#print(get_referred_date(-1, 'N'))

"""Next step is to make a function to put things in the store. So what did you buy for in the supermarket.
   I called this function process_buy_instruction. It need the args and the dates parameter. 
   To test this I will first do it without args and dates en put my own parameters in it. 
   We use success to see if the function did successfully run."""

def process_buy_instruction(args, dates):
    success = False
    max_id = get_new_id("bought.csv")  # getting a new id
    # This function append a row, thats why we use 'a'
    args.product_name = args.product_name.lower()
    file_name = os.path.isfile('./bought.csv')
    with open('./bought.csv', 'a', newline='') as csvfile:
        field_names = ['id', 'product-name', 'buy-date', 'buy-price', 'expiration-date', 'sold(date)']
        bought_item = csv.writer(csvfile, delimiter=';',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        expiration_date = datetime.strptime(args.expiration_date, "%Y-%m-%d")
        if max_id != 0:
            if not file_name:
                bought_item.writerow(field_names)
            else:
                pass
            bought_item.writerow([str(max_id)]+[args.product_name]+[dates.today_str] +
                                 [str(args.price).replace('.', ',')] + [expiration_date.strftime("%d%m%Y")]+["N"])
            success = True
    csvfile.close()
    return success
#print(process_buy_instruction('milk', '2021-05-28', 0.40, '2021-05-30'))

def get_sell_data(start_date, end_date):
    sold_items = []
    total_amount_sold = 0
    try:
        with open('./sold.csv', newline='') as csvfile:
            sold_items_source = csv.reader(
                csvfile, delimiter=';', quotechar='|')
            for row in sold_items_source:
                if row[0].isdigit():
                    if len(row[3]) == 7:
                        row[3] = "0"+row[3]
                    sell_date = datetime.strptime(row[3], "%d%m%Y")
                    if (sell_date >= start_date and sell_date <= end_date):
                        total_amount_sold = total_amount_sold + \
                            float(row[4].replace(",", "."))
                        sold_items.append({"id": row[0],
                                           "buy_id": row[1],
                                           "product_name": row[2],
                                           "sell_price": float(row[4].replace(',', '.')),
                                           "sell_date": sell_date,
                                           "buy_price": float(row[5].replace(',', '.'))})
        csvfile.close()
    except:
        None
    return sold_items, total_amount_sold

def get_bought_data(start_date, end_date):
   # Collecting from bought items and waste items from profit period.
    try:
        purchased_items = []
        total_amount_bought = 0
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():
                    if len(row[2]) == 7:
                        row[2] = "0"+row[2]
                    if len(row[4]) == 7:
                        row[4] = "0"+row[4]
                    buy_date = datetime.strptime(row[2], "%d%m%Y")
                    # check if products been sold in period
                    if (buy_date >= start_date and buy_date <= end_date):
                        purchased_items.append({"id": row[0],
                                                "product_name": row[1],
                                                "price": float(row[3].replace(",", ".")),
                                                "buy_date": buy_date,
                                                "expiration_date": datetime.strptime(row[4], '%d%m%Y'),
                                                "sold ": row[5]})
                        total_amount_bought = total_amount_bought + \
                            float(row[3].replace(",", "."))
        csvfile.close()
    except:
        None
    return purchased_items, total_amount_bought

def raise_inventory_data(product_name, price_str, expiry_date_str, inventoryData):
    # This function will change the table inventoryData with the total amount of item {product_name:{expiry_date:{price:x}}} x is total amount of items.
    if product_name in inventoryData:
        if expiry_date_str in inventoryData[product_name]:
            if price_str.replace(',', '.') in inventoryData[product_name][expiry_date_str]:
                inventoryData[product_name][expiry_date_str][price_str.replace(",", ".")
                                                             ] = inventoryData[product_name][expiry_date_str][price_str.replace(",", ".")]+1
            else:
                inventoryData[product_name
                              ][expiry_date_str][price_str.replace(",", ".")] = 1
        else:
            inventoryData[product_name][expiry_date_str] = {}
            inventoryData[product_name][expiry_date_str
                                        ][price_str.replace(",", ".")] = 1
    else:
        inventoryData[product_name] = {}
        inventoryData[product_name][expiry_date_str] = {}
        inventoryData[product_name][expiry_date_str
                                    ][price_str.replace(",", ".")] = 1
    return inventoryData

def report_inventory_data_and_report(ref_date):
    # The inventory will always be orderd on date. The inventory will be equal on what that is been bought but not be sold on that date and not been waste.
    # The inventory will be made on base before the shops open.
    # The format from inventoryData will be {product (row[1]): {expiratiedate(row[4]):{price[row[3]]:x(total amont(int))
    # ref_date : The controll date
    # row[0]: index
    # row[1]: product_name
    # row[2]: bought date
    # row[3]: price
    # row[4]: expiration date
    # row[5]: N if product isn't be sold, otherwise the solddate
    inventoryData = {}
    try:
        with open('./bought.csv', newline='') as csvfile:
            bought_item = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in bought_item:
                if row[0].isdigit():           # index : index is always integer
                    if len(row[2]) == 7:       
                        row[2] = "0" + row[2]  # boughtdate
                    if len(row[4]) == 7:       # expirationdate
                        row[4] = "0"+row[4]
                    # product is sold before contoll date
                    if datetime.strptime(row[2], "%d%m%Y") < ref_date:
                        checkSell = 'N'  # To check if a product is in stock, it hasn't been sold before the new inventory will start
                        # Product isn't be waste before controll date
                        if row[5] == "N":
                            if datetime.strptime(row[4], "%d%m%Y") < ref_date:
                                None
                            else:
                                checkSell = "Y"
                        else:
                            if len(row[5]) == 7:
                                row[5] = '0'+row[5]
                            if datetime.strptime(row[5], "%d%m%Y") >= ref_date:
                                checkSell = "Y"  # product is sold after controll date
                        if checkSell == "Y":
                            inventoryData = raise_inventory_data(
                                row[1], row[3], row[4], inventoryData)
        csvfile.close()
    except:
        print("the file bought.csv couldn't be opened")
    make_report_inventory(inventoryData, ref_date)

def report_revenue_data_and_report(start_date, end_date):
    # revenue : total amount of sold products in that period
    sellData = []
    sellData, total_amount_sold = get_sell_data(
        start_date, end_date)  # collect sell data
    make_report_revenue(sellData, total_amount_sold,
                        start_date, end_date)  # making the report

def report_profit_data_and_report(start_date, end_date):
    # profit : total sold - total bought from that day - total waste and didn't been sold. You need this to calculate the profit.
    purchased_items = []
    expired_items = []
    sold_items = []
    total_amount_sold = 0
    total_amount_bought = 0
    total_amount_perished = 0
    # caluculate the sell data and calculate the total amount of sold for that day
    sold_items, total_amount_sold = get_sell_data(start_date, end_date)
    # getting the bought data and also the waste data from that period.
    purchased_items, total_amount_bought = get_bought_data(
        start_date, end_date)
    make_report_profit(sold_items, purchased_items, expired_items,
                       total_amount_sold, total_amount_bought, total_amount_perished, start_date, end_date)

def call_on_report(args, called_report, dates, ref_today, subparse_version):
    # This function will help the other function to give the data to them. The profit and revenue repports will use always a start-and end-date.
    # The date from today and yesterday are equal to eachother and have the first and last day from that month from the month reports.
    # The inventory has always a controll date, to calculate the inventory. Techanily the argument --now and --today are equal.
    # I made the optinal paramter --date robust, so you can't give a wrong date.
    if ref_today == True:
        if subparse_version == "inventory":
            called_report(dates.today)
        else:
            called_report(dates.today, dates.today)
    elif args.yesterday == True:
        if subparse_version == "inventory":
            called_report(dates.yesterday)
        else:
            called_report(dates.yesterday, dates.yesterday)
    else:
        if subparse_version == "inventory":
            date_approved = "Y"
            try:
                date_approved = "N"
                ref_date = datetime.strptime(args.date, "%Y-%m-%d")
                date_approved = "Y"
            except:
                print("Date should have the format yyyy-mm-dd")
            if date_approved == "Y":
                called_report(ref_date)
        else:
            date_range_approved = "N"
            try:
                month = datetime.strptime(args.date, '%Y-%m')
                start_date_str = month.strftime("%Y%m")+'01'
                start_date = datetime.strptime(start_date_str, '%Y%m%d')
                end_date = start_date
                # calculate the last day from the month
                end_date = end_date.replace(day=28)
                end_date = end_date+timedelta(days=4)
                end_date = end_date-timedelta(days=end_date.day)
                date_range_approved = "Y"
            except:
                print("date is not a month in yyyy-mm format")
            # If the start and end date can be calculate the variabel data_range_approved is equal to Y
            if date_range_approved == "Y":
                called_report(start_date, end_date)

def main():
    args = parser_()
    if isinstance(args.command, str):
        subparse_version = args.command
    else:
        subparse_version = ""
    if args.advance_time:
        referred_date, date_validated = get_referred_date(args.advance_time)
        if date_validated == 'Y':
            print("OK, referred-date.txt is made")
        else:
            print("NOK, referred-date.txt isn't made")
    else:
        if args.reset_date:
            #The reset is for changing the referred-date to system-date
            referred_date, date_validated = get_referred_date(0, 'Y')
            if date_validated == 'Y':
                print("OK, The referred-date is now the system-date")
            else:
                print("NOK, The system couldn't change the referred-date to system-date")
        else:
            referred_date, date_validated = get_referred_date()
    if args.h == True or args.help == True:
        print_helplist()
    dates = setDates(referred_date)
    if subparse_version == 'buy':
        buy = process_buy_instruction(args, dates)
        if buy == True:
            print("OK, product is add to bought.csv")
        else:
            print("NOK, product couldn't be add to bought.csv")
    elif subparse_version == 'sell':
        sell = process_sell_instruction(args, dates)
        if sell == True:
            print("OK, product is add to sold.csv")
        else:
            print("ERROR! Product isn't in stock")
    # The function call_on_report will be used by all reports. (profit,revenue and inventory).
    # Notice that the parameters from profit and revenue the star- and end-date are equal. And inventory only use one date parameter.
    # Further agreements are that the call with today/now, yesterday. Date for profit and revenue are one month ago and inventory is the controll date
    if subparse_version == "profit":
        call_on_report(args, report_profit_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "revenue":
        call_on_report(args, report_revenue_data_and_report,
                       dates, args.today, subparse_version)

    if subparse_version == "inventory":
        call_on_report(args, report_inventory_data_and_report,
                       dates, args.now, subparse_version)
    # Notice that process_status has diffrent subfuctions, like; number, sell_price, buy_price, revenue en profit
    # That's why I used a seprate file.
    if subparse_version == "stats":
        process_stats(args, dates)      



if __name__ == '__main__':
    main()
