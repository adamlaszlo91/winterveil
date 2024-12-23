import sys
import cv2
import torch
import numpy as np
import random
import util as util_
import argparse

from snowflake_generator import SnowflakeGenerator


def get_depth_map(image: np.ndarray) -> np.ndarray:
    model_type = "DPT_Hybrid"
    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    midas.eval()
    transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
    input_batch = transform(image)

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
    depth_mask = cv2.merge([depth_map, depth_map, depth_map])
    height, width, channels = image.shape
    fog = np.ones((height, width, channels), dtype=np.uint8) * 255
    foggy_image = (fog * (1-depth_mask) + image *
                   depth_mask).astype(np.uint8)
    return foggy_image


def add_snow(image: np.ndarray, depth_map: np.ndarray, generator: SnowflakeGenerator, snowflake_size: int, count: int) -> np.ndarray:
    height, width, _ = image.shape
    snowy_image = image.copy()

    # Put snowflakes onto random 3d coordinates and manipulate them
    # according to their z coordinate and depth map
    for _ in range(count):
        x = random.randint(0, width - snowflake_size - 1)
        y = random.randint(0, height - snowflake_size - 1)
        z = random.uniform(0, 1)
        if z > depth_map[y][x]:
            snowflake, snowflake_mask = generator.generate(
                size=snowflake_size, distance_ratio=z)

            original_window = snowy_image[y:y +
                                          snowflake_size, x:x+snowflake_size]
            snowy_image[y:y+snowflake_size, x:x+snowflake_size] = (
                snowflake*snowflake_mask + original_window * (1-snowflake_mask))

    return snowy_image


def add_fallen_snow(image: np.ndarray, depth_map: np.ndarray) -> np.ndarray:
    height, width, _ = image.shape
    snowy_image = image.copy()

    sobelx = cv2.Sobel(depth_map * 255, cv2.CV_64F, 0, 1, ksize=5)
    sobel_magnitude = cv2.convertScaleAbs(sobelx)
    _, edges = cv2.threshold(
        sobel_magnitude, 250, 255, cv2.THRESH_BINARY)

    for row in range(height):
        for col in range(width):
            intensity = (1 - depth_map[row, col]) * 0.8
            if edges[row, col] == 255 and random.uniform(0, 1) < intensity:
                cv2.circle(snowy_image, (col, row), radius=1,
                           color=(255, 255, 255), thickness=-1)

    return snowy_image


def setup_argparse():
    parser = argparse.ArgumentParser(
        prog='WinterVeil')
    parser.add_argument('-i', '--image', required=True,
                        help='input image path')
    parser.add_argument('-f', '--fog',
                        action='store_true', help='add fog to the image')
    parser.add_argument('-s', '--snow',
                        action='store_true', help='add snow to the image')
    parser.add_argument('-ss', '--snowflake-size',
                        default=12, type=int, help='size of snowflakes in pixel')
    parser.add_argument('-sc', '--snowflake-count',
                        default=400, type=int, help='number of snowflakes on image (visibility depends on depth map!)')
    parser.add_argument('-fs', '--fallen-snow',
                        action='store_true', help='add fallen snow to the image')
    return parser.parse_args()


def main() -> None:
    args = setup_argparse()

    try:
        image = cv2.imread(args.image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        print('Please provide a valid image path.')
        return

    depth_map = get_depth_map(image=image)
    # Normalize depth map to make usage easier
    depth_map = util_.normalize(item=depth_map)
    cv2.imwrite('out/depth_map.png', depth_map * 255)

    output = image

    if args.fallen_snow:
        output = add_fallen_snow(image=output, depth_map=depth_map)
    if args.snow:
        output = add_snow(image=output, depth_map=depth_map,
                          generator=SnowflakeGenerator(), snowflake_size=args.snowflake_size, count=args.snowflake_count)
    if args.fog:
        output = add_fog(image=output, depth_map=depth_map)

    cv2.imwrite(f'out/output{'_f' if args.fog else ''}{'_s' if args.snow else ''}{'_fs' if args.fallen_snow else ''}.png',
                cv2.cvtColor(output, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()
