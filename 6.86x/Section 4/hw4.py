import numpy as np
import scipy.stats

pdf = scipy.stats.norm.pdf

x = np.array([[-1, 0, 4, 5, 6]])

p = np.array([0.5, 0.5])
mu = np.array([6, 7])
var = np.array([1, 4])

theta = np.array([0.5, 0.5, 6, 7, 1, 4])

L = p * pdf(x.T, mu, var**0.5)

e = np.argmax(L, axis=1)

mu = np.array([x[0][np.where(e==0)].mean(), x[0][np.where(e==1)].mean()])

var = np.array([((x[0][np.where(e==0)] - mu[0])**2).mean(), ((x[0][np.where(e==1)] - mu[1])**2).mean()])
p = np.array([1-e.mean(), e.mean()])

ll = []
for y in range(len(p)):
