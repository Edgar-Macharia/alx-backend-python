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
    
def paginate_users(page_size: int, offset: int) -> List[Dict]:
    # function to get a specific page of users
    connection = connect_to_database()
    try:
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        
        # Fetch all rows in the current page
        page_data = cursor.fetchall()
        
        return page_data
        
    except mysql.connector.Error as e:
        print(f"Error fetching paginated users: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
def lazy_paginate(page_size: int) -> Iterator[Dict]:
    # generator function to lazily paginate through users
    
    offset = 0
    
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        
        if not page:
            break
        
        for user in page:
            yield user
        
        offset += page_size
 
        
# Example
if __name__ == "__main__":

    PAGE_SIZE = 10
    
    print(f"Lazily loading users with page size of {PAGE_SIZE}:")
    
    for i, user in enumerate(lazy_paginate(PAGE_SIZE), 1):
        print(f"User {i}: {user['name']} (Email: {user['email']})")
        
        if i >= 5:
            print("...")
            break
    
    total_users = sum(1 for _ in lazy_paginate(PAGE_SIZE))
    print(f"\nTotal users in database: {total_users}")

    total_age = sum(float(user['age']) for user in lazy_paginate(PAGE_SIZE))
    print(f"Average age: {total_age / total_users:.2f}")