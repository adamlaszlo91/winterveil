import cv2


class Core:
    def __init__(self):
        self.cv_image = None

    def load_image(self, path: str) -> None:
        if path:
            print(f'Loading image: {path}')
            # TODO: Handle error
            self.cv_image = cv2.imread(path)
