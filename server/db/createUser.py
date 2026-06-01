import os
import mysql.connector
from mysql.connector import errorcode
import bcrypt
from dotenv import load_dotenv

#load environment variables
load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

# Establish a connection to the database
conn = mysql.connector.connect(
    host=db_host,  # or your database host
    user=db_user,  # or your database username
    password=db_password,  # or your database password
    database=db_database  # or your database name
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create a users table with hashed passwords
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
""")

print("Welcome to User Registration System")
# Get username and password from the user
username = input("Enter your username: ")
password = input("Enter your password: ")

#generate a salt
salt = bcrypt.gensalt()

# Hash the password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

try:

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))

    # Commit the transaction
    conn.commit()

    print("User registered successfully")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Database Access Denied")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

# Close the cursor and connection
cursor.close()
conn.close()

