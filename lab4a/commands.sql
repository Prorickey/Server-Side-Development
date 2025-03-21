CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    salt TEXT
);

INSERT INTO users(username, password, salt) VALUES
('bsea', 'PANDAS!', 'BAMBOO'),
('hubbard', 'Gully', 'Battle'),
('cantwell', 'HCIwoot', 'mices'),
('happer', 'ateapples', 'mooses');

SELECT * FROM users;

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    color TEXT,
    hand TEXT,
    dept TEXT,
    "group" INTEGER DEFAULT(5), /* Must in quotes because group is a reserved key - look that up */
    FOREIGN KEY (userid) REFERENCES users(id)
);

INSERT INTO profiles(userid, color, hand, dept) VALUES 
(4, "red", "left", "science");

INSERT INTO profiles(userid, color, hand, dept, "group") VALUES 
(2, "red", "right", "math", 20),
(1, "green", "right", "ecs", 22),
(3, "purple", "ambi", "humanities", 22);

SELECT color, dept FROM profiles;

SELECT * FROM profiles WHERE hand='right';

SELECT * FROM users INNER JOIN profiles ON users.id = profiles.userid WHERE length(users.password) > 6;

SELECT username FROM users 
INNER JOIN profiles ON users.id = profiles.userid 
WHERE profiles."group" > 10 AND substr(users.salt,1,1) = 'B';