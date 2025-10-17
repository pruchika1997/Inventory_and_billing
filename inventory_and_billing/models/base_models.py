# ---- Base Classes ----
class Product:
    def __init__(self, pid, name, category, price, stock):
        self.pid = pid
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def calculate_total(self, quantity):
        """Base version (will be overridden by subclasses)"""
        return self.price * quantity

# ---- Sub classes ----
class Electronics(Product):
    def calculate_total(self, quantity):
        tax = 0.18
        return self.price * quantity * (1 + tax)


class Clothing(Product):
    def calculate_total(self, quantity):
        discount = 0.10
        return self.price * quantity * (1 - discount)


class Food(Product):
    def calculate_total(self, quantity):
        tax = 0.05
        return self.price * quantity * (1 + tax)
