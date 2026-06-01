import os
import mysql.connector
import bcrypt
from dotenv import load_dotenv
#load environment variables
load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

# Function to verify the user
def verify_user( username, password):
    
    # Establish a connection to the database
    conn = mysql.connector.connect(
        host=db_host,  # or your database host
        user=db_user,  # or your database username
        password=db_password,
        database=db_database  # or your database name
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Fetch the hashed password for the given username
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    if result:
        stored_hashed_password = result[0]
        # Compare the provided password with the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False
