from functools import wraps
import logging
import time

def log_activity(func):
    @wraps(func)
    def inner(*args, **kwargs):
        logging.info(f"---- Execution Started: {func.__name__} ----")
        start = time.time()
        try:
            result = func(*args, **kwargs)
            logging.info(f"---- Execution Ended: {func.__name__} in {time.time() - start:.2f} ----")
            return result
        except Exception as e:
            logging.exception(f"Error in {func.__name__}: {e}")
            raise
    return inner