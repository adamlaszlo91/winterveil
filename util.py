import numpy as np


def normalize(item: np.ndarray) -> np.ndarray:
    """
    Scale the elements of input to be between 0 and 1
    """
    return (item-np.min(item)) / \
        (np.max(item)-np.min(item))
