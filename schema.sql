CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE wardrobes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL UNIQUE,
    name       VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE seasons (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    wardrobe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    season_id   INTEGER NOT NULL,
    name        VARCHAR(100) NOT NULL,
    min_temp    INTEGER NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobes(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (season_id)   REFERENCES seasons(id)
);

CREATE INDEX idx_items_wardrobe ON items(wardrobe_id);
CREATE INDEX idx_items_category ON items(category_id);
CREATE INDEX idx_items_season   ON items(season_id);