-- Sample accounts, these are just to view and will not be logged into
INSERT INTO accounts (username, password, salt) VALUES
('user1', 'password1', 'salt1'),
('user2', 'password2', 'salt2'),
('user3', 'password3', 'salt3'),
('user4', 'password4', 'salt4'),
('user5', 'password5', 'salt5'),
('user6', 'password6', 'salt6'),
('user7', 'password7', 'salt7'),
('user8', 'password8', 'salt8'),
('user9', 'password9', 'salt9'),
('user10', 'password10', 'salt10');

-- Sample profiles to go with the sample accounts
INSERT INTO profiles (userid, fname, lname, avatar) VALUES
(1, 'Anonymous', '', NULL), 
(2, 'John', 'Doe', '/static/avatars/prorickey_avatar.png')
(3, 'Jane', '', '/static/avatars/prorickey_avatar.png'), 
(4, 'Anonymous', 'Smith', NULL),
(5, 'Alice', 'Johnson', NULL), 
(6, 'Anonymous', '', '/static/avatars/prorickey_avatar.png'), 
(7, 'Tom', NULL, '/static/avatars/prorickey_avatar.png'),
(8, 'Emily', 'Clark', NULL), 
(9, 'Anonymous', 'Brown', '/static/avatars/prorickey_avatar.png'), 
(10, 'Bob', '', NULL); 