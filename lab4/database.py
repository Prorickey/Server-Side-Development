from queue import Queue
import secrets
import sqlite3
import hashlib
import string

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

def get_profile(username):
    """
    Get the profile for the given username. This includes the first name, last name, and bio.
    """

    # Grab a connection from the pool
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT fname, lname, avatar FROM profiles INNER JOIN accounts ON profiles.userid = accounts.rowid WHERE accounts.username=?", (username.lower(),))
        profile = cursor.fetchone()
    finally:
        # Release the connection back to the pool
        release_connection(conn)

    return profile

def login(username, password):
    """
    Check if the username and password are valid. If they are valid, true will be returned.
    """

    # Grab a connection from the pool
    conn = get_connection()
    verified = False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT salt, password FROM accounts WHERE username=?", (username.lower(),))
        result = cursor.fetchone()

        if result is not None:
            salt = result[0]

            # Hash the password with the salt
            hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
            if hashed_password == result[1]:
                verified = True
    finally:
        # Release the connection back to the pool
        release_connection(conn)

    return verified

def register(username, password):
    """
    Register a new user with the given username and password. If the username is already taken, false will be returned.
    """

    # Grab a connection from the pool
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username=?", (username.lower(),))
        existing_user = cursor.fetchone()

        if existing_user is not None:
            return False

        # Generate a random salt
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

        # Hash the password with the salt
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()

        # Insert the new user into the database
        cursor.execute("INSERT INTO accounts (username, password, salt) VALUES (?, ?, ?)", (username.lower(), hashed_password, salt))
        cursor.execute("INSERT INTO profiles (userid) VALUES (?)", (cursor.lastrowid,))
        conn.commit()
    finally:
        # Release the connection back to the pool
        release_connection(conn)

    return True

def delete_user(user):
    """
    Delete a user account and its associated profile
    """

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profiles WHERE userid = (SELECT rowid FROM accounts WHERE username=?)", (user,))
        cursor.execute("DELETE FROM accounts WHERE username=?", (user,))
        conn.commit()
    finally:
        release_connection(conn)

def update_password(user, password):
    """
    Update a users password
    """

    conn = get_connection()
    try:
        # Rehash the password with a new salt to ensure security
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()

        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET password=?, salt=? WHERE username=?", (hashed_password, salt, user))
        conn.commit()
    finally:
        release_connection(conn)

    return True

def update_name(user, fname, lname):
    """
    Update a users name
    """

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE profiles SET fname=?, lname=? WHERE userid = (SELECT rowid FROM accounts WHERE username=?)", (fname, lname, user))
        conn.commit()
    finally:
        release_connection(conn)

    return True