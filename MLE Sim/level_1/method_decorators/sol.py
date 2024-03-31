from __future__ import annotations
from typing import List


class BankMetrics:
    """
    A class to represent bank metrics.

    Attributes
    ----------
    global_bank_rate : float
        The global bank rate applicable to all accounts.
    accounts : List[BankMetrics]
        A list of BankMetrics instances representing bank accounts.

    Methods
    -------
    __init__(name: str, balance: float):
        Initializes a new BankMetrics instance with a name and balance.
    adjust_global_bank_rate(new_rate: float):
        Method to adjust the global bank rate.
    calculate_avg_balance() -> float:
        Method to calculate the average balance across all accounts.
    calculate_interest(account: BankMetrics) -> float:
        Method to calculate interest for a given account.
    """

    global_bank_rate: float = 15.0
    accounts: List[BankMetrics] = []

    def __init__(self, name: str, balance: float):
        self.name = name
        self.balance = balance
        BankMetrics.accounts.append(self)

    
    @classmethod
    def adjust_global_bank_rate(cls, global_bank_rate):
        cls.adjust_global_bank_rate = global_bank_rate

    @staticmethod
    def calculate_avg_balance(...) -> float:
        ...

    @staticmethod
    def calculate_interest(...) -> float:
        ...


if __name__ == "__main__":
    Account1 = BankMetrics("Tom", 15000)
    Account2 = BankMetrics("Jerry", 20000)
    Account3 = BankMetrics("Spike", 10000)

    assert BankMetrics.calculate_avg_balance() == 15000

    BankMetrics.adjust_global_bank_rate(16.0)
    assert BankMetrics.global_bank_rate == 16.0

    assert BankMetrics.calculate_interest(Account1) == 2400.0
