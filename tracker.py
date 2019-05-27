import sys
import os
import sqlite3
import logging


logging.basicConfig(filename="PriceTracker.log", level=logging.NOTSET, format="%(asctime)s %(levelname)s: %(message)s")
logging.getLogger(__name__).addHandler(logging.NullHandler())
__log__ = logging.getLogger(__name__)
idsWithErrors = []

try:
    conn = sqlite3.connect("products.db")
except sqlite3.OperationalError:
    __log__.error("There was an error connecting to the database. Do you have write permissions here?")

__log__.info("Updating products")
cursor = conn.cursor()
cursor2 = conn.cursor()
query = cursor.execute("SELECT * FROM products")
for row in query:
    os.system("curl --silent " + row[2] + " 2>&1 > trackOutput.log")
    f = open("trackOutput.log", mode="r", encoding="utf-8")
    content = f.read()
    splitted = content.split("""<div class="p-current-price">""")
    splitted = splitted[1].split("</div>")
    if """itemprop="price">""" in splitted[0]:
        splitted = splitted[0].split("""itemprop="price">""")
        splitted = splitted[1].split("</span>")
        price = splitted[0]
    elif """itemprop="lowPrice">""" in splitted[0]:
        splitted = splitted[0].split("""itemprop="lowPrice">""")
        splitted2 = splitted[1].split("</span>")
        splitted3 = splitted[1].split("""itemprop="highPrice">""")
        splitted3 = splitted3[1].split("</span>")
        price = splitted2[0] + " - " + splitted3[0]
    else:
        price = None
        __log__.error("Error while filtering the data for productId " + str(row[0]))
    if price is not None and price == row[3]:
        __log__.info("Updated productId " + str(row[0]) + " with the same price: " + price)
    else:
        try:
            if price is None:
                cursor2.execute("UPDATE products SET price=NULL WHERE id= " + str(row[0]))
            else:
                cursor2.execute("UPDATE products SET price = '" + price + "', lastPrice=price WHERE id = " + str(row[0]))
            conn.commit()
            __log__.info("Updated productId " + str(row[0]) + " with the same price: " + price) 
        except sqlite3.OperationalError:
           __log__.error("ERROR WHILE EXECUTING SQL QUERY AND COMITTING CHANGES TO THE DATABASE... EXITING FOR KEEPING DATABASE'S INTEGRITY")
           sys.exit(1)
os.remove("trackOutput.log")

## Update HTML

output = """<table>\n\t\t\t<tr>\n\t\t\t\t<td style="font-weight: bold">Item</td>\n\t\t\t\t<td style="font-weight: bold">Price</td>\n\t\t\t\t<td style="font-weight: bold">Last Price</td>\n\t\t\t</tr>"""
page=open("track_data/index.html", mode="r", encoding="utf-8")
content=page.read()
with open("track_data/index.html", mode="w", encoding="utf-8") as f:
    placeholder = content.split("<table>")
    placeholder = placeholder[1].split("</table>")
    placeholder = "<table>" + placeholder[0] + "</table>"
    query = cursor.execute("SELECT * FROM products")
    for row in query:
        output = output + "\n\t\t\t<tr>\n\t\t\t\t<td>" + row[1] + "</td>\n\t\t\t\t<td>" + str(row[4]) + "</td>\n\t\t\t\t<td>" + str(row[3]) + "</td>\n\t\t\t</tr>"
    output = output + "\n\t\t</table>"
    content = content.replace(placeholder, output)
    f.write(content)