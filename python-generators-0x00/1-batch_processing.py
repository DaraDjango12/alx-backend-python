import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from user_data in batches of given size.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ yields a batch

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def batch_processing(batch_size):
    """
    Generator that yields users over age 25, one by one, from each batch.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ 1st loop
        for user in batch:  # ✅ 2nd loop
            if user['age'] > 25:
                yield user  # ✅ yields filtered user
