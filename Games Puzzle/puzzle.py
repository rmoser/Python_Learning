import sklearn
import skimage
import skimage.filters
import skimage.transform

import PIL.Image
from pathlib import Path
import numpy as np


def show(arr):
    PIL.Image.fromarray(arr).show()


def inverse(arr):
    return skimage.filters.inverse(arr)


def clean(arr, size=5):
    if not size % 2:
        size += 1
    return skimage.filters.threshold_niblack(npimg, size) > 128


def crop(arr):
    pass


theta = np.arange(0, 2 * np.pi, np.pi / 720)
sin_theta = np.sin(theta)
cos_theta = np.cos(theta)


def detect_locus(arr, x, y):
    n = 0
    for i, angle in enumerate(theta):
        mask = np.zeros(arr.shape, bool)
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        for r in range(20):
            _y = np.int(y + r * sin_theta)
            _x = int(x + r * cos_theta)
            if _y <= arr.shape[0] and _x <= arr.shape[1]:
                mask[_y, _x] = True
            if np.sum(mask * arr) > 18 * 255:
                n += 1
    return n


if __name__ == '__main__':
    folder = Path("./Games Puzzle")
    filename = "puzzle.png"

    imagefile = folder / filename
    image = PIL.Image.open(imagefile)

    # Import as np array, and invert to white on black
    npimg = 255 - np.asarray(image.convert('L'))
    img = clean(npimg)




