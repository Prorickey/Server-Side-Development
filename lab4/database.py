import sqlite3

__db = None 

def connect():
    __db = sqlite3.connect("accounts.db")

    # TODO: Create tables here - probably can just run my schema file