import asyncio
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def async_retry(max_retries: int = 3, delay: float = 2.0):
    """
    Async decorator to retry a coroutine in case of exceptions.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{max_retries} for {func.__name__} failed with error: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            logger.error(f"All {max_retries} attempts failed for {func.__name__}.")
            raise last_exception
        return wrapper
    return decorator
