import sys
import cv2
import torch
import numpy as np
import random

from snowflake_generator import SnowflakeGenerator


def get_depth_map(image: np.ndarray) -> np.ndarray:
    model_type = "DPT_Hybrid"
    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
    input_batch = transform(image)
    midas.eval()

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    return prediction.numpy()


def add_fog(image: np.ndarray, depth_map: np.ndarray) -> np.ndarray:
    # Normalize depth values to be between 0 and 1
    depth_map = (depth_map-np.min(depth_map)) / \
        (np.max(depth_map)-np.min(depth_map))
    # Inverse the depth as MiDaS sets higher values to closer locations
    depth_map = 1 - depth_map
    # Create alpha channels for RGB matrix multiplication
    depth_mask = cv2.merge([depth_map, depth_map, depth_map])

    height, width, channels = image.shape
    fog = np.ones((height, width, channels), dtype=np.uint8) * 255
    foggy_image = (fog * depth_mask + image *
                   (1 - depth_mask)).astype(np.uint8)

    return foggy_image


def add_snow(image: np.ndarray, depth_map: np.ndarray, generator: SnowflakeGenerator, count: int) -> np.ndarray:
    # Normalize depth values to be between 0 and 1
    depth_map = (depth_map-np.min(depth_map)) / \
        (np.max(depth_map)-np.min(depth_map))

    height, width, _ = image.shape
    snowy_image = image.copy()

    snowflake_size = 60

    # Put snowflakes onto random 3d coordinates and manipulate them
    # according to their z coordinate and depth map
    for _ in range(count):
        x = random.randint(0, width - snowflake_size - 1)
        y = random.randint(0, height - snowflake_size - 1)
        z = random.uniform(0, 1)
        if z > depth_map[y][x]:
            snowflake, snowflake_mask = generator.generate(
                size=snowflake_size, blur_multiplier=(1-z) / 2)

            original_window = snowy_image[y:y +
                                          snowflake_size, x:x+snowflake_size]
            snowy_image[y:y+snowflake_size, x:x+snowflake_size] = (
                snowflake*snowflake_mask + original_window * (1-snowflake_mask))

    return snowy_image


def main() -> None:
    if len(sys.argv) < 2:
        print('Please provide the image path.')
        return

    try:
        image = cv2.imread(sys.argv[1])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        print('Please provide a valid image path.')
        return

    depth_map = get_depth_map(image=image)
    cv2.imwrite('out/depth_map.png', depth_map)
    output = image
    # output = add_fog(image=output, depth_map=depth_map)
    output = add_snow(image=output, depth_map=depth_map,
                      generator=SnowflakeGenerator(), count=100)

    cv2.imwrite('out/output.png',
                cv2.cvtColor(output, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()
