# services/file_ops.py
from ..models.base_models import Electronics, Clothing, Food
from .decorators import log_activity
import aiofiles
import logging
import asyncio

@log_activity
async def load_products(file_path):
    products = []
    try:
        async with aiofiles.open(file_path, "r") as file:
            async for line in file:  # only async because file I/O is async
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
        logging.info(f"Products loaded: {len(products)} items")
    except Exception as e:
        logging.exception(f"Error reading {file_path}: {e}")
    return products

@log_activity
async def write_bill(file_path, products, order, grand_total):
    try:
        async with aiofiles.open(file_path, "w") as bill:
            await bill.write("ID\tName\tCategory\tQuantity\tTotal\n")
            for product in products:  # normal for loop because products is a list
                if product.name in order:
                    quantity = order[product.name]
                    total = product.calculate_total(quantity)
                    await bill.write(f"{product.pid}\t{product.name}\t{product.category}\t{quantity}\t{total:.2f}\n")
            await bill.write(f"\nGrand Total: {grand_total:.2f}\n")
        logging.info(f"Bill written successfully to {file_path}")
    except Exception as e:
        logging.error(f"Error while writing bill: {e}")
