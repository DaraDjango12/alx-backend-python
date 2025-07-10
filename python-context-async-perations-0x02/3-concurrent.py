import asyncio
import aiosqlite

DB_PATH = "users.db"  # ✅ Replace with your database path


async def async_fetch_users():
    """
    Fetch all users from the users table.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return [dict(user) for user in users]  # ✅ Return statement


async def async_fetch_older_users():
    """
    Fetch users older than 40.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            return [dict(user) for user in users]  # ✅ Return statement


async def fetch_concurrently():
    """
    Run both queries concurrently and return their results.
    """
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return all_users, older_users  # ✅ Return required here


if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())

    print("\n✅ All users:")
    for user in all_users:
        print(user)

    print("\n✅ Users over 40:")
    for user in older_users:
        print(user)
