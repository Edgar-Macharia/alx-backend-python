from dotenv import load_dotenv
import os
load_dotenv()

import mysql.connector
import pandas as pd
import uuid
from mysql.connector import Error

def connect_db():
    # """Connect to MySQL database and return the connection object."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", "")
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

    
def create_database(connection):
#    """creates a database named ALX_prodev"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")
 
        
def connect_to_prodev():
    # """Connect to the ALX_prodev database and return the connection object."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None
    
def create_table(connection):
    # """Create the user_data table."""
    try:
        cursor = connection.cursor()
        
        # Create the user_data table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'user_data' created or already exists")
    except Error as e:
        print(f"Error creating table: {e}")
        
        
def insert_data(connection, data):
    # """Insert data into the user_data table."""
    try:
        cursor = connection.cursor()
        
        # Check if each row exists before inserting
        for index, row in data.iterrows():
            # Generate UUID if user_id is not provided or is NaN
            if 'user_id' not in row or pd.isna(row['user_id']):
                user_id = str(uuid.uuid4())
            else:
                user_id = row['user_id']
            
            # Check if this user_id already exists
            check_query = "SELECT COUNT(*) FROM user_data WHERE user_id = %s"
            cursor.execute(check_query, (user_id,))
            result = cursor.fetchone()
            
            # Insert only if the user_id doesn't exist
            if result[0] == 0:
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user_id,
                    row['name'],
                    row['email'],
                    row['age']
                ))
        
        connection.commit()
        print(f"Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
        
def row_generator(connection, batch_size=100):
    # """Generator to yield rows from the user_data table in batches."""
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get total count of rows
        cursor.execute("SELECT COUNT(*) as count FROM user_data")
        total_rows = cursor.fetchone()['count']
        print(f"Total rows in database: {total_rows}")
        
        # Fetch and yield rows in batches for efficiency
        offset = 0
        while offset < total_rows:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s", 
                (batch_size, offset)
            )
            rows = cursor.fetchall()
            
            if not rows:
                break
                
            # Yield each row one at a time
            for row in rows:
                yield row
                
            offset += batch_size
            
    except Error as e:
        print(f"Error in row generator: {e}")
            
def main():
    # execute the script.
    
    # Connect to MySQL server
    connection = connect_db()
    if not connection:
        return
    
    # Create database
    create_database(connection)
    connection.close()
    
    # Connect to ALX_prodev database
    prodev_connection = connect_to_prodev()
    if not prodev_connection:
        return
    
    # Create table
    create_table(prodev_connection)
    
    # Load CSV data and insert it
    try:
        data = pd.read_csv('user_data.csv')
        insert_data(prodev_connection, data)
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        
    # Use the row generator to fetch and print rows
    print("\nDemonstrating row generator:")
    print("Streaming rows one by one:")
    for i, row in enumerate(row_generator(prodev_connection), 1):
        print(f"Row {i}: {row}")
        # Limit to 5 rows for demonstration
        if i >= 5:
            print("...")
            break

    # Close connection
        prodev_connection.close()


if __name__ == "__main__":
    main()