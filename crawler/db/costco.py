import pysqlite3 as sqlite3

DB_NAME = "costco.db"


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            basePrice REAL,
            discountPrice REAL,
            discountDateStart DATE,
            discountDateEnd DATE,
            url TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_product(product):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO products (name, basePrice, discountPrice, discountDateStart, discountDateEnd, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            product.name,
            product.basePrice,
            product.discountPrice,
            product.discountDateStart,
            product.discountDateEnd,
            product.url,
        ),
    )
    conn.commit()
    conn.close()


def get_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name, basePrice, discountPrice, discountDateStart, discountDateEnd, url
        FROM products
        """
    )
    products = cursor.fetchall()
    conn.close()
    return products
