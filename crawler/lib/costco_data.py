import json

import requests

FILE_DEST = "crawler/data/costco.json"


def get_data(web=False):
    if not web:
        with open(FILE_DEST, "r") as file:
            data = json.load(file)
        return data

    url = "https://www.costco.com.tw/rest/v2/taiwan/products/search?fields=FULL&query=&pageSize=10000&category=hot-buys&lang=zh_TW&curr=TWD"
    response = requests.get(url)
    return response.json()
