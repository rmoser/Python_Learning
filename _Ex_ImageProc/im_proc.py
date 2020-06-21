import PIL.Image
import PIL.ImageWin

import _Ex_kmeans.km as km
import numpy as np
import scipy as sp
import scipy.cluster
import scipy.spatial
import matplotlib.pyplot as plt
from os import path
import os
import sys


def read_pic(filename):
    # Reads data from JPEG filename
    # Returns numpy 2-d matrix with image data
    pic = PIL.Image.open(filename)
    pic.load()
    # pic = PIL.ImageOps.equalize(pic)
    # size = pic.size  # PIL size returns pixels in (y, x)
#    return np.asarray(pic, dtype="uint8").reshape(pic.size)
    return pic


def show_pic(image, colormap=0):
    if isinstance(image, np.ndarray):
        img = PIL.Image.fromarray(image.astype(np.uint8))
    else:
        img = image
    img.show()


def pic_km(image, k=None):
    if  k is None:
        k = 10

    if isinstance(image, PIL.Image.Image):
        arr = np.asarray(image)
    else:
        arr = image

    flat = arr.reshape(-1, 4)  # Other color formats?
    clusters, score = sp.cluster.vq.kmeans(flat.astype(float), k)  # Run Kmeans
    assigned, score2 = sp.cluster.vq.vq(flat, clusters)  # Assign cluster id to each pixel
    new = clusters.round(0).astype(np.uint8)[assigned]  # Generate pixel-clustered image flat array
    new = new.reshape(arr.shape)  # Reshape to original image x/y dimensions

    if isinstance(image, PIL.Image.Image):
        return PIL.Image.fromarray(new)
    return new


def dist(a, b):
    return sp.spatial.distance.euclidean(a, b)


def name():
    return sys._getframe().f_code.co_name


def grid(images, shape):
    if np.iterable(images):
        indices = range(np.prod(shape[:2]))

    elif isinstance(images, PIL.Image.Image):
        images = [images]
        indices = np.zeros(shape, dtype=np.uint8)
    else:
        raise TypeError(f"ERROR in grid():  images arg should be list of PIL Images: {images}")


if __name__ == '__main__':
    folder = r'C:\Users\rmose\Desktop\pics'
    file = path.join(folder, 'IMG_0114.PNG')
    folder = os.path.join(folder, "Gavin")
    if not os.path.isdir(folder):
        os.mkdir(folder)

    pic = read_pic(file)
    # print(pic.shape)
    # pic.show()

    dims = tuple(x//2 for x in pic.size)

    small = pic.resize(dims)
    small.save(os.path.join(folder, "Gavin_99.png"))

    image = PIL.Image.new('RGB', (small.width*5, small.height*4))
    for y in range(4):
        for x in range(5):
            i = x + y * 5
            print(f"Processing Image {i}...")
            if i == 0:
                image.paste(small, (0, 0))
            else:
                img = pic_km(small, 21 - i)  # .resize(small.size)
                img.save(os.path.join(folder, f"Gavin_{str(21-i).zfill(2)}.png"))
                image.paste(img, (x * small.width, y * small.height))

    image.save(path.join(folder, 'Gavin Baseball Kmeans.PNG'))

