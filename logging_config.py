import logging
import sys

def setup_logging():
    """
    Configures logging with both console and file handlers.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (logs to app.log)
    fh = logging.FileHandler("app.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
