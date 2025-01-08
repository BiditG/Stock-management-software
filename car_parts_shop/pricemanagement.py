class PriceManager:
    def __init__(self, price, vat_rate=17.5):
        self._price = price
        self._vat_rate = vat_rate

    @property
    def price_before_vat(self):
        return self._price

    @property
    def price_after_vat(self):
        return self._price * (1 + self._vat_rate / 100)

    def set_price(self, price):
        if price > 0:
            self._price = price
        else:
            raise ValueError("Price must be positive.")

    def get_vat_rate(self):
        return self._vat_rate

