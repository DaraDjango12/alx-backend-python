import asyncio
import aiosqlite

DB_PATH = "users.db"  # ✅ Path to your SQLite database

async def async_fetch_users():
    """
    Fetch all users from the users table.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row  # Return results as dict-like rows
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("\nAll users:")
            for user in users:
                print(dict(user))


async def async_fetch_older_users():
    """
    Fetch users older than 40 from the users table.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in users:
                print(dict(user))


async def fetch_concurrently():
    """
    Run both async queries concurrently.
    """
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# ✅ Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
