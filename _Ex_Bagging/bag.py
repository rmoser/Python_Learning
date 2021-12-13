import numpy as np
import pandas as pd


def gen_data(n):
    df = pd.DataFrame()

    centers = ((0, 0), (np.random.randint(1, 5, dtype=np.int), np.random.randint(1, 5, dtype=np.int)))

    df['c'] = np.random.randint(0, 2, n, dtype=np.int)
    df['X'] = np.zeros(n, dtype=np.int)
    df['Y'] = np.zeros(n, dtype=np.int)
    for r, s in df.iterrows():
        s['X'] = centers[int(s['c'])][0]
        s['Y'] = centers[int(s['c'])][1]

    df['x'] = df['X'] + np.random.normal(size=n)
    df['y'] = df['Y'] + np.random.normal(size=n)

    return df


def oned(df):
    x = df[['x', 'c']].sort_values(by='x')
    for r, s in x.iterrows():
        pass



