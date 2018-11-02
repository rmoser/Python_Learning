# MIT Data Science Case Study 1.1
# Facial Clustering

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import PIL.Image
import PIL.ImageOps

size = (0, 0)

def get_image_file_list(folder):
    try:
        folder_handle = Path(os.curdir).rglob(folder).__next__()
    except:
        raise FileNotFoundError("Folder not found: ", folder)

    if folder_handle.exists():
        files = list(folder_handle.rglob("*.pgm")) + list(folder_handle.rglob("*.jpg"))
        return [f for f in files if len(f.stem) <= 3]


def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)

    global size
    size = (height, width)

    return np.frombuffer(buffer,
                         dtype='u1' if int(maxval) < 256 else byteorder + 'u2',
                         count=int(width) * int(height),
                         offset=len(header)
                         ).flatten()  # .reshape((int(height), int(width)))


def read_pic(filename):
    # Reads data from JPEG filename
    # Returns numpy 2-d matrix with image data
    pic = PIL.Image.open(filename)
    pic.load()
    # pic = PIL.ImageOps.equalize(pic)

    global size
    size = pic.size  # PIL size returns pixels in (y, x)

#    return np.asarray(pic, dtype="uint8").reshape(pic.size)
    return np.asarray(pic).reshape(pic.size)



def show_pic(image):
    dims = np.ndim(image)
    if dims == 2:
        images = np.array([image])
    else:
        images = image
    grid = np.ceil(np.sqrt(len(images))).astype(int)
    f, axarr = plt.subplots(grid, grid)

    for i, img in enumerate(images):
        c = i % grid
        r = i // grid

        if grid == 1:
            # axarr will not be a matrix
            axarr.imshow(img, plt.cm.gray)
        else:
            # axarr[r, c].imshow(img, plt.cm.gray)
            axarr[r, c].imshow(img, plt.cm.gray)

    plt.show()


def get_image_data(source):
    pics = get_image_file_list(source)

    for p, pic in enumerate(pics):
        print("  ", pic)

        pictype = Path(pic).suffix.lower()
        if pictype == '.pgm':
            image = read_pgm(pic, byteorder='<')
        else:
            image = read_pic(pic)

        # Need to know the image size to create the matrix to store
        if p == 0:
            _size = image.shape
            pic_data = np.zeros((len(pics), _size[0], _size[1]))

        pic_data[p] = image

    # print(pic_data.shape)
    return pic_data


def get_mean_pic(pic):
    # This func returns the mean of mat(i,j) across all the matrices in pic

    # Some matrix ops need to be told to operate on a list of matrices
    # Assume the data stored in matrices, not arrays
    # So the last two dimensions define the matrix
    # The rest define the iterator dimensions
    if np.ndim(pic) <= 2:
        axes = None
    else:
        axes = tuple(np.arange(np.ndim(pic))[:-2])

    return np.mean(pic, axis=axes).astype(np.uint8)


def get_delta_pic(pic):
    # Element-wise subtraction
    return np.subtract(pic, get_mean_pic(pic))


def get_std_pic(pic):
    # This func returns the stdev of mat(i,j) across all the matrices in pic

    # Some matrix ops need to be told to operate on a list of matrices
    # Assume the data stored in matrices, not arrays
    # So the last two dimensions define the matrix
    if np.ndim(pic) <= 2:
        axes = None
    else:
        axes = tuple(np.arange(np.ndim(pic))[:-2])

    return np.std(pic, axis=axes)


def get_norm_pic(pic):
    # Some matrix ops need to be told to operate on a list of matrices
    # Assume the data stored in matrices, not arrays
    # So the last two dimensions define the matrix
    itr_axes = tuple(np.arange(np.ndim(pic))[:-2])
    mat_axes = tuple(np.arange(np.ndim(pic))[-2:])

    # Use this to reshape mean and std so regular math operators cast correctly
    shape = np.shape(pic)[:-2] + (1, 1)

    # Overall mean and stddev
    # um = get_mean_pic(pic)
    # us = get_std_pic(pic)

    # I think um and us are single values in the psuedocode...nope
    um = np.mean(pic)
    us = np.std(pic)

    # I think um and us are per-pic values in the psuedocode...nope
    # um = np.mean(pic, axis=itr_axes).reshape(shape)
    # us = np.std(pic, axis=itr_axes).reshape(shape)

    # Per-pic mean and  std
    m = np.mean(pic, axis=mat_axes).reshape(shape)
    s = np.std(pic, axis=mat_axes).reshape(shape)
    # Normalize each pic
    # return (pic - m) * us / s + um
    return um + (pic - m) * us / s


def norm_vecs(mat):
    # Get normalization value: length of the n-dimensional eigenvector
    # linalg.norm assumes the entire matrix is one dataset, so we need to tell it the axes that represent datasets
    mat_rss = rss(mat)

    # Normalize the matrix: divide by
    return mat / mat_rss

def rss(mat):
    n = np.ndim(mat) - 1
    # Some matrix ops need to be told to operate on a list of matrices
    # Assume the data stored in matrices, not arrays
    # So the last two dimensions define the matrix
    axes = tuple(np.arange(np.ndim(mat))[-n:])

    # Use this to reshape mean and std so regular math operators cast correctly
    shape = np.shape(mat)[:-2] + (1, 1)
    return np.linalg.norm(mat, axis=axes).reshape(shape)


def transpose_pic(pic):
    axes = np.arange(np.ndim(pic))
    # Regular numpy transpose does not broadcast properly, but swapaxes does the right thing
    return np.swapaxes(pic, axes[-1], axes[-2])


if __name__ == '__main__':
    # Picture subfolder source options
    source = "att_db"
    source = "instructors"

    pics = get_image_data(source)

    pics_mean = get_mean_pic(pics)

    # M/S are mean and sigma of values for the overall mean pic
    M = np.mean(pics_mean)
    S = np.std(pics_mean)

    # m/s are mean and sigma of each pic
    m = np.mean(pics, axis=(1, 2))
    s = np.std(pics, axis=(1, 2))

    # norm_pics = get_norm_pic(pics)
    # Normalize by just subtracting the mean
    norm_pics = np.asarray([(pics[i] - m[i]) * S / s[i] + M for i in range(len(pics))])

    # Flatten so we can make covariance matrix
    A = np.asmatrix([a.flatten() for a in norm_pics])
    L = A * A.T

    # Looks like the eigenvectors come back normalized already
    (eigvals, eigvecs) = np.linalg.eig(L)

    # Sort values/vectors here, drop if eigenvalue is zero

    # Keeps the 4 largest eigenvalues
    # keep = np.argsort(eigvals)[-1:-5:-1]  # Last 4 indices, reversed
    # eigvals = eigvals[keep]
    # eigvecs = np.asarray([e[0, keep] for e in eigvecs])

    X = A.T * eigvecs
    Y = X / np.sqrt(eigvals)
    C = np.array([y.reshape((300,300)) for y in Y.T])



