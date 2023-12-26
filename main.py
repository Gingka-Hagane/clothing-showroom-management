import mysql.connector 
from datetime import datetime

# Initialize MySQL Connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul2366",
    database="offline_shopping_management_system"
)
cursor = conn.cursor()

def customer_purchase_history():
  global cursor, conn

  try:
      # Prompt the user for customer ID
      customer_id = int(input("Enter customer ID: "))

      # Check if the customer ID exists in the Customers table
      cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = %s", (customer_id,))
      customer_exists = cursor.fetchone()[0]

      if customer_exists:
          # Prompt the user for the date range
          start_date = input("Enter start date (YYYY-MM-DD): ")
          end_date = input("Enter end date (YYYY-MM-DD): ")

          # Fetch and display purchase history for the specified customer and date range
          cursor.execute("""
              SELECT order_id, order_date, total_amount
              FROM Orders
              WHERE customer_id = %s AND order_date BETWEEN %s AND %s
          """, (customer_id, start_date, end_date))
          order_history = cursor.fetchall()

          if order_history:
              print("\nPurchase History:")
              for order in order_history:
                  order_id, order_date, total_amount = order
                  print("Order ID: {}, Order Date: {}, Total Amount: {}".format(order_id, order_date, total_amount))

                  # Fetch and display purchase items for each order
                  cursor.execute("""
                      SELECT product_id, quantity, payment_mode
                      FROM OrderDetails
                      WHERE order_id = %s
                  """, (order_id,))
                  purchase_items = cursor.fetchall()

                  if purchase_items:
                      print("Purchase Items:")
                      for item in purchase_items:
                          product_id, quantity, payment_mode = item
                          # Fetch and display product name for each product ID
                          cursor.execute("""
                              SELECT name
                              FROM Products
                              WHERE product_id = %s
                          """, (product_id,))
                          product_name = cursor.fetchone()[0]
                          print("Product ID: {}, Quantity: {}, Product Name: {}, Payment Mode: {}".format(product_id, quantity, product_name, payment_mode))
                  else:
                      print("No purchase items found for this order.")

              print("\nEnd of Purchase History.")
          else:
              print("No purchase history found for this customer in the specified date range.")
      else:
          print("Customer not found.")
  except Exception as e:
      print("An error occurred:", str(e))



def modify_product_price():
  global cursor, conn

  try:
      # Display the list of products for user reference
      display_product_info()

      # Prompt the user for the product ID to modify
      product_id_to_modify = int(input("Enter the product ID to modify: "))

      # Check if the product ID exists in the Products table
      cursor.execute("SELECT COUNT(*) FROM Products WHERE product_id = %s", (product_id_to_modify,))
      product_exists = cursor.fetchone()[0]

      if product_exists:
          # Prompt the user for the new price
          new_price = float(input("Enter the new price for the product: "))

          # Update the product price in the Products table
          cursor.execute("UPDATE Products SET price = %s WHERE product_id = %s", (new_price, product_id_to_modify))
          conn.commit()

          print("Product price modified successfully.")
      else:
          print("Product not found.")
  except Exception as e:
      print("An error occurred:", str(e))


def total_sales_on_date():
    global cursor, conn

    try:
        # Prompt the user for the date
        date_str = input("Enter the date (YYYY-MM-DD): ")

        # Convert the input date string to a datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        # Retrieve total sales on the specified date from the Orders table
        cursor.execute("SELECT SUM(total_amount) FROM Orders WHERE DATE(order_date) = %s", (date_obj,))
        total_sales = cursor.fetchone()[0]

        if total_sales is not None:
            print("Total Sales on {}: {}".format(date_str, total_sales))
        else:
            print("No sales data available for the specified date.")
    except Exception as e:
        print("An error occurred:", str(e))


def remove_customer():
  global cursor, conn

  try:
      # Display the list of customers for user reference
      cursor.execute("SELECT customer_id, name, phone_number, email FROM Customers")
      customers = cursor.fetchall()
      for customer in customers:
          customer_id, name, phone_number, email = customer
          print(str(customer_id) + " " + name + " " + str(phone_number) + " " + str(email))

      # Prompt the user for the customer ID to remove
      customer_id_to_remove = int(input("Enter the customer ID to remove: "))

      # Check if the customer ID exists in the Customers table
      cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = %s", (customer_id_to_remove,))
      customer_exists = cursor.fetchone()[0]

      if customer_exists:
          # Remove the customer from the Customers table
          cursor.execute("DELETE FROM orders WHERE customer_id = %s", (customer_id_to_remove,))
          cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id_to_remove,))
          conn.commit()

          print("Customer removed successfully.")
      else:
          print("Customer not found.")
  except Exception as e:
      print("An error occurred:", str(e))


def remove_product():
  global cursor, conn

  try:
      # Display the list of products for user reference
      display_product_info()

      # Prompt the user for the product ID to remove
      product_id_to_remove = int(input("Enter the product ID to remove: "))

      # Check if the product ID exists in the Products table
      cursor.execute("SELECT COUNT(*) FROM Products WHERE product_id = %s", (product_id_to_remove,))
      product_exists = cursor.fetchone()[0]

      if product_exists:
          # Remove the product from the Products table
          cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id_to_remove,))
          conn.commit()

          print("Product removed successfully.")
      else:
          print("Product not found.")
  except Exception as e:
      print("An error occurred:", str(e))


def add_product():
  global cursor, conn

  try:
      # Prompt the user for product details
      name = input("Enter product name: ")
      price = float(input("Enter product price: "))
      quantity = int(input("Enter product quantity: "))

      # Insert the product data into the Products table
      cursor.execute("INSERT INTO Products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
      conn.commit()

      print("Product added successfully.")
  except Exception as e:
      print("An error occurred:", str(e))


# Function to handle customer buying a product and making payment
# Function to add quantity to a product when it's less than 10
def add_quantity():
    global cursor, conn

    try:
        display_product_info()
        # Prompt the user for product ID and quantity to add
        product_id = int(input("Enter product ID: "))
        quantity_to_add = int(input("Enter quantity to add: "))

        # Check the current quantity
        cursor.execute("SELECT quantity FROM Products WHERE product_id = %s", (product_id,))
        current_quantity = cursor.fetchone()[0]

        # Add quantity if it's less than 10
        if current_quantity < 10:
            new_quantity = current_quantity + quantity_to_add
            cursor.execute("UPDATE Products SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
            conn.commit()
            print("Quantity added successfully.")
        else:
            print("Quantity is already sufficient.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to subtract quantity when a customer buys a product
def subtract_quantity():
    global cursor, conn

    try:
        display_product_info()

        # Prompt the user for product ID and quantity to subtract    
        product_id = int(input("Enter product ID: "))
        quantity_to_subtract = int(input("Enter quantity to subtract: "))

        # Check the current quantity
        cursor.execute("SELECT quantity FROM Products WHERE product_id = %s", (product_id,))
        current_quantity = cursor.fetchone()[0]

        # Subtract quantity if there's enough in stock
        if current_quantity >= quantity_to_subtract:
            new_quantity = current_quantity - quantity_to_subtract
            cursor.execute("UPDATE Products SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
            conn.commit()
            print("Quantity subtracted successfully.")
        else:
            print("Not enough quantity in stock.")
    except Exception as e:
        print("An error occurred:", str(e))


# Function to handle customer buying a product and making payment
def buy_product():
    global cursor, conn

    while True:
        try:
            print('product we have:')
            print("\nproduct_id|\t|name|\t\t|price|\t\t|qty|")
            print('-'*75)
            cursor.execute("SELECT product_id, name, price, quantity FROM Products")
            products = cursor.fetchall()
            for product in products:
                product_id, name, price, quantity = product
                print(str(product_id) + "|\t\t|" + name + "|\t|" + str(price) + "|\t|" + str(quantity))


            # Prompt the user for customer ID
            customer_id = int(input("Enter customer ID (0 to exit): "))

            if customer_id == 0:
                break

            # Check if the customer ID exists in the Customers table
            cursor.execute("SELECT COUNT(*) FROM Customers WHERE customer_id = %s", (customer_id,))
            customer_exists = cursor.fetchone()[0]

            if customer_exists:
                # Prompt the user for product ID and quantity
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))

                # Check product availability
                cursor.execute("SELECT name,quantity, price FROM Products WHERE product_id = %s", (product_id,))
                product_data = cursor.fetchone()

                if product_data is not None:
                    name,available_quantity, product_price = product_data

                    if available_quantity >= quantity:
                        # Calculate total cost
                        total_cost = product_price * quantity

                        # Prompt the user for payment mode
                        payment_mode = input("Enter payment mode (Cash/Card): ").strip().lower()

                        if payment_mode in ("cash", "card"):
                            # Update product quantity
                            new_quantity = available_quantity - quantity
                            cursor.execute("UPDATE Products SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
                            conn.commit()

                            # Record the purchase in Orders and OrderDetails tables
                            cursor.execute("INSERT INTO Orders (customer_id, order_date, total_amount) VALUES (%s, NOW(), %s)", (customer_id, total_cost))
                            conn.commit()

                            order_id = cursor.lastrowid

                            cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, amount, payment_mode) VALUES (%s, %s, %s, %s, %s)", (order_id, product_id, quantity, total_cost, payment_mode))
                            conn.commit()
                            print('*'*10,'BILL','*'*10)

                            print('prouduct name:',name)
                            print('product rate:',product_price)
                            print('product qty:',quantity)
                            print('total cost:',total_cost)
                            while True:
                                confirm=input('do to want to confirm the purchase (yes/y) or (no/n):').lower()
                                if confirm == 'yes' or confirm == 'y':
                                    print("Purchase successful!")
                                    break
                                elif confirm == 'no' or confirm == 'n':
                                    print('purchase cancle')
                                    break
                                else:
                                    print('Invaild Choice')
                                    continue
                            return True
                        else:
                            print("Invalid payment mode. Payment failed.")
                    else:
                        print("Not enough quantity in stock.")
                else:
                    print("Product not found.")
            else:
                print("this customer is not found. In our database./n so kindly  register first")
                return False
        except Exception as e:
            print("An error occurred:", str(e))
# Function to return items

def return_items():
    global cursor, conn

    try:
        # Prompt the user for customer phone number
        phone_number = input("Enter customer's phone number: ")

        # Check if the customer phone number exists in the Customers table
        cursor.execute("SELECT customer_id FROM Customers WHERE phone_number = %s", (phone_number,))
        customer_data = cursor.fetchone()

        if customer_data:
            customer_id = customer_data[0]

            # Fetch the items purchased by the customer
            cursor.execute("SELECT order_id, product_id, quantity FROM OrderDetails WHERE order_id IN (SELECT order_id FROM Orders WHERE customer_id = %s)", (customer_id,))
            purchased_items = cursor.fetchall()

            if purchased_items:
                print("\nItems Purchased:")
                for item in purchased_items:
                    order_id, product_id, quantity = item
                    cursor.execute("SELECT name FROM Products WHERE product_id = %s", (product_id,))
                    product_name = cursor.fetchone()[0]
                    print(product_name ,'-', quantity)

                item_to_return = input("Enter the name of the item you want to return: ").capitalize()
                quantity_to_return = int(input("Enter the quantity to return: "))

                # Check if the item is in the purchased items list
                item_found = False
                for item in purchased_items:
                    order_id, product_id, purchased_quantity = item
                    cursor.execute("SELECT name FROM Products WHERE product_id = %s", (product_id,))
                    product_name = cursor.fetchone()[0]

                    if item_to_return == product_name:
                        item_found = True
                        if quantity_to_return <= purchased_quantity:
                            # Update product quantity and remove from purchased items
                            cursor.execute("UPDATE Products SET quantity = quantity + %s WHERE product_id = %s", (quantity_to_return, product_id))
                            purchased_items.remove(item)  # Remove the item from purchased_items
                            conn.commit()

                            # Update the return in OrderDetails
                            cursor.execute("UPDATE OrderDetails SET quantity = quantity - %s WHERE order_id = %s AND product_id = %s", (quantity_to_return, order_id, product_id))
                            conn.commit()

                            print(quantity_to_return ,item_to_return,"(s) returned successfully!")
                        else:
                            print("Not enough ",item_to_return,"in the purchase history to return ",quantity_to_return,"items!")
                        break

                if not item_found:
                    print("Item not found in purchase history!")
            else:
                print("No items found in the purchase history for this customer.")
        else:
            print("Customer not found.")
    except Exception as e:
        print("An error occurred:", str(e))

def add_customer():
    global cursor, conn

    try:

         cursor.execute("SELECT customer_id,name,phone_number,email FROM customers")
         customers = cursor.fetchall()

         for customer in customers:
             customers_id, name, phone_number, email = customer
             print(str(customers_id) + " " + name + " " + str(phone_number) + " " + str(email))


        # Prompt the user for customer details
         name = input("Enter customer name: ")
         phone_number = input("Enter customer phone number: ")
         email = input("Enter customer email: ")

         # Insert the customer data into the Customers table
         cursor.execute("INSERT INTO Customers (name, phone_number, email) VALUES (%s, %s, %s)", (name, phone_number, email))
         conn.commit()

         print("Customer added successfully.")
    except Exception as e:
        print("An error occurred:", str(e))



# Function to exchange items

def exchange_items():
    global cursor, conn

    try:
        # Prompt the user for customer phone number
        phone_number = input("Enter customer's phone number: ")

        # Check if the customer phone number exists in the Customers table
        cursor.execute("SELECT customer_id FROM Customers WHERE phone_number = %s", (phone_number,))
        customer_data = cursor.fetchone()

        if customer_data:
            customer_id = customer_data[0]

            # Fetch the items purchased by the customer
            cursor.execute("SELECT order_id, product_id, quantity FROM OrderDetails WHERE order_id IN (SELECT order_id FROM Orders WHERE customer_id = %s)", (customer_id,))
            purchased_items = cursor.fetchall()

            if purchased_items:
                print("\nItems Purchased:")
                for item in purchased_items:
                    (order_id, product_id, quantity) = item
                    cursor.execute("SELECT name FROM Products WHERE product_id = %s", (product_id,))
                    product_name = cursor.fetchone()[0]
                    print(product_name,'-', quantity)

                item_to_exchange = input("Enter the name of the item you want to exchange: ").capitalize()
                new_item = input("Enter the name of the new item for exchange: ").capitalize()

                # Check if both items are in the purchased items list
                item_to_exchange_found = False
                new_item_found = False

                for item in purchased_items:
                    (order_id, product_id, purchased_quantity) = item
                    cursor.execute("SELECT name FROM Products WHERE product_id = %s", (product_id,))
                    product_name = cursor.fetchone()[0]

                    if item_to_exchange == product_name:
                        item_to_exchange_found = True
                        if new_item == item_to_exchange:
                            print("The new item should be different from the item to exchange.")
                            

               

                    if new_item != product_name:
                        new_item_found = True
                        original_item_rate = cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
                        original_item_rate = cursor.fetchone()[0]
                        cursor.execute("SELECT price FROM Products WHERE name = %s", (item_to_exchange,))
                        item_to_exchange_rate = cursor.fetchone()[0]
                        exchange_rate = item_to_exchange_rate - original_item_rate
                        qty_to_exchange = int(input("Enter the quantity of ",item_to_exchange," to exchange: "))

                        if exchange_rate > 0:
                            print("You will need to pay" ,exchange_rate * qty_to_exchange ,"extra for the exchange.")
                            print("Total amount to be paid:",item_to_exchange_rate * qty_to_exchange," rupees.")
                            print("Please pay the amount to the cash counter.")
                            print("Item will be packed once the payment is received.")
                        elif exchange_rate < 0:
                            print("You will get a refund of ",(-exchange_rate) * qty_to_exchange," rupees for the exchange.")
                            print("Please collect the refund from the cash counter.")
                            print("Item will be packed once the refund is collected.")
                        else:
                            print("No additional payment required for the exchange.")
                            print("Total amount to be paid:",item_to_exchange_rate * qty_to_exchange," rupees.")
                            print("Please pay the amount to the delivery person.")
                            print("Item will be delivered once the payment is received.")
                            confirm_exchange = input("Do you want to proceed with the exchange? (yes/no)").strip().lower()

                            if confirm_exchange == "yes":
                                cursor.execute("UPDATE Products SET quantity = quantity + %s WHERE name = %s", (qty_to_exchange, item_to_exchange))
                                cursor.execute("UPDATE Products SET quantity = quantity - %s WHERE name = %s", (qty_to_exchange, new_item))
                                conn.commit()

                                # Update the exchange in OrderDetails
                                cursor.execute("UPDATE OrderDetails SET product_id = %s, WHERE order_id = %s AND product_id = %s", (product_id, order_id, product_id))
                                cursor.execute("UPDATE OrderDetails SET  quantity = %s WHERE order_id = %s AND product_id = %s", ( qty_to_exchange, order_id, product_id))
                

                                conn.commit()

                                print("Item exchanged successfully!")
                            else:
                                print("Exchange canceled.")
                    break

                if item_to_exchange_found == False:
                    print("Item to exchange not found in purchase history!")
                if new_item_found == False:
                    print("New item not found in purchase history!")
            else:
                print("No items found in the purchase history for this customer.")
        else:
            print("Customer not found.")
    except Exception as e:
        print("An error occurred:", str(e))
# aFunction to view customer details
def view_customer_details():
    global cursor, conn

    customer_id = int(input("Enter customer ID: "))

    # Check if the customer ID exists in the Customers table
    cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
    customer_data = cursor.fetchone()

    if customer_data:
        print("Customer ID:", customer_data[0])
        print("Name:", customer_data[1])
        print("Phone Number:", customer_data[2])
        print("Email:", customer_data[3])
    else:
        print("Customer not found.")

# Function to calculate and display total sales
def total_sales():
    global cursor, conn

    cursor.execute("SELECT SUM(total_amount) FROM Orders")
    total_sales = cursor.fetchone()[0]

    if total_sales:
        print("Total Sales: ", total_sales)
    else:
        print("No sales data available.")

# Function to display product information
def display_product_info():
    global cursor, conn

    # Retrieve product information from the Products table
    cursor.execute("SELECT product_id, name, price, quantity FROM Products")
    products = cursor.fetchall()
    print("\nproduct_id|\t|name|\t\t|price|\t\t|qty|")
    print('-'*75)
    # Display the product information
    for product in products:
        product_id, name, price, quantity = product
        print(str(product_id) + "|\t\t|" + name + "|\t|" + str(price) + "|\t|" + str(quantity))

# Function for user authentication
def authenticate_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check the username and password against predefined values (replace with your authentication logic)
    if username == "gingka" and password == "pegaus":
        return  'gingka'
    elif username == "guest" and password == "12345":
        return 'guest'
    else:
        print("Authentication failed. Invalid username or password.")
        return False






# Main loop with user authentication
while True:
    authenticate_user = authenticate_user()
    if authenticate_user == 'gingka' :

        while True:
            print("*"*25,"Welcome to Gingka's cloths showroom","*"*25)
            print("\nOptions:")

            print("1. Buy Product")

            print("2. Return Items")

            print("3. Exchange Items")

            print("4. View Customer Details")

            print("5. Total Sales")

            print("6. Display Product Info")

            print("7. Add products.qty")

            print("8. Add customers")

            print("9. Remove customers")

            print("10. Add Products")

            print("11. Remove Products")

            print("12. Total Sales On a Particular date")

            print("13. Modity Product Price")

            print("14. View Custom History")
            
            print("15. Subtract Products.qty")
            
            print("0.  Exit")
            
            choice = int(input("Select an option: "))


            if choice == 0:
                print('EXITING......')

                break
            elif choice == 1:
                print("*"*25,"Buy Product","*"*25)

                a = False

                while a == False:
                  a=buy_product()
                  if a == False:
                      add_customer()
                  elif a == 'cancle':
                      break
                while True :
                    other_purchase=input('do you want to purchase any other items (yes/y) or (no/n):').lower()
                    if other_purchase == 'yes' or other_purchase == 'y':
                        buy_product()
                    elif other_purchase == 'no' or other_purchase == 'n':
                        print('thankyou')
                        break
                    else:
                        print('invaild option try again').upper()
            elif choice == 2:
              print("*"*25,"Return Rroduct","*"*25)

              return_items()
            elif choice == 3:
              print("*"*25,"Exchange product","*"*25)

              exchange_items()
            elif choice == 4:
              print("*"*25,"View Customer Details","*"*25)

              view_customer_details()
            elif choice == 5:
              print("*"*25,"Total Sales","*"*25)

              total_sales()
            elif choice == 6:
              print("*"*25," Product Info","*"*25)

              display_product_info()
            elif choice == 7:
              print("*"*25,"Add Quantity","*"*25)

              add_quantity()
            elif choice == 8:
              print("*"*25,"Add Customer ","*"*25)

              add_customer()
            elif choice == 9:

              print("*"*25,"Remove Customer ","*"*25)

              remove_customer() 
            elif choice == 10:
              print("*"*25,"Add Products ","*"*25)

              add_product()
            elif choice == 11:
              print("*"*25,"Remove Products ","*"*25)

              remove_product()
            elif choice == 12:
              print("*"*25,"View Total Sales On a Particular date ","*"*25)

              total_sales_on_date()

            elif choice == 13:

              print("*"*25,"Modify Product Price ","*"*25)

              modify_product_price()

            elif choice == 14:
              print("*"*25,"View Customer History ","*"*25)

              customer_purchase_history()
            elif choice == 15:
              print("*"*25," Subtract Quantity ","*"*25)
              subtract_quantity()
    elif authenticate_user == 'guest' :
        while True:
            print("*"*25,"Welcome to Gingka's cloths showroom","*"*25)

            print("\nOptions:")

            print("1. Buy Product")

            print("2. Return Items")

            print("3. Exchange Items")

            print("4. View Customer Details")

            print("5. Total Sales")

            print("6. Display Product Info")

            print("0.  Exit")
            choice = int(input("Select an option: "))


            if choice == 0:
               print('EXITING......')
               
               break
                
            elif choice == 1:
                print("*"*25,"Buy Product","*"*25)

                a = False

                while a == False:
                  a=buy_product()
                  if a == False:
                      add_customer()
                  elif a == 'cancle':
                      break
                while True :
                    other_purchase=input('do you want to purchase any other items (yes/y) or (no/n):').lower()
                    if other_purchase == 'yes' or other_purchase == 'y':
                        buy_product()
                    elif other_purchase == 'no' or other_purchase == 'n':
                        print('thankyou')
                        break
                    else:
                        print('invaild option try again').upper()
            elif choice == 2:
              print("*"*25,"Return Rroduct","*"*25)

              return_items()
            elif choice == 3:
              print("*"*25,"Exchange product","*"*25)

              exchange_items()
            elif choice == 4:
              print("*"*25,"View Customer Details","*"*25)

              view_customer_details()
            elif choice == 5:
              print("*"*25,"Total Sales","*"*25)

              total_sales()
            elif choice == 6:
              print("*"*25," Product Info","*"*25)
              display_product_info()

    else:
        print("INVALID CHOICE/n try again")
        continue

# Close the MySQL connection
cursor.close()
conn.close()



