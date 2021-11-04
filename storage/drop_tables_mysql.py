import mysql.connector

db_conn = mysql.connector.connect(host="acit3855lab6.eastus.cloudapp.azure.com", user="dcheng", password="password", database="orders_reading")
db_cursor = db_conn.cursor()

db_cursor.execute('''
          DROP TABLE customer_orders
          ''')

db_cursor.execute('''
          DROP TABLE completed_orders
          ''')

db_cursor.commit()
db_cursor.close()