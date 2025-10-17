from ..models.exceptions import OutofStockError
import logging

def process_order(products, order):
    grand_total = 0
    for product in products:
        if product.name in order:
            quantity = order[product.name]
            if product.stock >= quantity:
                total = product.calculate_total(quantity)
                grand_total += total
                product.stock -= quantity
                logging.info(f"Order processed: {product.name} | Quantity: {quantity} | Total: {total:.2f}")
            else:
                raise OutofStockError(f"{product.name} is out of stock.")
    return grand_total