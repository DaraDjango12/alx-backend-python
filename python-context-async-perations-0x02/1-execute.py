import mysql.connector

class ExecuteQuery:
    """
    Custom context manager to execute a parameterized SELECT query.
    """
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your actual password
            database="ALX_prodev"
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # This will be assigned in the 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
