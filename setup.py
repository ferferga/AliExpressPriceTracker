import os
import sys
import sqlite3

loop = 0
print("ferferga - Price Tracker setup tool\n\n")

try:
    conn = sqlite3.connect("products.db")
except:
    print("Error while creating database, you likely don't have rights to write in this directory")
    sys.exit(1)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, alias TEXT, link TEXT, lastPrice TEXT, price TEXT)")
conn.commit()

while True:
    try:
        print("Available options:\n")
        print("1. See tracked products")
        print("2. Modify alias of tracked products")
        print("3. Remove tracked products")
        print("4. Add products to track")
        print("5. Save all the changes and exit")
        answer = input("\n\nYour option> ")
        if int(answer) == 1:
            print("\n\nTracked products: ")
            print("|ID           | Alias             | Link")
            query = cursor.execute("SELECT * FROM products")
            for row in query:
                print("| " + str(row[0]) + " | " + str(row[1]) + " | " + str(row[2]))
            print("\n\nNothing else to do. Going back to main menu\n\n")
        elif int(answer) == 2:
            print("\n\n(You need to know the ID of the product do you want to modify. You can see it by pressing CTRL + C and choosing option 1)")
            identifier = input("ID of the element to modify: ")
            alias = input("Type the new alias of the product: ")
            try:
                cursor.execute("UPDATE products SET alias = '" + str(alias) + "' WHERE id = '" + str(identifier) + "'")
                conn.commit()
                print("Data saved succesfully into the database! Going back to main menu...\n\n")
            except sqlite3.OperationalError:
                print("Some data was given in an incorrect format. Your changes were discarded. Going back to main menu:\n\n")
        elif int(answer) == 3:
            print("\n\n(You need to know the ID of the product do you want to modify. You can see it by pressing CTRL + C and choosing option 1)")
            identifier = input("ID of the element to modify: ")
            try:
                cursor.execute("DELETE FROM products WHERE id = " + str(identifier))
                conn.commit()
                print("Data saved succesfully into the database! Going back to main menu...\n\n")
            except sqlite3.OperationalError:
                print("Some data was given in an incorrect format. Your changes were discarded. Going back to main menu:\n\n")
        elif int(answer) == 4:
            print("\n\nAdding new products to the database... Press CTRL + C to go back whenever you are done.")
            while True:
                try:
                    alias = input("\n\nType the alias of your new product: ")
                    link = input("Type the AliExpress' link to your product: ")
                    reg = (None, alias, link, None, None)
                    try:
                        cursor.execute("INSERT INTO products VALUES(?,?,?,?,?)", reg)
                        conn.commit()
                    except sqlite3.OperationalError:
                        print("\nThere was an error saving data into the database. Check that the data is correct")
                except KeyboardInterrupt:
                    print("Data saved into the database. Going back to main menu\n\n")
                    break
        elif int(answer) == 5:
            try:
                conn.commit()
                print("All done! Bye!")
                break
            except sqlite3.OperationalError:
                print("\nThere was an error saving data into the database. Aborting and exiting...")
    except KeyboardInterrupt:
        continue
