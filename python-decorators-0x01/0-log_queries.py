# 0-log_queries.py

from datetime import datetime
import sqlite3
import functools

# Decorator to log SQL queries with timestamp
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)
            if query:
                print(f"[{datetime.now()}] Executing SQL Query: {query}")
            else:
                print(f"[{datetime.now()}] No SQL query provided.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
