import cv2
import numpy as np


class SnowflakeGenerator:

    def __init__(self):
        self._snowflake = cv2.imread(
            'asset/snowflake.png', cv2.IMREAD_UNCHANGED)
        self._snowflake = cv2.cvtColor(self._snowflake, cv2.COLOR_BGRA2RGBA)

    def generate(self, size: int, distance_ratio: float) -> tuple:
        """
        Creates a new snowflake RGB image and RGB mask based on the given parameters
        """
        snowflake = self._snowflake.copy()
        snowflake = self._resize(
            snowflake=snowflake, size=size, distance_ratio=distance_ratio)
        snowflake = self._blur(snowflake=snowflake,
                               size=size, distance_ratio=distance_ratio)
        mask = snowflake[:, :, 3] / 255
        mask = cv2.merge([mask, mask, mask])
        return snowflake[:, :, :3], mask

    def _resize(self, snowflake: np.ndarray, size: int, distance_ratio: float) -> np.ndarray:
        """
        Resizes the input depending on its distance, keeps canvas size
        """
        size_multiplier = distance_ratio
        new_size = max(1, int(size * size_multiplier))
        small_image = cv2.resize(snowflake, (new_size, new_size))
        canvas = np.ones((size, size, 4), dtype=np.uint8)
        offset = (size - new_size) // 2
        canvas[offset:offset+new_size, offset:offset+new_size] = small_image
        return canvas

    def _blur(self, snowflake: np.ndarray, size: int, distance_ratio: float) -> np.ndarray:
        """
        Blurs the input depending on its distance
        """
        blur_multiplier = (1-distance_ratio) / 2
        blur_kernel_size = max(1, int(size * blur_multiplier))
        return cv2.blur(snowflake, (blur_kernel_size, blur_kernel_size))
