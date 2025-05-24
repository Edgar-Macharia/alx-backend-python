import sqlite3
import os

def create_database(db_path="users.db"):
    # Check if database file exists
    db_exists = os.path.exists(db_path)
    
    # Connect to the database
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    
    print(f"{'Connected to' if db_exists else 'Created new'} database at {db_path}")
    return connect, cursor

def create_users_table(cursor):

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        date_of_birth DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        role TEXT DEFAULT 'user'
    )
    ''')
    print("Users table created or already exists")
    
def insert_test_users(cursor):

    test_users = [
        ('testuser1', 'test1@example.com', 'hashed_password1', 'John', 'Doe', '1990-01-01', True, 'user'),
        ('testuser2', 'test2@example.com', 'hashed_password2', 'Jane', 'Smith', '1992-05-15', True, 'admin'),
        ('testuser3', 'test3@example.com', 'hashed_password3', 'Bob', 'Johnson', '1985-12-10', False, 'user'),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO users 
    (username, email, password_hash, first_name, last_name, date_of_birth, is_active, role) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', test_users)
    
    print(f"Inserted test users into the database")
    
def query_users(cursor):
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    
    print("\nUsers in the database:")
    print("-" * 50)
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
    print("-" * 50)
    

def main():
    # Connect to database
    conn, cursor = create_database()
    
    # Create tables
    create_users_table(cursor)
    
    # Insert test data
    insert_test_users(cursor)
    
    # Commit changes
    conn.commit()
    
    # Query data
    query_users(cursor)
    
    # Close connection
    conn.close()
    print("\nDatabase connection closed")

# Script creates a SQLite database, creates a users table, inserts test data, and queries the data.
if __name__ == "__main__":
    main()