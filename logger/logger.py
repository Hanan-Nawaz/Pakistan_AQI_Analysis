import logging

def create_logger(file_path: str, formater: str, disabled: bool = False, level: int = 5) -> logging.Logger:
    """Creates a custom logger for logging

    Parameters
    ----------
    file_path : str
        File path of the logging file
    formater : str
        The format
    disabled : bool, optional
        To disable the logger, by default False
    level : int, optional
        Level of the logger, by default 5

    Returns
    -------
    logging.Logger
        Returns the logger
    """
    
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    logger.Propagate = False
    logger.disabled = disabled

    if not logger.handlers:
        file_handler = logging.FileHandler(file_path)
        formater = logging.Formatter(formater)
        file_handler.setFormatter(formater)
        logger.addHandler(file_handler)

    return logger
