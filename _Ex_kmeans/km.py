import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def make_data(rows=1000, k=3):
    df = pd.DataFrame()

    means = np.random.randint(-10, 10, size=(k, 2))
    sigmas = np.random.randint(1, 7, size=(k, 2)) / 2
    covs = np.random.uniform(low=-1.0, high=1.0, size=k)

    df['k'] = np.random.choice(range(k), size=rows)
    df['mx'] = means[df.k, 0]
    df['my'] = means[df.k, 1]
    df['sx'] = sigmas[df.k, 0]
    df['sy'] = sigmas[df.k, 1]
    df['cov'] = covs[df.k]

    n = np.random.normal(size=(2, rows))
    df['x'] = means[df.k, 0] + sigmas[df.k, 0] * n[0]
    df['y'] = means[df.k, 1] + sigmas[df.k, 1] * (n[0] * covs[df.k] + n[1] * (1-covs[df.k]))

#    df['y'] = df.lookup(df.index, [f'y{m}' for m in df.m])

    if False:
        for i in df.index:
            m = df.m.iloc[i]
            x = df[f'x{m}'].iloc[i]
            y = df[f'y{m}'].iloc[i]
            df['x'].iloc[i] = x
            df['y'].iloc[i] = y

    return df


def plotit(df):
    ks = df.k.unique()
    for k in ks:
        dfs = df[df.k == k]
        plt.scatter(dfs.x, dfs.y)
        plt.plot(np.median(dfs.x), np.median(dfs.y), marker=f"${k}$", color='b', markersize=14)

    plt.show()


def errfunc(df, m):
    return np.sum(np.square((df.x - m[df.k, 0], df.y - m[df.k, 1])))


def km(df, k=3, iters=100):
    np.random.seed()

    # Initial mean x/y coords
    # clusters = [df[['x', 'y']][:k].values)]  # Use first 3 points as centers
    clusters = [df[['x', 'y']].sample(k).values] # Use random k points as centers

    if 'k' not in df:
        df['k'] = 0

    errs = []
    if k >= df.k.max():
        err = errfunc(df, clusters[0])
    else:
        err = 0

    errs.append(err)

    dft = df[['x', 'y', 'k']].copy()
    for itr in range(iters):

        ms = clusters[itr]  # k * 2 matrix
        # print(ms)
        dx = df.x.values.reshape(len(df.x), 1)
        dy = df.y.values.reshape(len(df.y), 1)  # Convert to vertical matrix

        ds = np.sum(np.square((dx - ms[:, 0], dy - ms[:, 1])), axis=0)
        dft.k = [np.argsort(m)[0] for m in ds]

        for i in range(k):
            ms[i, 0] = np.mean(dft.x[dft.k == i])
            ms[i, 1] = np.mean(dft.y[dft.k == i])

        clusters.append(ms)

        err = errfunc(dft, ms)
        errs.append(err)

        # print(f"iter {itr+1}: err {err}")

        if abs(err - errs[itr]) < 0.001:
            break

    return err, clusters, dft


def kmedioids(df, k=3, iters=100):
    np.random.seed()

    if 'k' not in df:
        df['k'] = 0

    # Initialize clusters
    clusters = [df[['x', 'y']].sample(k).values]  # Use random k points as centers

    if k >= df.k.max():
        err = errfunc(df, clusters[0])
    else:
        err = 0

    errs = [err]

    for itr in range(iters):

        dft = df[['x', 'y', 'k']].copy()
        ms = clusters[itr]  # k * 2 matrix
        # print(ms)
        dx = df.x.values.reshape(len(df.x), 1)
        dy = df.y.values.reshape(len(df.y), 1)  # Convert to vertical matrix

        ds = np.sum(np.square((dx - ms[:, 0], dy - ms[:, 1])), axis=0)
        dft.k = [np.argsort(m)[0] for m in ds]

        for i in range(k):
            ms[i, 0] = np.median(dft.x[dft.k == i])
            ms[i, 1] = np.median(dft.y[dft.k == i])

        clusters.append(ms)

        err = errfunc(dft, ms)
        errs.append(err)

        # print(f"iter {itr+1}: err {err}")

        if abs(err - errs[itr]) < 0.001:
            break

    return err, clusters, dft


def kgnn(df, k=3, iters=100):
    raise NotImplementedError

    np.random.seed()
    means = []
    sigmas = []
    covs = []

    m = df[['x', 'y']].mean()

#    means.append(df[['x', 'y']][:k].values)  # Use first 3 points as centers
    means.append(df[['x', 'y']].sample(k).values)  # Use random k points as centers
    errs = []
    err = errfunc(df, means[0])
    errs.append(err)

    for itr in range(iters):

        dft = df[['x', 'y', 'm']].copy()
        ms = means[itr]  # k * 2 matrix
        # print(ms)
        dx = df.x.values.reshape(len(df.x), 1)
        dy = df.y.values.reshape(len(df.y), 1)  # Convert to vertical matrix

        ds = np.sum(np.square((dx - ms[:, 0], dy - ms[:, 1])), axis=0)
        dft.m = [np.argsort(m)[0] for m in ds]

        for i in range(k):
            ms[i, 0] = np.mean(dft.x[dft.m == i])
            ms[i, 1] = np.mean(dft.y[dft.m == i])

        means.append(ms)

        err = errfunc(dft, ms)
        errs.append(err)

        # print(f"iter {itr+1}: err {err}")

        if abs(err - errs[itr]) < 0.001:
            break

    return err, means, dft


if __name__ == '__main__':
    # f = km
    f = kmedioids
    k = 8
    df = make_data(10000, k)
    runs = {}
    for i in range(10):
        run = f(df, k)
        err = run[0]
        runs[err] = run
        print(f"iter {i}: err {err}")

    minerr = min(runs.keys())
    print(f"Min Error: {minerr}")
    plotit(runs[minerr][2])
