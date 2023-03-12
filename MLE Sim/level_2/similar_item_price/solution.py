"""Import libs"""

from typing import Dict, Tuple, List
from itertools import combinations
import numpy as np


class SimilarItems():
    """Class for calculation prices of similar products"""
    @staticmethod
    def similarity(embeddings: Dict[int, np.ndarray]) -> Dict[Tuple[int, int], float]:
        """Calculate pairwise similarities between each item
        in embedding.

        Args:
            embeddings (Dict[int, np.ndarray]): Items embeddings.

        Returns:
            Tuple[List[str], Dict[Tuple[int, int], float]]:
            List of all items + Pairwise similarities dict
            Keys are in form of (i, j) - combinations pairs of item_ids
            with i < j.
            Round each value to 8 decimal places.
        """
        possible_combinations = list(combinations(embeddings.keys(), 2))

        def get_similarity(first_product: np.array, second_product: np.array) -> float:
            """
            Func calculates cosine distance between embeddings

            Parameters
            ----------
            first_product : np.array[float]
                first product embedding
            second_product : np.array[float]
                second product embedding

            Returns
            -------
            float
                Cosine distance
            """
            return round(sum(first_product * second_product) /
                         (np.sqrt(sum(first_product ** 2)) * np.sqrt(sum(second_product ** 2))), 8)

        result_dict = {}
        for i in possible_combinations:
            result_dict[i] = get_similarity(embeddings[i[0]], embeddings[i[1]])

        return result_dict

    @staticmethod
    def knn(
        sim: Dict[Tuple[int, int], float], top: int
    ) -> Dict[int, List[Tuple[int, float]]]:
        """Return closest neighbors for each item.

        Args:
            sim (Dict[Tuple[int, int], float]): <similarity> method output.
            top (int): Number of top neighbors to consider.

        Returns:
            Dict[int, List[Tuple[int, float]]]: Dict with top closest neighbors
            for each item.
        """
        sorted_dict = dict(
            sorted(sim.items(), key=lambda x: x[1], reverse=True))

        n = 1
        res_dict = {}
        for i in sorted_dict.items():
            res_dict[n] = list(i)
            n += 1

        return {i: res_dict[i] for i in list(res_dict.keys())[:top]}
