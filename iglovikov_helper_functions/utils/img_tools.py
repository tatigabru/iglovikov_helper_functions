import cv2
import numpy as np
import jpeg4py
from pathlib import Path
from PIL import Image
from typing import Tuple


def load_rgb(image_path: (Path, str), lib="cv2") -> np.array:
    """Load RGB image from path.

    Args:
        image_path: path to image
        lib: library used to read an image.
            currently supported `cv2` and `jpeg4py`

    Returns: 3 channel array with RGB image

    """
    if Path(image_path).is_file():
        if lib == "cv2":
            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif lib == "jpeg4py":
            image = jpeg4py.JPEG(str(image_path)).decode()
        else:
            raise NotImplementedError("Only cv2 and jpeg4py are supported.")
        return image

    raise FileNotFoundError(f"File not found {image_path}")


def load_grayscale(mask_path: (Path, str)) -> np.array:
    """Load grayscale mask from path

    Args:
        mask_path: Path to mask

    Returns: 1 channel grayscale mask

    """
    if Path(mask_path).is_file():
        return cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    raise FileNotFoundError(f"File not found {mask_path}")


def pad(image: np.array, factor=32, border=cv2.BORDER_REFLECT_101) -> tuple:
    """Pads the image on the sides, so that it will be divisible by factor.
    Common use case: UNet type architectures.

    Args:
        image:
        factor:
        border: cv2 type border.

    Returns: padded_image

    """
    height, width = image.shape[:2]

    if height % factor == 0:
        y_min_pad = 0
        y_max_pad = 0
    else:
        y_pad = factor - height % factor
        y_min_pad = y_pad // 2
        y_max_pad = y_pad - y_min_pad

    if width % factor == 0:
        x_min_pad = 0
        x_max_pad = 0
    else:
        x_pad = factor - width % factor
        x_min_pad = x_pad // 2
        x_max_pad = x_pad - x_min_pad

    padded_image = cv2.copyMakeBorder(image, y_min_pad, y_max_pad, x_min_pad, x_max_pad, border)

    return padded_image, (x_min_pad, y_min_pad, x_max_pad, y_max_pad)


def unpad(image: np.array, pads: list) -> np.array:
    """Crops patch from the center so that sides are equal to pads.

    Args:
        image:
        pads: (x_min_pad, y_min_pad, x_max_pad, y_max_pad)

    Returns: cropped image

    """
    x_min_pad, y_min_pad, x_max_pad, y_max_pad = pads
    height, width = image.shape[:2]

    return image[y_min_pad : height - y_max_pad, x_min_pad : width - x_max_pad]


def get_size(file_path: (str, Path)) -> Tuple[int, int]:
    """Gets size of the image in a lazy way.

    Args:
        file_path: Path to the target image.

    Returns: (width, height)

    """
    image = Image.open(file_path)
    width, height = image.size
    return width, height


def bgr2rgb(image):
    """Convert image from bgr to rgb format

    Args:
        image:

    Returns:

    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
