import aiomysql
from os.path import isfile
from os import getenv
from dotenv import load_dotenv

# Constants
BUILD_PATH = "./data/db/build.sql"
load_dotenv()

# Global connection pool
# pool = None

"""

	Please check IMPORTANT.md for the layout and descriptions of other commands. Some are very simple, and some are complex.
	For existing errors, check ERRORS.md.
	For overall and general information about this project, database schema, and more, check README.md.

	Goodluck to those who will use this once-so-called 'masterpiece' for their discord server.

	Sincerely,
		raianxh_

		
	PS: The database that KBL BOT uses is MySQL / MariaDB hosted on a production server. Previously, it uses SQLite (which is easy and simple).
        To use SQLite, rename 'db_sqlite.py' to 'db.py' and safely remove this file.

        It's up to you on what database will you use, as it supports most relational databases.

"""

async def init_db_pool():
    """Initialize the aiomysql connection pool."""
    global pool
    pool = await aiomysql.create_pool(
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASS"),
        db=getenv("DB_NAME"),
        autocommit=True,
        minsize=1,
        maxsize=5,
    )
    print("Database connection pool initialized.")


async def commit():
    """Commit changes to the database."""
    async with pool.acquire() as conn:
        await conn.commit()


def with_commit(func):
    """Decorator to ensure a commit after function execution."""
    async def inner(*args, **kwargs):
        await func(*args, **kwargs)
        await commit()
    return inner


@with_commit
async def build():
    """Build the database schema from a SQL file."""
    if isfile(BUILD_PATH):
        await scriptexec(BUILD_PATH)


async def close_pool():
    """Close the database connection pool."""
    pool.close()
    await pool.wait_closed()
    print("Database connection pool closed.")


async def execute(query, *values):
    """Execute a query and fetch no results."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, values)


async def field(query, *values):
    """Execute a query and fetch a single value."""
    global pool
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, values)
            if (result := await cursor.fetchone()) is not None:
                return result[0]


async def record(query, *values):
    """Execute a query and fetch a single record."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, values)
            return await cursor.fetchone()


async def records(query, *values):
    """Execute a query and fetch all records."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, values)
            return await cursor.fetchall()


async def column(query, *values):
    """Execute a query and fetch a single column."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, values)
            return [row[0] for row in await cursor.fetchall()]


async def multiexec(query, valueset):
    """Execute a query with multiple sets of values."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany(query, valueset)


async def scriptexec(path):
    """Execute an SQL script from a file."""
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            try:
                with open(path, "r", encoding="utf-8") as script:
                    for statement in script.read().split(";"):
                        if statement.strip():
                            await cursor.execute(statement)
            except FileNotFoundError:
                print(f"SQL script file not found: {path}")
            except aiomysql.MySQLError as e:
                print(f"Error executing script: {e}")


# Exported methods
__all__ = [
    "init_db_pool",
    "close_pool",
    "execute",
    "field",
    "record",
    "records",
    "column",
    "multiexec",
    "scriptexec",
    "build",
    "autosave",
]
