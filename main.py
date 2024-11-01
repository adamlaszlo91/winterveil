import sys
import cv2
import torch
import numpy as np


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
    depth_map = cv2.merge([depth_map, depth_map, depth_map])

    height, width, channels = image.shape
    fog = np.ones((height, width, channels), dtype=np.uint8) * 255
    foggy_image = (fog * depth_map + image * (1 - depth_map)).astype(np.uint8)

    return foggy_image


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
    output = add_fog(image=image, depth_map=depth_map)
    cv2.imwrite('out/output.png', cv2.cvtColor(output, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()
