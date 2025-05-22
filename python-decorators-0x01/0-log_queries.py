import sqlite3
import functools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#### decorator to log SQL queries
def log_queries(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        query = None
        
        if 'query' in kwargs:
            query = kwargs['query']
        elif args and isinstance(args[0], str):
            query = args[0]
        else:
            for arg in args:
                if isinstance(arg, str) and any(keyword in arg.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                    query = arg
                    break
        
        # Log the query if found
        if query:
            logging.info(f"Executing SQL Query: {query.strip()}")
        else:
            logging.warning(f"Could not identify SQL query in function '{func.__name__}'")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
if __name__ == "__main__":
    # This will log: "Executing SQL Query: SELECT * FROM users"
    users = fetch_all_users(query="SELECT * FROM users")