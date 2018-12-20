# Source
# https://python-graph-gallery.com/84-hexbin-plot-with-matplotlib/

# libraries
import matplotlib.pyplot as plt
import numpy as np

# create data
i = np.random.normal(size=50000)
x = i + np.random.normal(size=50000)
y = i + np.random.normal(size=50000)

# cmap = 'Set1'
cmap = None

plt.figure(figsize=(8, 8))
if True:
    for i in range(3):
        for j in range(3):
            k = 1 + i + 3 * j
            plt.subplot(3, 3, k)

            g = 5+int(1.6 ** k)
            # Make the plot
            plt.hexbin(x, y, gridsize=g, cmap=cmap, edgecolors='black', linewidths=0.2)

else:
    plt.subplot(3, 3, 1)
    plt.scatter(x, y)

    plt.subplot(3, 3, 2)
    plt.hexbin(x, y)

    plt.subplot(3, 3, 3)
    plt.hexbin(x, y, gridsize=15)

plt.show()

