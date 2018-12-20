# Dataset Source:
# https://www.geeksforgeeks.org/analysis-of-test-data-using-k-means-clustering-in-python/

# importing required tools
import numpy as np
from matplotlib import pyplot as plt

def make_data():
    # creating two test data
    x = np.random.randint(10, 35, (25, 2))
    y = np.random.randint(55, 70, (25, 2))
    z = np.vstack((x, y))
    z = z.reshape((50, 2))

    # convert to np.float32
    z = np.float32(z)
    return z

# Simple implementation of k-means algorithm
# Using sample dataset and only two clusters
def run():
    z = make_data()

    x = z[:,0]
    y = z[:,1]

    xm = np.mean(x)
    xs = np.std(x)
    ym = np.mean(y)
    ys = np.std(y)

    # These are really bad guesses for the x,y coordinates of each cluster center
    #   just to show that it still will converge
    # Note that even when guessing that both clusters have the same center, the algo converges
    x0i = 0
    y0i = 0
    x1i = 0
    y1i = 0

    x0 = x0i
    y0 = y0i
    x1 = x1i
    y1 = y1i

    # init distances
    d = np.inf
    lenz = range(len(z))
    iter = 0

    while True:
        # iteration counter, just to watch how quickly the algo converges
        iter += 1

        # Init lists of zeros to store distance to each cluster for each point
        d0s = [0]*len(z)
        d1s = [0]*len(z)

        # Iterate on each point, and calculate the distance to each cluster's current center
        for i, p in enumerate(z):
            d0s[i] = np.sum(np.square([p[0] - x0, p[1] - y0]))
            d1s[i] = np.sum(np.square([p[0] - x1, p[1] - y1]))

        # Use the calculated distances to re-assign each point to a cluster
        g0_flag = [d0s[i] < d1s[i] for i in lenz]

        # If any point is assigned to cluster zero, then calculate total distance for the current cluster point
        # AND calculate a new cluster center to evaluate
        if any(g0_flag):
            d0 = np.sum(d0s[i] for i in lenz if g0_flag[i])
            x0 = np.mean([z[i, 0] for i in lenz if g0_flag[i]])
            y0 = np.mean([z[i, 1] for i in lenz if g0_flag[i]])
        else:
            # If no points are in cluster zero, then total distance is zero
            # AND there is no data to justify a new cluster center
            d0 = 0

        # If any point is assigned to cluster one, then calculate total distance for the current cluster point
        # AND calculate a new cluster center to evaluate
        if not all(g0_flag):
            d1 = np.sum(d1s[i] for i in lenz if not g0_flag[i])
            x1 = np.mean([z[i, 0] for i in lenz if not g0_flag[i]])
            y1 = np.mean([z[i, 1] for i in lenz if not g0_flag[i]])
        else:
            # If no points are in cluster one, then total distance is zero
            # AND there is no data to justify a new cluster center
            d1 = 0

        # Report on progress
        print(iter, d0, d1, d, abs(d0 + d1 - d))

        # If the current distance score is close enough to the previous one, then we can stop seraching
        if abs(d0 + d1 - d) < .005:
            d = d0 + d1
            break

        # Show the new cluster guesses
        print(x0, y0)
        print(x1, y1)

        # Score the previous cluster centers before evaluating the new guess
        d = d0 + d1
        print(iter, d)


    # Plot all the sample data points
    plt.xlabel('Test Data')
    plt.ylabel('Z samples')
    plt.scatter(x, y, c='b')

    # Plot the final cluster centers
    plt.scatter(x0, y0, c='r')
    plt.scatter(x1, y1, c='g')

    # Plot the initial cluster centers
    plt.scatter(x0i, y0i, c='r', marker='+')
    plt.scatter(x1i, y1i, c='g', marker='+')

    plt.show()

run()