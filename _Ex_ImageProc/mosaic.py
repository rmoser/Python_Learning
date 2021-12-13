import _Ex_ImageProc.im_proc as im_proc
import PIL
import PIL.Image
import PIL.ImageFile
import os
import glob
import numpy as np
import shutil


def mosaic(img, images, grid=None, fast=False, enlarge=False):
    (x_size, y_size) = img.size

    if grid is None:
        grid = (12, 8)

    if not len(grid) == 2:
        raise ValueError(f"grid must be a tuple of length 2: {grid}")

    # Scan images to ensure all have same size
    images_size = images_min_size(images)
    if all([img.size == images_size for img in images]):
        _images = images
    else:
        _images = images_resize(images_size, images)

    # Size in pixels of each section of target image to convert to a mosaic tile
    x_tile = x_size // grid[0]
    y_tile = y_size // grid[1]

    if enlarge:
        # Assemble mosaic with full-size image tiles
        # New image will likely have different size than original
        x_insert, y_insert = images_size
    else:
        # Assemble mosaic with resized image tiles
        # New image will be (nearly) the same size as the original
        x_insert, y_insert = x_tile, y_tile

    # print(f"x_small, y_small: {x_small}, {y_small}")
    n = len(images)
    # Try converting to array here
    # _images = [_img.resize(size=(x_small, y_small)) for _img in images]
    _images = np.array([np.array(_img.resize(size=(x_tile, y_tile)), dtype=np.uint8) for _img in images])
    # print("img size: ", _images[0].size)

    image_mosaic = np.zeros(shape=(y_insert * grid[1], x_insert * grid[0], 3), dtype=np.uint8)

    for x in range(grid[0]):
        for y in range(grid[1]):
            #print(f"x,y: {x}, {y}")
            small = img.crop((x * x_tile, y * y_tile, (x+1) * x_tile, (y+1) * y_tile))

            nearest = im_proc.nearest(small, _images, fast=fast)
            image_mosaic[y * y_insert:(y+1)*y_insert, x * x_insert:(x+1)*x_insert] = np.asarray(nearest)

            #PIL.Image.fromarray(image_mosaic).show()

    return PIL.Image.fromarray(image_mosaic)


def images_resize(size, in_folder, out_folder):
    for filepath in glob.glob(os.path.join(in_folder, "*.jp*")):
        path, file = os.path.split(filepath)
        base, ext = os.path.splitext(file)
        outfull = base + "_small" + ext
        print(base, ext, outfull)
#        continue

        img = None
        try:
            img = im_proc.read_pic(filepath)
        except TypeError:
            raise

        if isinstance(img, PIL.Image.Image):
            x, y = img.size
            if x == y:
                crop = img  # Already square
            elif x > y:
                left = (x-y) // 2
                crop = img.crop((left, 0, left + y, y))  # Center crop to square
            else:
                top = (y-x) // 2
                crop = img.crop((0, top, x, top + x))  # Center crop to square

            small = crop.resize(size)

            small.save(os.path.join(out_folder, outfull))


def get_images(folder):
    return [im_proc.read_pic(file) for file in glob.glob(os.path.join(folder, "*.jp*"))]


def images_min_size(images):
    x = np.min([img.size[0] for img in images])
    y = np.min([img.size[1] for img in images])
    return x, y


def images_delete_small(size, folder):
    for filepath in glob.iglob(os.path.join(folder, "*.jp*")):
        path, file = os.path.split(filepath)
        base, ext = os.path.splitext(file)
        print(base, ext)
        #        continue

        img = None
        try:
            img = im_proc.read_pic(filepath)
        except TypeError:
            raise

        if isinstance(img, PIL.Image.Image):
            x, y = img.size
            if x < size[0] or y < size[1]:
                os.remove(filepath)



