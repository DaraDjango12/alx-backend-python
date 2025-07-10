import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches and yields user_data rows in batches.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your actual password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def batch_processing(batch_size):
    """
    Generator that yields users over age 25 from each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user['age'] > 25]
        yield filtered


# Optional: Test usage
if __name__ == "__main__":
    for users in batch_processing(2):
        print("Filtered Batch:")
        for user in users:
            print(user)
