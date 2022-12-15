"""import pandas to deal with df"""
import pandas as pd


def fillna_with_mean(df: pd.DataFrame, target: str, group: str) -> pd.DataFrame:
    """func fills NaNs with means of target and group columns

    Args:
        df_to_change (pd.DataFrame): df to change
        target (str): target column name
        group (str): group column name

    Returns:
        pd.DataFrame: df with filled with mean NaNs
    """
    grouped = df.groupby(group, as_index=False)[target].mean()

    d_of_means = {row[group]: row[target]
                  for _, row in grouped.iterrows()}
    copy_df = df.copy()

    copy_df[target].index = copy_df[group]
    copy_df[target] = copy_df[target].fillna(value=d_of_means).values

    return copy_df
