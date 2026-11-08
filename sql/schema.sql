CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS wardrobes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS seasons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    wardrobe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    min_temp INTEGER NOT NULL,
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobes(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (season_id) REFERENCES seasons(id)
);