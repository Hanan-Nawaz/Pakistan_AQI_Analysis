import pandas as pd
import logging
from typing import List, Dict

def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the columns drom dictionary to columns

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe that contains dictionary as column

    Returns
    -------
    pd.DataFrame
        Dataframe that are normalized and no longer have dictionary
    """
    records = df['list'].apply(lambda x: x[0])
    df = df.join(pd.json_normalize(records))
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns and remove redundant names like main and components
       from column name.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe where column names are redundant

    Returns
    -------
    pd.DataFrame
        Dataframe with normalized column names
    """

    df.columns = (df.columns
                  .str.replace('main.', '', regex=False)
                  .str.replace('components.', '', regex=False))
    
    return df

def change_types(df: pd.DataFrame) ->pd.DataFrame:
    """Convert datatypes of the columns

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe where column types are not converted

    Returns
    -------
    pd.DataFrame
        Dataframe where column types are normalized
    """

    df['date'] = pd.to_datetime(df['dt'], unit='s').dt.date
    return df

def drop_columns(config: dict, df: pd.DataFrame) -> pd.DataFrame:
    """Drops columns that are not needed.

    Parameters
    ----------
    config : dict
        Configuration of the project containing list of column names to be dropped
    df : pd.DataFrame
        Dataframe that contain redundant columns

    Returns
    -------
    pd.DataFrame
        Dataframe that didn't contain redundant columns
    """

    return df.drop(columns=config['drop_columns'])

def transform_daily(config: dict, raw_data: List[Dict], logger: logging.Logger) -> pd.DataFrame:
    """Transform the daily aqi data

    Parameters
    ----------
    config : dict
        Configuration of the project
    raw_data : json
        Raw json data that we get from api
    logger : json
        Raw json data that we get from api

    Returns
    -------
    pd.DataFrame
        Tranformed dataframe
    """

    try:
        df = pd.DataFrame(raw_data)
        df = normalize(df)
        df = rename_columns(df)
        df = change_types(df)
        df = drop_columns(config, df)

        return df
    except Exception as e:
        logger.exception(e)