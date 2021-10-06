PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY,
    username    INTEGER NOT NULL,
    text        TEXT NOT NULL,
    timestamp   INTEGER DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS post_username_idx ON posts(username);
CREATE INDEX IF NOT EXISTS post_timestamp_idx ON posts(timestamp);

