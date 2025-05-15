import mysql.connector
import os
from typing import Dict, Iterator

def connect_to_database() -> mysql.connector.connection.MySQLConnection:

    try:
        connection = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        raise
    
def stream_users() -> Iterator[Dict]:
    
    connection = connect_to_database()
    try:
        # Create a cursor that returns rows as dictionaries
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user_data")
        
        for row in cursor:
            yield row
            
    except mysql.connector.Error as e:
        print(f"Error fetching users: {e}")
        raise
    finally:

        if connection.is_connected():
            cursor.close()
            connection.close()
            

# Example
if __name__ == "__main__":
    # print first 5 users
    print("Streaming users from database:")
    
    for i, user in enumerate(stream_users(), 1):
        print(f"User {i}: {user}")
        
        if i >= 2:
            print("...")
            break