PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY,
    username  TEXT NOT NULL UNIQUE,
    email     TEXT NOT NULL UNIQUE,
    bio       TEXT NOT NULL,
    password  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS followers (
    id            INTEGER PRIMARY KEY,
    follower_id   INTEGER NOT NULL,
    following_id  INTEGER NOT NULL,

    FOREIGN KEY(follower_id) REFERENCES users(id),
    FOREIGN KEY(following_id) REFERENCES users(id),
    UNIQUE(follower_id, following_id)
);

CREATE VIEW IF NOT EXISTS following
AS
    SELECT users.username, friends.username as friendname
    FROM users, followers, users AS friends
    WHERE
        users.id = followers.follower_id AND
        followers.following_id = friends.id;

