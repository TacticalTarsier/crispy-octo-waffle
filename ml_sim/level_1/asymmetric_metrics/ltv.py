"""import module"""
import numpy as np


def ltv_error(y_true: np.array, y_pred: np.array) -> float:
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
        error metric
    """

    return np.mean(np.where(y_true - y_pred < 0, np.abs(y_true - y_pred)
                            ** 0.5, y_true - y_pred))
