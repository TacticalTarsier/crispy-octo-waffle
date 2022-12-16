"""Import modules"""
import pandas as pd
import numpy as np


def limit_gmv(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns df corrected by conditions

    Parameters
    ----------
    df : pd.DataFrame
        df with predictions

    Returns
    -------
    pd.DataFrame
        corrected df

    """

    df_cor = df.copy()

    df_cor['gmv'] = np.where(np.floor(df_cor['gmv'] / df_cor['price']) > df_cor['stock'],
                             df_cor['price'] * df_cor['stock'],
                             df_cor['price'] * np.floor(df_cor['gmv'] / df_cor['price']))

    return df_cor
