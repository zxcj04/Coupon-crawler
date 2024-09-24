import json
import re
from datetime import date, datetime

import requests

# FILE_NAME = "costco.json"


class Product:
    name = ""
    basePrice = 0
    discountPrice = 0
    discountDateStart = date.today()
    discountDateEnd = date.today()
    url = ""

    def __init__(self, name, basePrice, discountPrice, summary, url):
        self.name = name
        self.basePrice = basePrice
        self.discountPrice = discountPrice
        self.discountDateStart, self.discountDateEnd = self.extractDiscountDate(summary)
        self.url = "https://www.costco.com.tw/" + url

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
            f"Product: {self.name}\n"
            f"\tBase Price: {self.basePrice}\n"
            f"\tDiscount Price: {self.discountPrice}\n"
            f"\tDiscount Date Start: {self.discountDateStart}\n"
            f"\tDiscount Date End: {self.discountDateEnd}\n"
            f"\tURL: {self.url}"
        )


def get_data():
    url = "https://www.costco.com.tw/rest/v2/taiwan/products/search?fields=FULL&query=&pageSize=10000&category=hot-buys&lang=zh_TW&curr=TWD"
    response = requests.get(url)
    return response.json()


def main():
    # with open(FILE_NAME, "r") as file:
    #     data = json.load(file)
    data = get_data()

    products = data.get("products")
    serialized_products = []

    for product in products:
        name = product.get("name")
        basePrice = product.get("basePrice", {}).get("value", 0)
        discountPrice = product.get("discountPrice", {}).get("value", 0)
        summary = product.get("summary")
        url = product.get("url")
        product = Product(name, basePrice, discountPrice, summary, url)
        serialized_products.append(product)

    with open("web_products.txt", "w") as file:
        for product in serialized_products:
            file.write(str(product) + "\n\n")


if __name__ == "__main__":
    main()
