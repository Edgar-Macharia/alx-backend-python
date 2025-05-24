import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_path='users.db'):
        self.db_path = db_path
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None
        
    def __enter__(self):
        print(f"Opening database connection to {self.db_path}")
        
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            
            print(f"Executing query: {self.query}")
            
            if self.params:
                print(f"With parameters: {self.params}")
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)
            
            # Fetch and store results
            self.results = self.cursor.fetchall()
            print(f"✅ Query executed successfully. Found {len(self.results)} rows.")

            return self.results
            
        except Exception as e:
            print(f"❌ Error executing query: {e}")
            raise
    
    def __exit__(self):
        
        if self.cursor:
            self.cursor.close()
            print("Cursor closed")
            
        if self.connection:
            self.connection.close()
            print("Database connection closed")
        
        return False
    
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(query, param) as results:
        for row in results:
            print(row)