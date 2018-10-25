import scipy as sp
import sklearn as skl
import sklearn.decomposition
import sklearn.preprocessing
import numpy as np
import pathlib
import os
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

    result = np.zeros(shape=(rows, cols), dtype=np.int)
    # print(result)

    for r in range(rows):
        chunk = s[r*300:(r+1)*300]
        # print(chunk)
        d = {}
        # Split 300-character chunk into words of length(chars)
        for i in range(0, len(chunk), chars):
            w = chunk[i:i+chars]
            # Count the frequency of each word in the chunk
            d[w] = d.get(w, 0) + 1
            # print(w, d[w])

        for i, k in enumerate(sorted(d)):
            # print(i, k, d[k])
            result[r, i] = d[k]
            # print(result)

        # print(d)
        # print(result)

    return result

def Standardize(m):
    return (m - np.mean(m, axis=0)) / np.std(m, axis=0)

def myPCA(x):
    pca = sklearn.decomposition.PCA(n_components=2)
    x_std = sklearn.preprocessing.StandardScaler().fit_transform(x)
    x_pca = pca.fit_transform(x_std)

    plt.scatter(x_pca.T[0], x_pca.T[1])
    plt.show()

s = LoadSeq()
sd = 'atatatatcgcgcgtgtgacacacacacac' * 10

if False:
    x = CalcFreq(sd, 2)

    #xx = [CalcFreq(s, i+1) for i in range(4)]
    xx = CalcFreq(s, 3)

    # print(xx)
    xxT = x.T
    xxR = np.asarray(x for x in xxT if any(x))
    print(xxR.__repr__())

    # numpy mean of each column
    xs = np.sum(xx)
    # assert xs == [305400, 152700, 101800, 76350]

    xst = Standardize(xx)

    pca = skl.decomposition.PCA(n_components=2)

    xpca = pca.fit_transform(xst)

    plt.scatter(xpca.T[0], xpca.T[1])
    plt.show()

# xc = [np.cov(x) for x in xx]

# xe = [np.linalg.eig(x) for x in xc]

# print(xe)
# a = [xe[i][1].dot(xst[i].T) for i in range(len(xx))]

# print(a)

#print(xx2)
#print(xx3)
#print(xx4)


