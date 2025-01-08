class StockItem:
    # Class variable shared across all instances
    stock_category = "Car accessories"

    def __init__(self, stock_code, stock_name="Unknown Stock Name", stock_description="Unknown Stock Description", brand=None, price=None, quantity=0):
        self._stock_code = stock_code
        self._stock_name = stock_name
        self._stock_description = stock_description
        self._brand = brand

        from pricemanagement import PriceManager
        from stockmanagement import StockManager

        self._price_manager = PriceManager(price)  # Initialize with price if available
        self._stock_manager = StockManager(quantity)  # Initialize with quantity if available

    def get_stock_code(self):
        return self._stock_code

    def get_stock_name(self):
        return self._stock_name

    def get_stock_description(self):
        return self._stock_description

    def get_brand(self):
        return self._brand

    def get_price_before_vat(self):
        return self._price_manager.price_before_vat

    def get_price_after_vat(self):
        return self._price_manager.price_after_vat

    def set_price(self, price):
        self._price_manager.set_price(price)

    def set_vat_rate(self, vat_rate):
        self._price_manager.set_vat_rate(vat_rate)

    def get_vat_rate(self):
        return self._price_manager.get_vat_rate()

    def get_quantity(self):
        return self._stock_manager.get_stock_quantity()

    def increase_stock(self, amount):
        self._stock_manager.increase_stock(amount)

    def sell_stock(self, amount):
        self._stock_manager.sell_stock(amount)

    def get_stock_value(self):
        return self._stock_manager.get_stock_value(self.get_price_before_vat())

    def __str__(self):
        return (f"Stock Code: {self._stock_code}, "
                f"Name: {self._stock_name}, "
                f"Description: {self._stock_description}, "
                f"Brand: {self._brand}, "
                f"Quantity: {self.get_quantity()}, "
                f"Price before VAT: {self.get_price_before_vat():.2f}, "
                f"Price after VAT: {self.get_price_after_vat():.2f}, "
                f"Total stock value: {self.get_stock_value():.2f}")

