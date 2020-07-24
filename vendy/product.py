from decimal import Decimal


class Product:
    def __init__(self, name: str = "", price: str = "0.00") -> None:
        self.name = name
        self.price = Decimal(price)
