import calendar
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.style import Style

"""Ïn this file will all the reports made. We have reports for inventory, renvenue and profit.
    The data from this reports are collect in the main file main.py.
"""
def table_heading(purpose, rep, start_date, end_date):
    if purpose == "Revenue" or purpose == "Profit":
        if start_date == end_date:
            rep.print(f"{purpose} report for date " +
                      start_date.strftime('%d-%m-%Y'), style="red on white")
        else:
            rep.print(f"{purpose} report for the month " +
                      calendar.month_name[start_date.month], style="red on white")
    else:
        rep.print(f"{purpose} part", style="red on white")

def report_sell_part_table(sold_items, start_date, end_date):
    console = Console()
    table = Table(show_header=True, header_style="bold", show_lines=False)
    table.add_column("sold id", style="dim", width=10)
    table.add_column("buy id ", style="dim", width=10)
    table.add_column("product name", style="dim", width=30)
    if start_date != end_date:
        table.add_column("sell date", style="dim", width=30)
    table.add_column("buy price in eur", style="dim", width=20)
    table.add_column("sold price in eur", style="dim", width=20)
    sales_reportable = "N"

    for item in sold_items:
        sales_reportable = "Y"
        if start_date == end_date:
            table.add_row(item['id'],
                          item['buy_id'],
                          item['product_name'],
                          str('%.2f' % item['buy_price']).replace('.', ','),
                          str('%.2f' % item['sell_price']).replace('.', ','))
        else:
            table.add_row(item['id'],
                          item['buy_id'],
                          item['product_name'],
                          str(item['sell_date'].strftime("%d-%m-%Y")),
                          str('%.2f' % item['buy_price']).replace('.', ','),
                          str('%.2f' % item['sell_price']).replace('.', ','))
    if sales_reportable == "Y":
        console.print(table)
    else:
        if start_date == end_date:
            console.print(
                f"No sales reportabele for date {start_date.strftime('%d-%m-%Y')}", style="red on white")
        else:
            console.print(
                f"No sales reportable for the month {calendar.month_name[start_date.month]}")
    return sales_reportable

def report_sell_part(purpose, sold_items, start_date, end_date, total_amount_sold):
    # This function will used for revenue and profit, because selling items are used by both.
    console = Console()
    if purpose == "Revenue":
        table_heading("Revenue", console, start_date, end_date)
    else:
        table_heading("Sell", console, start_date, end_date)
    sales_reportable = report_sell_part_table(sold_items, start_date, end_date)

    if sales_reportable == "Y":
        sold_tot_amount = str('%.2f' % round(
            total_amount_sold, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(69), end="")
            console.print(
                f"Total sold eur {sold_tot_amount}", style="red on white")
        else:
            print(''.ljust(85), end="")
            console.print(
                f"Total sold eur {sold_tot_amount}", style="red on white")

def make_report_profit_table(purchased_items, start_date, end_date, total_amount_bought):
    # This function makes on base from purchased items table, the corresponding table.
    table = Table(show_header=True, header_style="bold", show_lines=False)
    console = Console()
    table_heading("Bought", console, start_date, end_date)
    table.add_column("buy id", style="dim", width=22)
    table.add_column("product name", style="dim", width=35)
    if start_date != end_date:
        table.add_column("buy date", style="dim", width=34)
    table.add_column("expiration date", style="dim", width=25)
    table.add_column("buy price in eur", style="dim", width=25)
    purchases_reportable = "N"
    for item in purchased_items:
        purchases_reportable = "Y"
        if start_date == end_date:
            table.add_row(item['id'],
                          item['product_name'],
                          item['expiration_date'].strftime('%d-%m-%Y'),
                          str('%.2f' % item['price']).replace('.', ','))
        else:
            table.add_row(item['id'],
                          item['product_name'],
                          item['buy_date'].strftime('%d-%m-%Y'),
                          item['expiration_date'].strftime('%d-%m-%Y'),
                          str("%.2f" % item['price']).replace('.', ','))
    # The upper statement makes always a table if there is a product in purchased_items is, if this is empty there will be a text that there are no items
    if purchases_reportable == "Y":
        console.print(table)
        bought_tot_amount = str('%.2f' % round(
            total_amount_bought, 2)).replace('.', ',')
        if start_date == end_date:
            print(''.ljust(65), end="")
            console.print(
                f"Total purchased eur {bought_tot_amount}", style="red on white")
        else:
            print(''.ljust(77), end="")
            console.print(
                f"Total purchased eur {bought_tot_amount}", style="red on white")
    else:
        if start_date == end_date:
            console.print(
                f"No purchases reportable for date {start_date.strftime('%d-%m-%Y')}", style="red on white")
        else:
            console.print(
                f"No purches reportable for the month {calendar.month_name[start_date.month]}", style="red on white")

def make_report_profit(sold_items, purchased_items, expired_items,
                       total_amount_sold, total_amount_bought, total_amount_perished, start_date,
                       end_date):

    # This report consists of two parts : one for the sale and one for the purchase
    console = Console()
    table_heading("Profit", console, start_date, end_date)

    # sell_part
    report_sell_part("Sell", sold_items, start_date,
                     end_date, total_amount_sold)

    # bought_part
    make_report_profit_table(purchased_items, start_date,
                             end_date, total_amount_bought)

    profit = str('%.2f' % round(total_amount_sold -
                                total_amount_bought, 2)).replace(".", ",")
    if start_date == end_date:
        console.print(
            f"The total profit on date {start_date.strftime('%d-%m-%Y')} equals eur {profit}", style="red on white")
    else:
        console.print(
            f"The total profit for the month {calendar.month_name[start_date.month]} equals eur {profit}", style="red on white")

def make_report_revenue(sellData, total_amount_sold, start_date, end_date):
    # total sell
    report_sell_part("Revenue", sellData, start_date,
                     end_date, total_amount_sold)

def make_report_inventory(inventory_data, ref_date):
    # inventory
    console = Console()
    console.print(
        f"Inventory on {ref_date.strftime('%d-%m-%Y')}", style="red on white")
    if len(inventory_data) == 0:
        print("There's no inventory on this date")
    else:
        table = Table(show_header=True, header_style="bold", show_lines=False)
        table.add_column("Product name", style="dim", width=30)
        table.add_column("Count")
        table.add_column("Buy price in eur", justify="right")
        table.add_column("Expiration date", justify="right")
        if isinstance(inventory_data, dict):
            for k, v in inventory_data.items():
                product_name = k
                if isinstance(v, dict):
                    value = v
                    for k, v in value.items():
                        expiry_date_str = k
                        if len(expiry_date_str) == 7:
                            expiry_date_str = "0"+expiry_date_str
                        expiry_date = datetime.strptime(
                            expiry_date_str, "%d%m%Y")
                        value = v
                        if isinstance(v, dict):
                            for k, v in value.items():
                                buy_price = k
                                # The key for the price is a string in the dictionary.
                                # That's why I need to take care of the two decimal behind the . and also the , 
                                number = v
                                buy_price_number = float(buy_price)
                                table.add_row(product_name,
                                              str(number),
                                              str("%.2f" % buy_price_number).replace(
                                                  '.', ','),
                                              expiry_date.strftime("%d-%m-%Y"),)
        console.print(table)