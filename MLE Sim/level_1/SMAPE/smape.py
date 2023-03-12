"""import numpy for array calculations"""
import numpy as np


def smape(y_true: np.array, y_pred: np.array) -> float:
    """returns sMAPE between two arrays

    Args:
        y_true (np.array): array of true values
        y_pred (np.array): array of predicted values

    Returns:
        float: sMAPE
    """
    return 2 * (np.mean(np.nan_to_num(np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred)))))
