import json
import re
from datetime import date, datetime

import pysqlite3 as sqlite3
import requests

FILE_NAME = "costco.json"
DB_NAME = "costco.db"


class Product:
    URL_PREFIX = "https://www.costco.com.tw"

    @property
    def name(self):
        return self._name

    @property
    def basePrice(self):
        return self._basePrice

    @property
    def discountPrice(self):
        return self._discountPrice

    @property
    def discountDateStart(self):
        return self._discountDateStart

    @property
    def discountDateEnd(self):
        return self._discountDateEnd

    @property
    def url(self):
        return self._url

    def __init__(
        self, name, basePrice, discountPrice, discountDateStart, discountDateEnd, url
    ):
        self._name = name
        self._basePrice = basePrice
        self._discountPrice = discountPrice
        self._discountDateStart = discountDateStart
        self._discountDateEnd = discountDateEnd
        self._url = url

    @classmethod
    def fromJson(cls, product):
        name = product.get("name")
        basePrice = product.get("basePrice", {}).get("value", 0)
        discountPrice = product.get("discountPrice", {}).get("value", 0)
        summary = product.get("summary")
        url = cls.URL_PREFIX + product.get("url")
        discountDateStart, discountDateEnd = cls.extractDiscountDate(summary)
        return cls(
            name, basePrice, discountPrice, discountDateStart, discountDateEnd, url
        )

    @staticmethod
    def extractDiscountDate(summary):
        # "<p>* 優惠期間 2024/09/16-2024/09/29</p>" or ""
        # return 2024/09/16 and 2024/09/29
        if not summary:
            return None, None
        pattern = re.compile(r"\d{4}/\d{2}/\d{2}")
        dates = pattern.findall(summary)
        if len(dates) == 2:
            return (
                datetime.strptime(dates[0], "%Y/%m/%d").date(),
                datetime.strptime(dates[1], "%Y/%m/%d").date(),
            )
        return None, None

    def __str__(self):
        return (
            f"Product: {self._name}\n"
            f"\tBase Price: {self._basePrice}\n"
            f"\tDiscount Price: {self._discountPrice}\n"
            f"\tDiscount Date Start: {self._discountDateStart}\n"
            f"\tDiscount Date End: {self._discountDateEnd}\n"
            f"\tURL: {self._url}"
        )


def get_data(web=False):
    if not web:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
        return data

    url = "https://www.costco.com.tw/rest/v2/taiwan/products/search?fields=FULL&query=&pageSize=10000&category=hot-buys&lang=zh_TW&curr=TWD"
    response = requests.get(url)
    return response.json()


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


def setup():
    create_db()


def main():
    data = get_data()

    products = data.get("products")

    for product in products:
        product = Product.fromJson(product)
        insert_product(product)

    products = get_products()
    serialized_products = []
    for product in products:
        product = list(product)
        try:
            serialized_product = Product(*product)
        except Exception as e:
            print(product)
            print(e)
            continue
        serialized_products.append(serialized_product)

    with open("db_products.txt", "w") as file:
        for product in serialized_products:
            file.write(str(product) + "\n\n")


if __name__ == "__main__":
    setup()
    main()
