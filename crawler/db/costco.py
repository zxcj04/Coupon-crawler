from functools import wraps

import pysqlite3 as sqlite3

DB_NAME = "costco.db"


class CostcoDB:
    def __init__(self):
        self.create_db()

    @staticmethod
    def db_connection_handler(fallback=None):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    with sqlite3.connect(DB_NAME) as conn:
                        return func(self, *args, **kwargs, conn=conn)
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                    if fallback is not None:
                        return fallback

            return wrapper

        return decorator

    def create_db(self):
        self._create_db()

    def insert_product(self, product):
        self._insert_product(product)

    def get_products(self):
        return self._get_products()

    def modify_product(self, product):
        self._modify_product(product)

    def is_exists(self, product):
        return self._is_exists(product)

    @db_connection_handler()
    def _create_db(self, conn=None):
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
        conn.commit()

    @db_connection_handler()
    def _insert_product(self, product, conn=None):
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

    @db_connection_handler(fallback=[])
    def _get_products(self, conn=None):
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name, basePrice, discountPrice, discountDateStart, discountDateEnd, url
            FROM products
            """
        )
        products = cursor.fetchall()
        return products

    @db_connection_handler()
    def _modify_product(self, product, conn=None):
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
        conn.commit()

    @db_connection_handler(fallback=False)
    def _is_exists(self, product, conn=None):
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name
            FROM products
            WHERE name = ?
            """,
            (product.name,),
        )
        return cursor.fetchone() is not None

    @db_connection_handler()
    def _delete_product(self, product, conn=None):
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM products
            WHERE name = ?
            """,
            (product.name,),
        )
        conn.commit()
