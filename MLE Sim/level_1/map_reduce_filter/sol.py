from typing import List
from functools import reduce


def sales_with_tax(sales: List[float], tax_rate: float, threshold: float = 300) -> List[float]:
    """_summary_

    Args:
        sales (List[float]): _description_
        tax_rate (float): _description_
        threshold (float, optional): _description_. Defaults to 300.

    Returns:
        List[float]: _description_
    """
    sales_filtered = list(filter(lambda x: x > threshold, sales))
    sales_taxed = list(map(lambda x: x * (1 + tax_rate), sales_filtered))

    return sales_taxed


def sum_sales(sales: List[float], threshold: float = 300) -> float:
    """_summary_

    Args:
        sales (List[float]): _description_
        threshold (float, optional): _description_. Defaults to 300.

    Returns:
        float: _description_
    """
    sales_filtered = list(filter(lambda x: x > threshold, sales))
    sales_sum = float(reduce(lambda x, y: x+y, sales_filtered))

    return sales_sum


def average_age(ages: List[int], threshold: int = 30) -> float:
    """_summary_

    Args:
        ages (List[int]): _description_
        threshold (int, optional): _description_. Defaults to 30.

    Returns:
        float: _description_
    """
    ages_filtered = list(filter(lambda x: x > threshold, ages))
    ages_sum = reduce(lambda x, y: x+y, ages_filtered)
    ages_len = len(ages_filtered)

    return ages_sum / ages_len


def increased_prices(prices: List[float], increase_rate: int = 0.2, threshold: float = 300) -> List[float]:
    """_summary_

    Args:
        prices (List[float]): _description_
        increase_rate (int, optional): _description_. Defaults to 0.2.
        threshold (float, optional): _description_. Defaults to 300.

    Returns:
        List[float]: _description_
    """
    increased_prices = list(map(lambda x: x * (1 + increase_rate), prices))
    filtered_prices = list(filter(lambda x: x > threshold, increased_prices))

    return filtered_prices


def weighted_sale_price(sales: List[float]) -> float:
    """_summary_

    Args:
        sales (List[float]): _description_

    Returns:
        float: _description_
    """
    sales_cnt = int(reduce(lambda x, y: x + y, list(map(lambda x: x[1], sales))))
    sales_w = list(map(lambda x: x[0] * x[1], sales))

    return reduce(lambda x, y: x + y, sales_w) / sales_cnt