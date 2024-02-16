import PIL.Image
import PIL.ImageWin
import PIL.ImageFilter

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

    # Not sure this is necessary
    # pic.load()

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


def pic_km(image, k=None, ratio=None):
    if not isinstance(image, PIL.Image.Image):
        raise TypeError(f"Requires PIL Image: {image}")

    if k is None:
        k = 10

    # 0 < ratio <= 1:  Reduces pixels to accelerate the Kmeans execution
    if ratio is None or ratio <= 0:
        ratio = 1

    if ratio > 1:
        ratio = 1 / ratio

    large = np.asarray(image)
    small = np.asarray(image.resize(size=np.ceil((image.width * ratio, image.height * ratio)).astype(int)))

    flat_large = large.reshape(-1, large.shape[-1])  # Flatten to one row per pixel
    flat_small = small.reshape(-1, large.shape[-1])

    clusters, score = sp.cluster.vq.kmeans(flat_small.astype(float), k)  # Run Kmeans

    assigned, score2 = sp.cluster.vq.vq(flat_large, clusters)  # Assign cluster id to each pixel in full image
    new = clusters.round(0).astype(np.uint8)[assigned]  # Generate pixel-clustered image flat array
    new = new.reshape(large.shape)  # Reshape to original image x/y dimensions

    if isinstance(image, PIL.Image.Image):
        return PIL.Image.fromarray(new)
    return new


def pic_toon(image):
    pic_med = image.filter(PIL.ImageFilter.MedianFilter(7))
    pic_edge0 = pic_med.filter(PIL.ImageFilter.FIND_EDGES)
    pic_edge1 = pic_edge0.filter(PIL.ImageFilter.MaxFilter(3))


def dist(a, b):
    """
        Returns distance between two images.  Squared sum of differences in pixel values
        Image sizes must match in size (x, y), color encoding (rgb), and bits per pixel
    """

    if not isinstance(a, np.ndarray):
        a = np.asarray(a)

    if not isinstance(b, np.ndarray):
        b = np.asarray(b)

    return sp.spatial.distance.euclidean(a.flatten().astype(int), b.flatten().astype(int))


def dists(i, arr):
    """
        Calculates distance of image (i) from an array of images (arr)
        Returns array of floats with dimensions matching arr
    """
    return [dist(i, img) for img in arr]


def nearest(i, arr, fast=False):
    """
        Returns img from arr nearest (min distance from) target image i
    """
    if fast:
        arr = np.mean(np.array([np.array(i) for i in arr]), axis=(1, 2))
        i = np.mean(np.array(i), axis=(1, 2))

    d = np.asarray(dists(i, arr))
    idx = np.argmin(d)
    return arr[idx]


def name():
    return sys._getframe().f_code.co_name


def _calc_grid(n=None, aspect_ratio=None, image_aspect_ratio=None):
    if not aspect_ratio:
        aspect_ratio = 16/9.
    elif np.iterable(aspect_ratio):
        if len(aspect_ratio) >= 2:
            aspect_ratio = aspect_ratio[0] / aspect_ratio[1]
        else:
            aspect_ratio = aspect_ratio[0]

    if not image_aspect_ratio:
        img_aspect_ratio = 1
    elif np.iterable(image_aspect_ratio):
        if len(image_aspect_ratio) >= 2:
            img_aspect_ratio = image_aspect_ratio[0] / image_aspect_ratio[1]
        else:
            img_aspect_ratio = image_aspect_ratio[0]

    if not np.issubdtype(type(n), np.integer):
        if np.iterable(n):
            n = len(n)
        elif np.issubdtype(type(n), np.float):
            n = np.uint(np.abs(n))
        else:
            n = 1

    # Defines desired aspect ratio for grid
    _x = aspect_ratio / image_aspect_ratio
    _y = 1

    v = (n / _x * _y) ** 0.5
    y = int(round(v, 0))
    x = int(n / y)
    while n > y * x:
        x += 1
    # print(f"n: {n}  v: {v}  xy: {x} {y}")
    return x, y


def grid(images, shape=(), repeat=False, scale=None):
    if not np.iterable(images):
        images = [images]

    for i, img in enumerate(images):
        if np.issubdtype(type(img), np.str_) and os.path.exists(img):
            images[i] = PIL.Image.open(img)

    repeat = bool(repeat)

    if scale is None or scale <= 0:
        scale = 1

    # Image dimensions
    img_width = np.max([x.width for x in images]) * scale
    img_height = np.max([x.height for x in images]) * scale
    mode = images[0].mode

    if not shape:
        shape = _calc_grid(images, aspect_ratio=None, image_aspect_ratio=img_width / img_height)

    if np.issubdtype(type(shape), np.integer):
        shape = (shape, 1)

    # Grid dimensions
    grid_width, grid_height = shape

    indices = np.arange(np.prod(shape[:2])) % len(images)

    image = PIL.Image.new(mode, size=(img_width * grid_width, img_height * grid_height))

    # Convert all images to same color mode
    for i in images:
        if i.mode != mode:
            images[i] = i.convert(mode)

    for i in range(len(indices)):
        index = i % len(images)
        x = i % grid_width
        y = i // grid_width

        img = images[index]
        if scale != 1:
            img = img.resize(size=(img.width * scale, img.height * scale))

        image.paste(img, (x * img_width, y * img_height))

        if i == len(images) - 1 and not repeat:
            break

    return image


if __name__ == '__main__':
    file = 'IMG_6158.jpg'
    folder = r'C:\Users\rmose\Desktop\pics'
    file = path.join(folder, file)
    base, ext = os.path.splitext(file)
    folder = os.path.join(folder, "Mystic")
    if not os.path.isdir(folder):
        os.mkdir(folder)

    pic = read_pic(file)
    # Output as jpg
    pic = pic.convert('RGB')
    ext = '.jpg'
    # print(pic.shape)
    # pic.show()

    dims = tuple(int(x) for x in pic.size)

    #small = pic.resize(dims)
    small = pic

    nm = "Mystic"
    outfull = os.path.join(folder, f"{nm}___{ext}")
    if not os.path.exists(outfull):
        small.save(outfull)

    ratio = np.max((0.1, np.min((1., 10000 / np.prod(pic.size)))))
    print(f"Ratio: {ratio}")

    for i in range(2, 20):
        outfile = f"{nm}_{str(i).zfill(2)}{ext}"
        outfull = os.path.join(folder, outfile)
        if os.path.exists(outfull):
            print(f"Already have Image {i}: {outfile}...")
            continue

        print(f"Processing Image {i}: {outfile}...")
        img = pic_km(small, i, ratio=0.2)  # .resize(small.size)
        img.save(os.path.join(folder, outfull))
        continue

