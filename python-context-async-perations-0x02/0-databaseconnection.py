import mysql.connector

class DatabaseConnection:
    """
    Custom context manager for handling MySQL database connections.
    """
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)
        return self.cursor  # This is what you'll use inside the 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# ✅ Using the context manager to perform the query
if __name__ == "__main__":
    with DatabaseConnection(
        host="localhost",
        user="root",
        password="your_password",  # 🔁 Replace with your password
        database="ALX_prodev"
    ) as cursor:
        cursor.execute("SELECT * FROM users")  # Assuming 'users' table exists
        results = cursor.fetchall()
        for row in results:
            print(row)
