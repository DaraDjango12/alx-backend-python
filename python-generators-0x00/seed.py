import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import uuid


def connect_db():
    """Connects to the MySQL server (without selecting database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"  # 🔁 Replace with your actual password
        )
        print("✅ Connected to MySQL Server.")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None


def create_database(connection):
    """Creates the ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("✅ Database 'ALX_prodev' ensured.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")
    finally:
        cursor.close()


def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 🔁 Replace with your actual password
            database="ALX_prodev"
        )
        print("✅ Connected to ALX_prodev database.")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error connecting to ALX_prodev: {err}")
        return None


def create_table(connection):
    """Creates the user_data table if it does not exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL,
        INDEX(user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("✅ Table 'user_data' ensured.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating table: {err}")
    finally:
        cursor.close()


def insert_data(connection, data):
    """Inserts data into the user_data table if not already present."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"

    inserted = 0
    for _, row in data.iterrows():
        cursor.execute(check_query, (row['email'],))
        if cursor.fetchone()[0] == 0:
            uid = str(uuid.uuid4())
            cursor.execute(insert_query, (uid, row['name'], row['email'], row['age']))
            inserted += 1

    connection.commit()
    cursor.close()
    print(f"✅ Inserted {inserted} new records.")


def main():
    # Step 1: Connect to MySQL server and ensure DB
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()

    # Step 2: Connect to ALX_prodev DB
    connection = connect_to_prodev()
    if connection is None:
        return

    # Step 3: Ensure table exists
    create_table(connection)

    # Step 4: Load CSV data and insert into DB
    try:
        df = pd.read_csv('user_data.csv')
        if {'name', 'email', 'age'}.issubset(df.columns):
            insert_data(connection, df)
        else:
            print("❌ CSV is missing required columns.")
    except FileNotFoundError:
        print("❌ 'user_data.csv' not found.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
