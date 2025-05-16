import mysql.connector
import os
from typing import Iterator


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
    
def stream_user_ages() -> Iterator[float]:
    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT age FROM user_data")
        
        for (age,) in cursor:
            yield float(age)
            
    except mysql.connector.Error as e:
        print(f"Error fetching user ages: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
def calculate_average_age() -> float:
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


def main():
    try:
        average_age = calculate_average_age()
        
        print(f"Average age of users: {average_age:.2f}")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()