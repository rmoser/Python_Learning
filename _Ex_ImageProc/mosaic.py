import _Ex_ImageProc.im_proc as im_proc
import PIL
import PIL.Image
import PIL.ImageFile
import os
import glob
import numpy as np


def mosaic(img, images):
    (x_size, y_size) = img.size

    x_small = x_size // 12
    y_small = y_size // 8

    #print(f"x_small, y_small: {x_small}, {y_small}")
    n = len(images)
    _images = [_img.resize(size=(x_small, y_small)) for _img in images]
    #print("img size: ", _images[0].size)

    image_mosaic = np.zeros(shape=(y_small * 8, x_small * 12, 3), dtype=np.uint8)

    for x in range(12):
        for y in range(8):
            print(f"x,y: {x}, {y}")
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


