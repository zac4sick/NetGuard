import sqlite3
import mysql.connector
import mysql.connector.pooling
import itertools

# SQLite3 Configuration
sqlite_db_file = "net_querie_iot.db"  # Replace with the path to your SQLite3 database file
sqlite_connection = sqlite3.connect(sqlite_db_file)
sqlite_cursor = sqlite_connection.cursor()

# MySQL Configuration
mysql_db_config = {
    "host": "13.53.168.221",         # Replace with your MySQL server IP or hostname
    "user": "safeheaven1",             # Replace with your MySQL username
    "password": "Yehan123@",   # Replace with your MySQL password
    "database": "clouddb_ML"           # Replace with your MySQL database name
}

mysql_connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **mysql_db_config)
mysql_connection = mysql_connection_pool.get_connection()
mysql_cursor = mysql_connection.cursor()

# Check if SQLite3 connection is successful
if sqlite_connection:
    print("Successfully connected to SQLite3 database.")
else:
    print("Failed to connect to SQLite3 database.")

# Check if MySQL connection is successful
if mysql_connection.is_connected():
    print("Successfully connected to MySQL database.")
else:
    print("Failed to connect to MySQL database.")

#--------------------------------------------------------------------- OK

# Function to transfer data from SQLite to MySQL and update if exists
def transfer_sqlite_to_mysql():
    try:
        # Retrieve data from SQLite
        sqlite_cursor.execute("SELECT info, ipaddress, status FROM net_queries WHERE status=0")
        data_to_transfer = sqlite_cursor.fetchall()

        sqlite_cursor.execute("SELECT bandwidth, status FROM net_baandwidth WHERE status=0")
        data_to_transferBW = sqlite_cursor.fetchall()

        for row in data_to_transfer:
            info, ipaddress, status = row
            insert_query = "INSERT INTO net_queries (info, ipaddress, status) VALUES (%s, %s, %s)"
            mysql_cursor.execute(insert_query, (info, ipaddress, status))
            mysql_connection.commit()

        print("Data transferred and updated successfully net_queries.") 

        for row1 in data_to_transferBW:
            bandwidth, status = row1
            insert_query = "INSERT INTO net_baandwidth (bandwidth, status) VALUES (%s, %s)"
            mysql_cursor.execute(insert_query, (bandwidth, status))
            mysql_connection.commit()
        # for row in data_to_transfer:
        #     info,status = row
        #     sqlite_cursor.execute("UPDATE net_queries set status = 5 WHERE info = ?",(info))
        #     sqlite_connection.commit()

        print("Data transferred and updated successfully net_baandwidth.")
    except Exception as e:
        print("Error occurred during data transfer:", str(e))
    finally:
        # Close SQLite3 cursor and connection
        sqlite_cursor.close()
        sqlite_connection.close()
        mysql_connection.close()

# Call the function to transfer and update data from SQLite to MySQL
transfer_sqlite_to_mysql()

#--------------------------------------------------------------------- OK

# Reconnect SQLite cursor and connection

del sqlite_connection
del sqlite_cursor
del mysql_connection
del mysql_cursor

sqlite_connection = sqlite3.connect(sqlite_db_file)
sqlite_cursor = sqlite_connection.cursor()

mysql_connection = mysql_connection_pool.get_connection()
mysql_cursor = mysql_connection.cursor()

# Check if SQLite3 connection is successful
if sqlite_connection:
    print("Successfully connected to SQLite3 database. second attempt")
else:
    print("Failed to connect to SQLite3 database. second attempt")

# Check if MySQL connection is successful
if mysql_connection.is_connected():
    print("Successfully connected to MySQL database. second attempt")
else:
    print("Failed to connect to MySQL database. second attempt")

#--------------------------------------------------------------------- OK

# Delete the MySQL connection pool & SQlite connection

del sqlite_connection
del sqlite_cursor
del mysql_connection
del mysql_cursor
del mysql_connection_pool
