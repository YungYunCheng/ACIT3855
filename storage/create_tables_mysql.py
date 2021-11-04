import mysql.connector

db_conn = mysql.connector.connect(host="acit3855lab6.eastus.cloudapp.azure.com", user="dcheng", password="password", database="orders_reading")
db_cursor = db_conn.cursor()
db_cursor.execute('''
          CREATE TABLE customer_orders
          (id INT NOT NULL AUTO_INCREMENT,
           order_id VARCHAR(250) NOT NULL,
           device_id VARCHAR(250) NOT NULL,
           releaseDate VARCHAR(100) NOT NULL,
           num_of_prduct INTEGER NOT NULL,
           product_name VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT customer_orders_pk PRIMARY KEY (id))
          ''')
db_cursor.execute('''
          CREATE TABLE completed_orders
          (id INT NOT NULL AUTO_INCREMENT,
           order_id VARCHAR(250) NOT NULL,
           completedDate VARCHAR(100) NOT NULL, 
           device_id VARCHAR(250)NOT NULL,
           status VARCHAR(250)NOT NULL,
           date_created VARCHAR(100) NOT NULL,
            CONSTRAINT completed_orders_pk PRIMARY KEY (id))
          ''')
db_conn.commit()
db_conn.close()
