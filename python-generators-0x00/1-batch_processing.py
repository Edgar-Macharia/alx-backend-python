import mysql.connector
import os
from typing import Dict, Iterator, List


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
    
def stream_users_in_batches(batch_size: int = 100) -> Iterator[List[Dict]]:
    # generator function to stream users in batches
    
    connection = connect_to_database()
    try:
        cursor = connection.cursor(dictionary=True)
        
        # get the total row count
        cursor.execute("SELECT COUNT(*) as count FROM user_data")
        total_rows = cursor.fetchone()['count']
        
        offset = 0
        while offset < total_rows:
            
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            
            # Get all rows in the current batch
            batch = cursor.fetchall()
            
            if not batch:
                break
                
            yield batch
            
            offset += batch_size
            
    except mysql.connector.Error as e:
        print(f"Error fetching users in batches: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
def batch_processing(batch_size: int = 100) -> Iterator[Dict]:

    # generator function to process users in batches
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if float(user['age']) > 25:
                yield user
                
                
# Example
if __name__ == "__main__":

    BATCH_SIZE = 50
    
    print(f"Processing users in batches of {BATCH_SIZE}:")
    print("\nUsers over 25 years old:")
    
    # Count users over 25
    count = 0
    for i, user in enumerate(batch_processing(BATCH_SIZE), 1):
        print(f"User {i}: {user['name']} (Age: {user['age']})")
        count += 1
        
        # Only show first 5 users for demonstration
        if i >= 5 and count < 10:
            print("...")
            break
    
    # Get total count without printing each user
    total_count = sum(1 for _ in batch_processing(BATCH_SIZE))
    print(f"\nTotal users over 25: {total_count}")