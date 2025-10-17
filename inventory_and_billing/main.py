from .services.logger_config import setup_logger
from .services.file_ops import load_products, write_bill
from .services.order_processor import process_order
from .models.exceptions import OutofStockError

def main():
    logger = setup_logger()

    products = load_products("data/products.txt")
    order = {"Wireless Mouse": 10, "Summer Dress": 5, "Milk Gallon": 5}

    try:
        grand_total = process_order(products, order)
        write_bill("data/final_bill.txt", products, order, grand_total)
        print("Bill generated Successfully.")
    except OutofStockError as out:
        print(out)
        logger.warning(out)
    except Exception as e:
        print(f"Unexpected error: {e}")
        logger.exception(e)

if __name__ == "__main__":
    main()
