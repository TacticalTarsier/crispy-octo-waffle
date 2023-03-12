"""import module"""
import numpy as np


def turnover_error(y_true: np.array, y_pred: np.array) -> float:
    """
    Func calculates asymmetric error metric

    Parameters
    ----------
    y_true : np.array
        True values
    y_pred : np.array
        Predicted values

    Returns
    -------
    float
        RMSLE
    """
    y_t = np.where(y_true >= 0, y_true, 0)
    y_p = np.where(y_pred >= 0, y_pred, 0)

    return np.sqrt(np.mean((np.log(y_t + 1) - np.log(y_p + 1)) ** 2))
