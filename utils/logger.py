import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

def get_logger(name):
    """
    Get a logger instance with a specific name.
    :param name: The name of the logger (usually the module name).
    :return: Configured logger instance.
    """
    return logging.getLogger(name)


def set_log_level(level):
    """
    Dynamically set the logging level.
    Args:
        - level: Logging level (e.g., "DEBUG", "INFO").
    """
    logging.getLogger().setLevel(level.upper())

