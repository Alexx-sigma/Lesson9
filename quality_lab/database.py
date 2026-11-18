import sqlite3

class Database:
    def __init__(self, path=":memory:"):
        self.connection = sqlite3.connect(str(path))
        self.connection.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL)")
        self.connection.commit()

    def add_product(self, name, price):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        self.connection.execute("INSERT INTO products(name, price) VALUES (?, ?)", (name, price))
        self.connection.commit()

    def list_products(self):
        return self.connection.execute("SELECT name, price FROM products ORDER BY id").fetchall()

    def close(self):
        self.connection.close()
