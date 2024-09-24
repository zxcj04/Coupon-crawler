class Product:
    URL_PREFIX = ""

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

    def __str__(self):
        return (
            f"Product: {self._name}\n"
            f"\tBase Price: {self._basePrice}\n"
            f"\tDiscount Price: {self._discountPrice}\n"
            f"\tDiscount Date Start: {self._discountDateStart}\n"
            f"\tDiscount Date End: {self._discountDateEnd}\n"
            f"\tURL: {self._url}"
        )
