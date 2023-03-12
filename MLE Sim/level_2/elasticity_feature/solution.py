'''
import modules
'''

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def elasticity_df(purchases_df: pd.DataFrame) -> pd.DataFrame:
    """
    _summary_

    Parameters
    ----------
    purchases_df : pd.DataFrame
        DataFrame with purchases info

    Returns
    -------
    pd.DataFrame
        DataFrame with elasticity info by sku
    """

    purchases_df.loc[:, 'qty_log'] = np.log(purchases_df['qty'] + 1)

    features = purchases_df.groupby('sku')['qty_log']\
        .apply(list)\
        .reset_index(name='log_qty')

    target = purchases_df.groupby('sku')['price']\
        .apply(list)\
        .reset_index(name='price')

    merged = target.merge(features)

    sku = []
    elasticity = []

    for _, val in merged.iterrows():
        sku.append(val['sku'])
        sku_prices = np.array(val['price']).reshape(-1, 1)
        sku_qtys = np.array(val['log_qty']).reshape(-1, 1)
        linear_model = LinearRegression()
        elasticity.append(linear_model.fit(X=sku_prices, y=sku_qtys).score(sku_prices, sku_qtys))

    return pd.DataFrame({'sku': sku,
                         'elasticity': elasticity})
