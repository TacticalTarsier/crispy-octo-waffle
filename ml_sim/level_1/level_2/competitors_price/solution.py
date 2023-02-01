"""
import useful docstrings
"""
import pandas as pd


def agg_comp_price(old_prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    computes new price by sku depending on agg func and comp price

    Parameters
    ----------
    X : pd.Dataframe
        dataframe with base prices and comp prices by sku

    Returns
    -------
    pd.DataFrame
        dataframe with new prices based on comp prices and agg func
    """

    d_of_agg_funcs = {'max': 'max',
                      'med': 'median',
                      'avg': 'mean',
                      'min': 'min'}

    comp_prices = []
    new_prices = []
    aggs = []
    base_prices = []

    for sku in old_prices_df['sku'].unique():
        temp_df = old_prices_df[old_prices_df['sku'] == sku]
        base_price = temp_df.iat[0, 3]

        if temp_df.iat[0, 1] != 'rnk':
            temp_price = temp_df['comp_price']\
                .agg(d_of_agg_funcs[temp_df.iat[0, 1]])
        else:
            temp_price = temp_df.iat[temp_df.reset_index(drop=True)
                                     ['rank'].idxmin(), 4]

        if -0.2 < (temp_price - base_price) / base_price < 0.2:
            new_price = temp_price
        else:
            new_price = base_price

        comp_prices.append(temp_price)
        new_prices.append(new_price)
        base_prices.append(base_price)
        aggs.append(temp_df.iat[0, 1])

    return pd.DataFrame({'sku': old_prices_df['sku'].unique(),
                         'agg': aggs,
                         'base_price': base_prices,
                         'comp_price': comp_prices,
                         'new_price': new_prices})
