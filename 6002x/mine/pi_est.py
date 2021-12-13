import numpy as np
import matplotlib.pyplot as plt


def pi_est(n):
    # Estimates pi based on the Buffon-Laplace method
    # Synthesizes array of length n, with values representing each iteration of a Monte Carlo sim
    #   of whether uniformly random x/y points land inside the unit circle
    # Value is 0 if random x/y was outside the unit circle
    # Value is 4 if random x/y was inside the unit circle
    # The avg of all values should converge to pi for large n

    batch = 10 ** int(np.log10(n) / 2)
    # print(f"batch: {batch}")

    if n <= 100000:
        # print(f"No Loop")
        x = np.random.uniform(size=n)
        y = np.random.uniform(size=n)
        d = np.sqrt(np.square(x) + np.square(y))
        return 4.0 * np.mean(d < 1.0)

    else:
        # print(f"Loop")
        m = []
        w = []
        while n > batch:
            # print(f"pi_est({n}): batch {batch}")
            m.append(pi_est(batch))
            w.append(batch)
            n -= batch
        else:
            m.append(pi_est(n))
            w.append(n)

        return np.average(m, weights=w)


def pi_cum(n):
    # print(f"No Loop")

    p = [pi_est(1000) for i in range(n)]

    return np.array([np.mean(p[:i+1]) for i in range(len(p))])


def pi_show(n):
    p = pi_cum(n)
    plt.plot(range(n), p)
    plt.plot((0, n), (np.pi, np.pi))
    plt.show()

    print(f"For n: {n} sims of 1k, pi ~= {np.mean(p)}")


def root_2_est(n):
    # Estimates square root of 2 using MC
    # Simulate points on the diagonal of a right triangle with side length 1
    # Proportion of points on the line further than than 1 from a corner is 1/sqrt(2), or half sqrt(2)

    x = np.random.uniform(size=n)
    d = np.sqrt(np.square(x) * 2)
    return 2.0 * np.mean(d <= 1.0)







