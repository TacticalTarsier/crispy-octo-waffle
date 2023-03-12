import pandas as pd

from typing import Dict
import numpy as np

from scipy.sparse import csr_matrix


class UserItemMatrix:
    def __init__(self, sales_data: pd.DataFrame):
        """
        Class initialization. You can make necessary
        calculations here.

        Args:
            sales_data (pd.DataFrame): Sales dataset.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36
        """
        self.sales_data = sales_data

    # @staticmethod
    def user_count(self) -> int:
        """
        Returns:
            int: the number of users in sales_data.
        """
        return self.sales_data['user_id'].nunique()

    # @staticmethod
    def item_count(self) -> int:
        """
        Returns:
            int: the number of items in sales_data.
        """
        return self.sales_data['item_id'].nunique()

    # @staticmethod
    def user_map(self) -> Dict[int, int]:
        """Creates a mapping from user_id to matrix rows indexes.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36

            user_map (Dict[int, int]):
                {1: 0, 2: 1, 4: 2, 5: 3}

        Returns:
            Dict[int, int]: User map
        """
        return {v: k for k, v in enumerate(self.sales_data['user_id'].sort_values().unique())}

    # @staticmethod
    def item_map(self) -> Dict[int, int]:
        """Creates a mapping from item_id to matrix rows indexes.

        Example:
            sales_data (pd.DataFrame):

                user_id  item_id  qty   price
            0        1      118    1   626.66
            1        1      285    1  1016.57
            2        2     1229    3   518.99
            3        4     1688    2   940.84
            4        5     2068    1   571.36 

            item_map (Dict[int, int]):
                {118: 0, 285: 1, 1229: 2, 1688: 3, 2068: 4}

        Returns:
            Dict[int, int]: Item map
        """
        return {v: k for k, v in enumerate(self.sales_data['item_id'].sort_values().unique())}

    # @staticmethod
    def csr_matrix(self):
        """User items matrix in form of CSR matrix.

        User row_ind, col_ind as
        rows and cols indecies (mapped from user/item map).

        Returns:
            csr_matrix: CSR matrix
        """
        users = self.user_map()
        items = self.item_map()
        temp_df = self.sales_data.copy()
        temp_df['user_id'] = temp_df['user_id'].apply(lambda x: users[x])
        temp_df['item_id'] = temp_df['item_id'].apply(lambda x: items[x])
        return csr_matrix((np.array(temp_df['qty']), (np.array(temp_df['user_id']), np.array(temp_df['item_id']))))
