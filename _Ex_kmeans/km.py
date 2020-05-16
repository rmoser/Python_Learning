import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def make_data(rows=1000, k=3):
    df = pd.DataFrame()
    for i in range(k):
        # df[f'nx{i}'] = np.zeros(shape=rows)
        df[f'nx{i}'] = np.random.normal(size=rows)

        df[f'ny{i}'] = np.random.normal(size=rows)

        df[f'x{i}'] = np.random.randint(-10, 10) + df[f'nx{i}'] * np.random.randint(1, 2)
        df[f'y{i}'] = np.random.randint(-10, 10) + df[f'ny{i}'] * np.random.randint(1, 2)

    dfx = pd.DataFrame()

    df['m'] = np.random.choice(range(k), size=rows)
    df['x'] = df.lookup(df.index, [f'x{m}' for m in df.m])
    df['y'] = df.lookup(df.index, [f'y{m}' for m in df.m])

    if False:
        for i in df.index:
            m = df.m.iloc[i]
            x = df[f'x{m}'].iloc[i]
            y = df[f'y{m}'].iloc[i]
            df['x'].iloc[i] = x
            df['y'].iloc[i] = y

    return df

def errfunc(df, m):
    return np.sum(np.square((df.x - m[df.m, 0], df.y - m[df.m, 1])))


def km(df, k=3, iters=100):
    np.random.seed()
    means = []
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

def kmedioids(df, k=3, iters=100):
    np.random.seed()
    meds = []
#    means.append(df[['x', 'y']][:k].values)  # Use first 3 points as centers
    meds.append(df[['x', 'y']].sample(k).values)  # Use random k points as centers
    errs = []
    err = errfunc(df, meds[0])
    errs.append(err)

    for itr in range(iters):

        dft = df[['x', 'y', 'm']].copy()
        ms = meds[itr]  # k * 2 matrix
        # print(ms)
        dx = df.x.values.reshape(len(df.x), 1)
        dy = df.y.values.reshape(len(df.y), 1)  # Convert to vertical matrix

        ds = np.sum(np.square((dx - ms[:, 0], dy - ms[:, 1])), axis=0)
        dft.m = [np.argsort(m)[0] for m in ds]

        for i in range(k):
            ms[i, 0] = np.median(dft.x[dft.m == i])
            ms[i, 1] = np.median(dft.y[dft.m == i])

        meds.append(ms)

        err = errfunc(dft, ms)
        errs.append(err)

        # print(f"iter {itr+1}: err {err}")

        if abs(err - errs[itr]) < 0.001:
            break

    return err, meds, dft


def plotit(df):
    ks = df.m.unique()
    for k in ks:
        dfs = df[df.m == k]
        plt.scatter(dfs.x, dfs.y)
        plt.scatter(np.median(dfs.x), np.median(dfs.y))

    plt.show()


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
