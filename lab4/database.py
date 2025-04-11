from queue import Queue
import sqlite3

schema_file = "schema.sql"

# Connection pool for SQLite database connections
# I had to do this because flask is handling my requests 
# on seperate threads. This solution helps avoid using one
# connection on different threads and allows my application
# to scale better
__connection_pool = Queue(maxsize=5)
for _ in range(5):
    __connection_pool.put(sqlite3.connect("accounts.db", check_same_thread=False))

def get_connection():
    return __connection_pool.get()

def release_connection(connection):
    __connection_pool.put(connection)

def init():
    """
    Connect to the SQLite database and create the tables if they don't exist.
    """

    conn = get_connection()
    try:
        # This just creates all the tables that are defined in the schema file
        with open(schema_file) as f:
            schema = f.read()

        conn.executescript(schema)
        conn.commit()
    finally:
        release_connection(conn)

def get_all_profiles():
    """
    Get all profiles from the database. This also includes the usernames 
    """

    # Grab a connection from the pool
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT username, fname, lname FROM profiles INNER JOIN accounts ON profiles.userid = accounts.rowid")
        profiles = cursor.fetchall()
    finally:
        # Release the connection back to the pool
        release_connection(conn)

    return profiles