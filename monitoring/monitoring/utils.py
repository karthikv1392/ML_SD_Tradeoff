import pandas as pd
from loguru import logger
import numpy as np


def prepare_output(df, interval='1T', column='service_instance'):
    """It ensures that data is ready for prediction"""

    df.set_index(pd.to_datetime(df['timestamp']), inplace=True)

    df = df.iloc[:, 1:]

    logger.debug(df.head())
    df = aggregate_df(df, interval, column)
    logger.debug(df.head())
    logger.debug(f"Df shape after aggregation: {df.shape}")
    # check missing value
    if not is_df_admissible(df, 40):
        return

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
