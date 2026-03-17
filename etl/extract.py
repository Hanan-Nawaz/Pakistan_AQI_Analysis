import requests as req
import logging
from typing import List, Dict


def get_historical_data(config: dict, api_key: str, logger: logging.Logger) -> List[Dict]:
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
    cities = config['cities']
    start  = config['start']
    end    = config['end']
    results = []

    for city_name, coords in cities.items():
        params = {
            'lat':   coords['latitude'],
            'lon':   coords['longitude'],
            'start': start,
            'end':   end,
            'appid': api_key
        }
        try:
            response = req.get(config['base_url_past'], params=params)
            response.raise_for_status()
            data = response.json()
            data['city'] = city_name        # tag which city this belongs to
            results.append(data)
            logger.info(f"Historical data fetched for {city_name}")
        except req.exceptions.ConnectionError:
            logger.exception(f"[{city_name}] Failed to connect. Check internet or URL.")
        except req.exceptions.Timeout:
            logger.exception(f"[{city_name}] Request timed out.")
        except req.exceptions.HTTPError as e:
            logger.exception(f"[{city_name}] HTTP error: {e}")
        except req.exceptions.RequestException as e:
            logger.exception(f"[{city_name}] Request error: {e}")

    return results


def get_daily_data(config: dict, api_key: str, logger: logging.Logger) -> List[Dict]:
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
    cities = config['cities']
    results = []

    for city_name, coords in cities.items():
        params = {
            'lat':   coords['latitude'],
            'lon':   coords['longitude'],
            'appid': api_key
        }
        try:
            response = req.get(config['base_url'], params=params)
            response.raise_for_status()
            data = response.json()
            data['city'] = city_name        # tag which city this belongs to
            results.append(data)
            logger.info(f"Daily data fetched for {city_name}")
        except req.exceptions.ConnectionError:
            logger.exception(f"[{city_name}] Failed to connect. Check internet or URL.")
        except req.exceptions.Timeout:
            logger.exception(f"[{city_name}] Request timed out.")
        except req.exceptions.HTTPError as e:
            logger.exception(f"[{city_name}] HTTP error: {e}")
        except req.exceptions.RequestException as e:
            logger.exception(f"[{city_name}] Request error: {e}")

    return results