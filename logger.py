import logging

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:  # Prevent adding multiple handlers
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        stream_handler = logging.StreamHandler()  # Logs to stdout
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    return logger