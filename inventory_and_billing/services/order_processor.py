# services/order_processor.py
from ..models.exceptions import OutofStockError
from .decorators import log_activity
import logging
import asyncio

@log_activity
async def process_order(products, order):
    grand_total = 0
    for product in products:  # normal for loop
        if product.name in order:
            quantity = order[product.name]
            if product.stock >= quantity:
                total = product.calculate_total(quantity)
                grand_total += total
                product.stock -= quantity
                logging.info(f"Order processed: {product.name} | Quantity: {quantity} | Total: {total:.2f}")
                await asyncio.sleep(0)  # allows event loop to switch tasks
            else:
                raise OutofStockError(f"{product.name} is out of stock.")
    return grand_total
