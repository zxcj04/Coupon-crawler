import pysqlite3 as sqlite3

DB_NAME = "costco.db"


class CostcoDB:
    def __init__(self):
        self.create_db()

    def create_db(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS products (
                        name TEXT PRIMARY KEY,
                        basePrice REAL,
                        discountPrice REAL,
                        discountDateStart DATE,
                        discountDateEnd DATE,
                        url TEXT
                    )
                    """
                )
        except sqlite3.Error as e:
            raise e

    def insert_product(self, product):
        try:
            with sqlite3.connect(DB_NAME) as conn:
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
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def get_products(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT name, basePrice, discountPrice, discountDateStart, discountDateEnd, url
                    FROM products
                    """
                )
                products = cursor.fetchall()
            return products
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def modify_product(self, product):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE products
                    SET name = ?, basePrice = ?, discountPrice = ?, discountDateStart = ?, discountDateEnd = ?, url = ?
                    WHERE name = ?
                    """,
                    (
                        product.name,
                        product.basePrice,
                        product.discountPrice,
                        product.discountDateStart,
                        product.discountDateEnd,
                        product.url,
                        product.name,
                    ),
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
