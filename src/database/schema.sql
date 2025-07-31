CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id INTEGER NOT NULL,
    payer_id INTEGER NOT NULL,
    server_id INTEGER NOT NULL,
    price REAL NOT NULL,
    plan TEXT NOT NULL,
    created_at TEXT,
    status TEXT CHECK(status IN ('pending', 'success', 'canceled')) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    plan_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);


CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    price REAL NOT NULL,
    max_ram INTEGER NOT NULL
    
);

CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner INTEGER NOT NULL,
    name TEXT NOT NULL,
    application_id TEXT NOT NULL,
    ram INTEGER NOT NULL
);


CREATE INDEX IF NOT EXISTS idx_payment_id ON transactions (payment_id);
CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id);
