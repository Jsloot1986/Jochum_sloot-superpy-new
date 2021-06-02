Technically highlights points.

1. To put in the bought.csv the date when the item is sold.
    I would first work with DictReader and DictWriter. I could make the csv files but after selling products the bought.csv was empty.
    And i also wanted to change the date in bought.csv to the sold-date(this is the last column, if not sold it's a 'N' otherwise the date).
    So after a talk with Thomas, he advice me to cancel the step for changing the bought.csv.
    But I really wanted that it should work so I tested with only the simple version read and write. after this i could change the date.
    I get it work with the function rewrite_bought_file. It's get his arrguments from the items_to_be_sold what will be set in the function process_sell_function. The product what is been sold will overwrite the product with the first expiration-date and change the column['sold'] from a 'N' to the sold-date. I still don't know why it didn't work with the DictWriter. But at least it's working now.

2. The handy errors what will be in the CLI if you typt something wrong.
    If you type something wrong, the system helps you what was wrong and also confrom what was happening.
    It's not really something special but I think with clear messages everyone will understand what was going wrong.

3. The Statistics in a barcharts or linecharts. 
    I also figure out how to make barcharts and linecharts. So if there is data in the sold.csv or bought.csv there can be made charts.
    The command stats --product-name xxxx start-date xxxx-xx-xx end-date xxxx-xx-xx and combinate this with the commando
    --number will give you the total of sold items from that product
    --buy-price will give you the bought-price of that product(also you can see if a price was bought higher of lower than before)
    --sell-price will give you the sell-price of that product(also you can see if the price of selling was higher or lower before)
    --revenue will give you the daily revenue of that product
    --profit will give you the daily profit of the product
    The profit is in a linechart because this is better to see than a barchart. notice that the x-axis is scaled for 3 hours a day. so you can also see when you sold the most (if you really gonna use this in a supermarket)

closing word.
It costs me alot of "bloed, zweet en tranen"(It's a dutch saying).
But I finished and I'm proud with the end result. I made diffrent versions and this version is the last one.
I think it is handy to make a README with a short explanation, so you can start right away. because the PDF is very long and sometimes you just want a short explanation. I learned alot with this porject and it felt a little bit that I just have figure out alot of things.
But you learn alot of this way.