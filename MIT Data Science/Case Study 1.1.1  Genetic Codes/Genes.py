import scipy as sp
import sklearn as skl
import sklearn.decomposition
import sklearn.preprocessing
import numpy as np
import pandas as pd
import pathlib
import os
import matplotlib
import matplotlib.mlab
import matplotlib.pyplot as plt

def LoadSeq():
    file = 'ccrescentus.fa'
    # Search the current folder tree for the file
    folder = pathlib.Path(os.curdir)
    files = folder.rglob(file)
    for file in files:
        with open(file) as f:
            lines = [line.rstrip() for line in f]

        return "".join(lines[1:])

def CalcFreq(s, chars):
    rows = len(s)//300
    cols = 4**chars


    names = dict()
    data = np.zeros(shape=(rows, cols), dtype=np.int)
    # print(result)

    for r in range(rows):
        chunk = s[r*300:(r+1)*300]
        # print(chunk)
        d = {}
        # Split 300-character chunk into words of length(chars)
        for i in range(0, len(chunk), chars):
            # Each Word w has chars characters
            w = chunk[i:i+chars]
            # Count the frequency of each word in the chunk
            d[w] = d.get(w, 0) + 1
            # print(w, d[w])

        for i, k in enumerate(sorted(d)):
            # See if this codon has been seen already
            if k not in names:
                names[k] = len(names)

            col = names[k]  # Get column number assigned to this codon

            # print(i, k, d[k])
            data[r, col] = d[k]
            # print(result)

        # order = np.argsort(names.keys())

        # print(d)
        # print(result)

    return np.asmatrix(data)

def Standardize(m):
    return (m - np.mean(m, axis=0)) / np.std(m, axis=0)

def myPCA(x):

    if False:
        pca = sklearn.decomposition.PCA()
        x_std = sklearn.preprocessing.StandardScaler().fit_transform(x)
        x_pca = pca.fit_transform(x_std)

    mpca = matplotlib.mlab.PCA(x)

    x = np.array(mpca.Y[:, 0]).flatten()
    y = np.array(mpca.Y[:, 1]).flatten()

    plt.scatter(x, y)
    plt.show()


