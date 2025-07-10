import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your MySQL password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:  # ✅ Loop 1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ Generator usage

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def batch_processing(batch_size):
    """
    Generator that filters users over age 25 from each batch.
    Yields each matching user one by one.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop 2
        for user in batch:  # ✅ Loop 3
            if user['age'] > 25:
                yield user  # ✅ Generator usage
