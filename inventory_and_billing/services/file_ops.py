from ..models.base_models import Electronics, Clothing, Food
import logging

def load_products(file_path):
    products = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                pid, name, category, price, in_stock = line.split(",")
                price = float(price)
                in_stock = int(in_stock)

                if category == 'Electronics':
                    products.append(Electronics(pid, name, category, price, in_stock))
                elif category == 'Clothing':
                    products.append(Clothing(pid, name, category, price, in_stock))
                elif category == 'Food':
                    products.append(Food(pid, name, category, price, in_stock))
                else:
                    logging.warning(f"Unknown category {category} for product {name}")
    except Exception as e:
        logging.exception(f"Error reading {file_path}: {e}")
    logging.info(f"Products: {products}")
    return products

def write_bill(file_path, products, order, grand_total):
    try:
        with open(file_path, "w") as bill:
            bill.write("ID\tName\tCategory\tPrice\tStock")
            for product in products:
                if product.name in order:
                    quantity = order[product.name]
                    total = product.calculate_total(quantity)
                    bill.write(f"\n{product.pid}\t{product.name}\t{product.category}\t{quantity}\t{total:.2f}\n")
            bill.write(f"\nGrand Total: {grand_total:.2f}\n")
    except Exception as e:
        logging.error(f"Error while writting bill: {e}")
    