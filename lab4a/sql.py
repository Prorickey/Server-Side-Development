import sqlite3 

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

def select(query):
	res = cursor.execute(query)
	for row in res:
		row = '	'.join([str(x) for x in row])
		print(row)

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT,
	password TEXT,
	salt TEXT
)""")

cursor.execute("""
INSERT INTO users(username, password, salt) VALUES
('bsea', 'PANDAS!', 'BAMBOO'),
('hubbard', 'Gully', 'Battle'),
('cantwell', 'HCIwoot', 'mices'),
('happer', 'ateapples', 'mooses')""")

conn.commit()

select("SELECT * FROM users")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    color TEXT,
    hand TEXT,
    dept TEXT,
    "group" INTEGER DEFAULT(5), /* Must in quotes because group is a reserved key - look that up */
    FOREIGN KEY (userid) REFERENCES users(id)
)""")

cursor.execute("""
INSERT INTO profiles(userid, color, hand, dept) VALUES 
(4, "red", "left", "science")""")

cursor.execute("""
INSERT INTO profiles(userid, color, hand, dept, "group") VALUES 
(2, "red", "right", "math", 20),
(1, "green", "right", "ecs", 22),
(3, "purple", "ambi", "humanities", 22)""")

conn.commit()

select("SELECT color, dept FROM profiles")
select("SELECT * FROM profiles WHERE hand='right'")
select("SELECT * FROM users INNER JOIN profiles ON users.id = profiles.userid WHERE length(users.password) > 6")

select("""
SELECT username FROM users 
INNER JOIN profiles ON users.id = profiles.userid 
WHERE profiles."group" > 10 AND substr(users.salt,1,1) = 'B'""")