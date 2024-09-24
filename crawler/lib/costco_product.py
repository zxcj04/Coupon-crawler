import re
from datetime import datetime

from .product import Product


class CostcoProduct(Product):
    URL_PREFIX = "https://www.costco.com.tw"

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
