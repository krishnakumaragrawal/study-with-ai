import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str, 
    log_dir: str = "logs", 
    log_file: str = "logs.log", 
    level: int = logging.DEBUG
) -> logging.Logger:
    
    """
    Creates and configures a logger.

    Args:
        name (str): Logger name. 
        log_dir (str): Directory to store the logs.
        log_file (str): Name of the log file.
        level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        logging.Logger: Configured logger instance.
    """

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    
    # Console handler
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers
    # logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger