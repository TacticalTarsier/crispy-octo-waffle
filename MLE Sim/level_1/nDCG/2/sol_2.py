from typing import List

import numpy as np


def discounted_cumulative_gain(relevance: List[float], k: int, method: str = "standard") -> float:
    """Discounted Cumulative Gain

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the valu
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    if method == 'standard':
        cor_rel = [v / (np.log2(i + 2)) for i, v in enumerate(relevance[:k])]
        return sum(cor_rel)
    if method == 'industry':
        cor_rel = [(2 ** v - 1) / (np.log2(i + 2)) for i, v in enumerate(relevance[:k])]
        return sum(cor_rel)
    else:
        raise ValueError
