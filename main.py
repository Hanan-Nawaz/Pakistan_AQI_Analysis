from dotenv import load_dotenv
import os
import yaml
from logger.logger import create_logger
from etl.extract import get_historical_data, get_daily_data
import logging
from typing import List, Dict

def get_yaml(file_path: str) -> dict:
    """Get configurations of the projects

    Parameters
    ----------
    file_path : str
        The file path of the config.yaml file.

    Returns
    -------
    dict
        Configurations needed for the project.
    """

    with open(file_path) as file:
        config = yaml.safe_load(file)

    return config

def load_env() -> None:
    """load .env which contains api_key."""

    dotenv_path = os.path.join(os.path.dirname(__file__), 'config/', '.env')
    load_dotenv(dotenv_path)

def get_logger(config: dict) -> logging.Logger:
    """Create the logger

    Parameters
    ----------
    config : dict
        Configuration of the project

    Returns
    -------
    logging.Logger
        Returns the logger
    """

    file_path = config['general']['logs']['filename']
    level = config['general']['logs']['level']
    format = config['general']['logs']['format']
    return create_logger(file_path, format, level)

def extract_historical(config: dict, api_key: str, logger:logging.Logger) -> List[Dict]:
    """Get AQI historical data from the Open Weather API

    Parameters
    ----------
    config : dict
        Configurations of the project
    api_key : str
        Api key, needed to call API
    logger : logging.Logger
        Custom logger for Logging

    Returns
    -------
    List[Dict]
        Returns the historical AQI data.
    """
        
    try:
        data_historical = get_historical_data(config, api_key, logger)
        return data_historical
    except Exception as e:
        logger.exception(e)
 
def extract_daily(config: dict, api_key: str, logger:logging.Logger) -> List[Dict]:
    """Get AQI daily data from the Open Weather API

    Parameters
    ----------
    config : dict
        Configurations of the project
    api_key : str
        Api key, needed to call API
    logger : logging.Logger
        Custom logger for Logging

    Returns
    -------
    List[Dict]
        Returns the daily AQI data.
    """

    try:
        data_daily = get_daily_data(config, api_key, logger)
        return data_daily
    except Exception as e:
        logger.exception(e)

def main():
    load_env()
    config = get_yaml('config/config.yaml')
    logger = get_logger(config)
    data = extract_daily(config['extract'], os.getenv('api_key'), logger)
    print(data)

if __name__ == "__main__":
    main()
