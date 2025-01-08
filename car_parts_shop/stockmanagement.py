class StockManager:
    def __init__(self, quantity=0):
        self._quantity = quantity

    def get_stock_quantity(self):
        return self._quantity

    def set_stock_quantity(self, quantity):
        self._quantity = quantity

    def increase_stock(self, amount):
        self._quantity += amount

    def sell_stock(self, amount):
        if amount > self._quantity:
            raise ValueError("Not enough stock to sell")
        self._quantity -= amount

    def get_stock_value(self, price):
        return self._quantity * price
