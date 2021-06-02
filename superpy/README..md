Welcome at my super py project.

Superpy is a program by means of which the administration of a supermarket can be kept. The program can accept several kinds of cli (command line interface) commands. A cli command is simply a string of several arguments by means of which the program main.py will carry out a specific instruction.

This is how you can start with super PY (check the pdf manual for the long discription).
Notice that I'm using py (this depends on the system) if you get an Error just use python.
for help use:
py main.py --help or py main.py --h

1. Start to set the date in the past 
py main.py --advance-time -x (number, have to be 1 or more and not -1)(Notice that to set the start date you have to use one time the -x(x=amount of days in the past))

2. You have to filling the inventory to buy things add every single product with the follow command.
x = the name
e = price
d = day
m = month
y = year

py main.py buy --product-name xxxx --price e.ee --expiration-date yyyy-mm-dd
example:
py main.py buy --product-name milk --price 0.30 --expiration-date 2021-05-20

3. Check the bought.csv what is made
column[1]: unique ID
column[2]: product-name
column[3]: purchase-date(bought-date)
column[4]: price
column[5]: expiration-date
column[6]: sold (if not sold = False, if sold = sold-date)

4. Sell a couple of items what's in bought.csv
x = name
e = price
py main.py sell --product-name xxxx --price e.ee
example:
py main.py sell --product-name milk --price 0.80

5. Check the bought.csv if the sold column[6] has the sold price instead of the False.

6. Checkin the sold.csv what is made
column[1]: unique ID
column[2]: related buying ID
column[3]: product-name
column[4]: selling-date (dd-mm-yyyy)
column[5]: sold price
column[6]: bought price

7. Reporting 
You can make 3 kind of reports (inventory, revenue and profit)

inventory report
py main.py report inventory --now (makes report till now)
py main.py report inventory --yesterday (makes report from yesterday)
py main.py report inventory --date yyyy-mm-dd (makes report from given day)

revenue report
py main.py report revenue --today (makes report from today)
py main.py report revenue --yesterday (makes report from yesterday)
py main.py report revenue --date yyyy-mm (makes report from given month, notice that we can't make it from 1 day because you use the previous command for this)

profit report
py main.py report profit --today (makes report from today)
py main.py report profit --yesterday (makes report from yesterday)
py main.py report profit --date yyyy-mm (makes report from given month, notice that we can't make it from 1 day because you use the previous command for this)

8. statistics
py main.py stats --product-name xxxx --start-date yyyy-mm-dd --end-date yyyy-mm-dd zzzzzzzzz

for zzzzzz you can place the follow commands:
--number (fluctuation of sold numbers on different dates)
--buy-price (fluctuation of the average daily price for which the goods are bought)
--sell-price (fluctuation of the average price for which the goods are sold)
--revenue (fluctuation of the daily revenue)
--profit (fluctuation of the daily profit)