#Base Class
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
#Sub-classes
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

#reading from the txt file
products = []

with open("products.txt", "r") as file:
    for line in file:
        pid, name, category, price, stock = line.strip().split(",")
        price = float(price)
        stock = int(stock)

        if category == "Electronics":
            products.append(Electronics(pid, name, category, price, stock))
        elif category == "Clothing":
            products.append(Clothing(pid, name, category, price, stock))
        elif category == "Food":
            products.append(Food(pid, name, category, price, stock))
#sample order
order = {
    "Wireless Mouse": 4,
    "Summer Dress": 1,
    "Milk Gallon": 3
}

#calculate the final bill amount
grand_total = 0

for product in products:  # products list came from file
    if product.name in order:  # if the customer ordered this item
        quantity = order[product.name]
        if product.stock >= quantity:
            total = product.calculate_total(quantity)
            grand_total += total
            product.stock -= quantity  # reduce stock
            print(f"{product.name}: {quantity} x {product.price} = {total:.2f}")

#writting the bill to a file
with open("final_bill.txt", "w") as bill:
    bill.write("ID\tName\tCategory\tQuantity\tTotal\n")
    for product in products:
        if product.name in order:
            quantity = order[product.name]
            total = product.calculate_total(quantity)
            bill.write(f"{product.pid}\t{product.name}\t{product.category}\t{quantity}\t{total:.2f}\n")

    bill.write(f"\nGrand Total: {grand_total:.2f}\n")

