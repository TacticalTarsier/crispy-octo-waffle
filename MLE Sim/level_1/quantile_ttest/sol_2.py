from typing import List, Tuple

import numpy as np
from scipy.stats import ttest_ind


def bootstrapped_quantile(x: List[float], n_bootstraps: int = 10_000, quantile: float = 0.5) -> List[float]:
    """Bootstrapped median distribution"""
    bootstrapped = []

    for _ in range(n_bootstraps):
        bootstrapped_sample = np.random.choice(x, size=len(x), replace=True)
        bootstrapped.append(np.quantile(bootstrapped_sample, quantile))

    return bootstrapped


def quantile_ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
    quantile: float = 0.95,
    n_bootstraps: int = 1000,
) -> Tuple[float, bool]:
    """
    Bootstrapped t-test for quantiles of two samples.
    """
    control_quantiles = bootstrapped_quantile(control, quantile=quantile)
    experiment_quantiles = bootstrapped_quantile(experiment, quantile=quantile)

    _, p_value = ttest_ind(control_quantiles, experiment_quantiles)

    result = bool(p_value <= alpha)
    return p_value, result
