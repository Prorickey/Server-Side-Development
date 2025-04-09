CREATE TABLE IF NOT EXISTS accounts(
    rowid       INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL,
    password    TEXT NOT NULL,
    salt        TEXT NOT NULL,
);

CREATE TABLE IF NOT EXISTS profiles(
    rowid   INTEGER PRIMARY KEY AUTOINCREMENT,
    userid  INTEGER NOT NULL,
    fname   TEXT DEFAULT 'Anonymous',
    lname   TEXT DEFAULT '',
    avatar  TEXT,

    FOREIGN KEY(userid) REFERENCES accounts(rowid)
);