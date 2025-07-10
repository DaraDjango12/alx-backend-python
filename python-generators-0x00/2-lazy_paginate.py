import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users starting from the given offset.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that yields pages of users, loading each only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
