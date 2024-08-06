DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS concert;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE concert (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    mgmt_email TEXT,
    mgmt_name TEXT,
    emailed BOOLEAN DEFAULT FALSE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (venue_id) REFERENCES venue(id)
);

CREATE TABLE venue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT,
    address TEXT,
    rating INTEGER,
    minimal_substring TEXT,
    venue_email_text TEXT
);

CREATE TABLE venue_alias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT NOT NULL,
    venue_id INTEGER NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venue (id) ON DELETE CASCADE
);
