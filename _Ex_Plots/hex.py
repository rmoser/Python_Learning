# Source
# https://python-graph-gallery.com/84-hexbin-plot-with-matplotlib/

# Colormaps: https://matplotlib.org/tutorials/colors/colormaps.html

# libraries
import matplotlib.pyplot as plt
import numpy as np

# create data
i = 2*np.random.normal(size=50000)
x = i + np.random.normal(size=50000)
y = i + np.random.normal(size=50000)

# cmap = 'Set1'
cmap = 'plasma'
# cmap = None

plt.figure(figsize=(8, 8))
plt.suptitle("Hexbin plots varying gridsize", fontsize=16)
# fig, axs = plt.subplots(3, 3, constrained_layout=True)

G = 5
Gfact = 1.3

for j in range(3):
    for i in range(3):
        k = 1 + i + 3 * j
        plt.subplot(3, 3, k)

        if i == 0 and j == 0:
            plt.title("scatter")
            plt.scatter(x, y, s=0.2, alpha=0.1)

        else:
            # g = 5+int(1.6 ** k)
            g = round(G)
            plt.title(f"gridsize={g}")

            # Make the plot
            plt.hexbin(x, y, gridsize=g, cmap=cmap, edgecolors='black', linewidths=0.2, mincnt=0, bins='log')
        print(f"k: {k}")
        G *= Gfact

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

