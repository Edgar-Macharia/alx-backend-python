import sqlite3
import os

class DatabaseConnection:
    
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def __enter__(self):
        print(f"🔌 Opening database connection to {self.db_path}")
        
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"❌ An error occurred: {exc_value}")
            if self.connection:
                self.connection.rollback()
        else:
            print("✅ Operations completed successfully")
            if self.connection:
                self.connection.commit()
        
        if self.cursor:
            self.cursor.close()
            print("📝 Cursor closed")
        
        if self.connection:
            self.connection.close()
            print("🔐 Database connection closed")
        
        return False
    
if __name__ == "__main__":
# Use the context manager to query users table and print results
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)