import logging

logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,      
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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

# ---- Custom Exception ----
class OutofStockError(Exception):
    """Raised when a product is out of stock."""
    pass

# ---- Load Products from File ----
products = []

try:
    with open("products.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # skip empty lines

            try:
                pid, name, category, price, stock = line.split(",")
                price = float(price)
                stock = int(stock)

                if category == "Electronics":
                    products.append(Electronics(pid, name, category, price, stock))
                elif category == "Clothing":
                    products.append(Clothing(pid, name, category, price, stock))
                elif category == "Food":
                    products.append(Food(pid, name, category, price, stock))
                else:
                    logging.warning(f"Unknown category '{category}' for product '{name}', skipping line.")

            except ValueError as ve:
                logging.error(f"Invalid line format in products.txt: {line} | Error: {ve}")

except FileNotFoundError as e:
    logging.critical("File not found: 'products.txt' | " + str(e))
except PermissionError as p:
    logging.critical("Permission denied accessing 'products.txt' | " + str(p))
except Exception as e:
    logging.exception(f"Unexpected error while reading file: {e}")
else:
    logging.info(f"{len(products)} products loaded successfully.")
finally:
    logging.debug("Product file read attempt completed.")

#---- Process Order ----
order = {
    "Wireless Mouse": 4,
    "Summer Dress": 2,
    "Milk Gallon": 3
}

grand_total = 0

try:
    for product in products:
        if product.name in order:
            quantity = order[product.name]
            if product.stock >= quantity:
                total = product.calculate_total(quantity)
                grand_total += total
                product.stock -= quantity  # reduce stock
                print(f"{product.name}: {quantity} x {product.price} = {total:.2f}")
                logging.info(f"Order processed: {product.name} | Quantity: {quantity} | Total: {total:.2f}")
            else:
                raise OutofStockError(f"{product.name} is out of stock.")
except OutofStockError as e:
    print(e)
    logging.warning(f"Out of stock: {e}")
except Exception as e:
    print("Unexpected error during order processing:", e)
    logging.exception(f"Unexpected error during order processing: {e}")
else:
    logging.info("All orders processed successfully.")
finally:
    logging.debug("Order processing attempt completed.")

# ---- Write Bill to File ----
try:
    with open("final_bill.txt", "w") as bill:
        bill.write("ID\tName\tCategory\tQuantity\tTotal\n")
        for product in products:
            if product.name in order:
                quantity = order[product.name]
                total = product.calculate_total(quantity)
                bill.write(f"{product.pid}\t{product.name}\t{product.category}\t{quantity}\t{total:.2f}\n")

        bill.write(f"\nGrand Total: {grand_total:.2f}\n")

    logging.info("Final bill successfully written to 'final_bill.txt'.")

except Exception as e:
    print("Error while writing final bill:", e)
    logging.error(f"Failed to write bill: {e}")
finally:
    logging.debug("Bill writing operation completed.")
