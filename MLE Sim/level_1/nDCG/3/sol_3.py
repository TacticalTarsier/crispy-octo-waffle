from typing import List

import numpy as np


def normalized_dcg(relevance: List[float], k: int, method: str = "standard") -> float:
    """Normalized Discounted Cumulative Gain.

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    relevance = np.array(relevance[:k])
    sorted_relevance = -np.sort(-relevance)[:k]
    l_arr = np.log2(np.arange(2, k + 2))

    if method == 'standard':
        dcg = np.sum(relevance / l_arr)
        idcg = np.sum((np.power(2, sorted_relevance) - 1) /
                      (l_arr))
        return dcg / idcg
    if method == 'industry':
        dcg = np.sum((np.power(2, relevance) - 1) /
                     (l_arr))
        idcg = np.sum((np.power(2, sorted_relevance) - 1) /
                      (l_arr))
        return dcg / idcg
    raise ValueError
