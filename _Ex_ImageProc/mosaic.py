import _Ex_ImageProc.im_proc as im_proc
import PIL
import PIL.Image
import PIL.ImageFile
import os
import glob
import numpy as np


def mosaic(img, images, grid=None):
    (x_size, y_size) = img.size

    if grid is None:
        grid = (12, 8)

    if not len(grid) == 2:
        raise ValueError(f"grid must be a tuple of length 2: {grid}")

    x_small = x_size // grid[0]
    y_small = y_size // grid[1]

    #print(f"x_small, y_small: {x_small}, {y_small}")
    n = len(images)
    _images = [_img.resize(size=(x_small, y_small)) for _img in images]
    #print("img size: ", _images[0].size)

    image_mosaic = np.zeros(shape=(y_small * grid[1], x_small * grid[0], 3), dtype=np.uint8)

    for x in range(grid[0]):
        for y in range(grid[1]):
            #print(f"x,y: {x}, {y}")
            small = img.crop((x * x_small, y * y_small, (x+1)*x_small, (y+1)*y_small))

            nearest = im_proc.nearest(small, _images)
            image_mosaic[y * y_small:(y+1)*y_small, x * x_small:(x+1)*x_small] = np.asarray(nearest)

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
                crop = img.crop((left, 0, y, left + y))  # Center crop to square
            else:
                top = (y-x) // 2
                crop = img.crop((0, top, x, top + x))  # Center crop to square

            small = crop.resize(size)

            small.save(os.path.join(out_folder, outfull))


def get_images(folder):
    return [im_proc.read_pic(file) for file in glob.glob(os.path.join(folder, "*.jp*"))]


