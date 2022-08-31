import numpy as np
import pandas as pd
import scipy as sp
from matplotlib import pyplot as plt

from scipy.stats import probplot

df = pd.DataFrame()
# Synthesize 'x' variable, as random normal with mean 10 and std dev 0.5:
df['x'] = np.random.normal(loc=10, scale=0.5, size=10000)

quantiles = probplot(df.x)

# Grab paired data for x variable and its calculated quantile
dfq = pd.DataFrame({'q': quantiles[0][0], 'x': quantiles[0][1]})  # Quantiles, aka Z-scores
dfq['p'] = sp.stats.norm.cdf(dfq.q) # Probabilities
dfq['fit'] = (dfq.x - quantiles[1][1]) / quantiles[1][0]  # Fit line

# plot
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax3 = ax1

ax1.plot(dfq.x, dfq.q, 'b-')
ax1.set_xlabel('x data')
ax1.set_ylabel('Quantile aka Z-score', color='b')

ax2.plot(dfq.x, dfq.p, 'r-')
ax2.set_ylabel('Probability', color='r')

ax3.plot(dfq.x, dfq.fit, 'b', linestyle='dotted')
plt.show()
