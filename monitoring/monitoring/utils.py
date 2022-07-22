import pandas as pd
from fastapi import HTTPException
from loguru import logger
from datetime import datetime
import numpy as np

ts_format = '%Y-%m-%d %H:%M:%S.%f'


def prepare_output(df, n_rows, interval='1T', column='service_instance'):
    """It ensures that data is ready for prediction"""

    df.set_index(pd.to_datetime(df['timestamp']), inplace=True)

    logger.debug(f"Min: {df['timestamp'].min()}")
    logger.debug(f"Max: {df['timestamp'].max()}")

    df = df.iloc[:, 1:]

    df = aggregate_df(df, interval, column)
    logger.debug(f"Df shape after aggregation: {df.shape}")

    # check missing value
    # if not is_df_admissible(df, 40):
    #     return

    # check shape
    df = adjust_shape(df, n_rows)

    df = interpolate_missing_values(df, 'linear')

    # check again
    if not is_df_admissible(df, 40):
        return

    logger.debug(f"Output shape: {df.values.shape}")

    return df.values


def aggregate_df(df, interval='1T', column='service_instance'):
    """Performs an aggregation on a timeseries based df with the given interval and column"""

    grouper = df.groupby([pd.Grouper(freq=interval, dropna=False), column])
    df = grouper.mean().unstack()

    # fill empty intervals
    df = df.resample(interval).mean()

    return df


def is_df_admissible(df, accepted_error=50) -> bool:
    """Checks nan values of a given df. If there are a lot of nans, it outputs an error"""
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)

    for mis_val_percent in mis_val_table.iloc[:, 1]:
        if mis_val_percent > accepted_error:
            logger.error(f"Found a percentage of {mis_val_percent} missing values.")
            return False
    return True


def interpolate_missing_values(df, method='linear'):
    for column in df:
        df[column] = df[column].interpolate(method=method).ffill().bfill()

    return df


def adjust_shape(df, n_rows):
    # longer than requested
    if df.shape[0] > n_rows:
        logger.debug(f"Adjusting size from {df.shape[0]} to {n_rows}")
        # df = df.tail(n_rows)
        df = df.iloc[-n_rows:]

    # shorter than requested
    if df.shape[0] < n_rows:
        logger.error(f"Dataframe has {df.shape[0]} rows. Minimum is {n_rows}")
        raise HTTPException(
            status_code=404,
            detail=f"Not enough current data is available.",
        )

    return df


def read_timestamp(str_ts):
    logger.debug(str_ts)
    try:
        ts_init = datetime.strptime(str_ts, ts_format)
        return ts_init
    except ValueError:
        logger.error(f"Provide a timestamp in valid format: {ts_format}. You provided: {str_ts}")
        raise HTTPException(
            status_code=400,
            detail=f"Provide a timestamp in valid format: {ts_format}. You provided: {str_ts}"
        )
