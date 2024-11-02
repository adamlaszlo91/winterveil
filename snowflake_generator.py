import cv2


class SnowflakeGenerator:

    def __init__(self):
        self._snowflake = cv2.imread('snowflake.png', cv2.IMREAD_UNCHANGED)
        self._snowflake = cv2.cvtColor(self._snowflake, cv2.COLOR_BGRA2RGBA)

    def generate(self, size: int, blur_multiplier: float) -> tuple:
        snowflake = self._snowflake.copy()
        snowflake = cv2.resize(snowflake, (size, size))
        blur_kernel_size = max(1, int(size * blur_multiplier))
        snowflake = cv2.blur(
            snowflake, (blur_kernel_size, blur_kernel_size))
        mask = snowflake[:, :, 3] / 255
        mask = cv2.merge([mask, mask, mask])
        return snowflake[:, :, :3], mask
