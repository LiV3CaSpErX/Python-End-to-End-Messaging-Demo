import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

#load environment variables
load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

# Database configuration
config = {
    'user': db_user,
    'password': db_password,
    'host': db_host
}

# Connect to MySQL server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Create a new schema
    schema_name = db_database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema_name}")

    # Commit the changes
    cnx.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print(f"Database {schema_name} created successfully")
    cursor.close()
    cnx.close()