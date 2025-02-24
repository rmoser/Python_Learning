import numpy as np
import logging
Log = logging.getLogger(__name__)
# Log =  logging.StreamHandler()
# Log.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def perceptron(X, Y, start=0, use_bias=False, theta=None, theta_0=None):
    if theta is None:
        theta = np.zeros(shape=np.array([0, 1]) + X[0].shape).T
    if theta_0 is None:
        theta_0 = 0.

    n = len(X)
    errs = 0
    thetas = []
    theta_0s = []
    # 10 epochs good enough to start
    consecutive_successes = 0
    for epoch in range(10):
        for i in range(n):
            _i = (start + i) % n
            x = X[_i]
            if use_bias:
                x = np.append(x, 1.).T
            x = x.T
            y = Y[_i]
            e = y * (theta.dot(x) + theta_0)
            logging.info(f'epoch: {epoch} i:{_i} => {y} * {theta} · {x}: {e} => {"ERR" if e <= 0 else "PASS"}')
            if e <= 0:
                theta += y*x
                errs += 1
                consecutive_successes = 0
                thetas.append(theta[:-1].tolist())
                if use_bias:
                    theta_0s.append(theta[-1])
                #     theta_0 += y
                #     theta_0s.append(theta_0)
            else:
                consecutive_successes += 1
            logging.info(f'successes: {consecutive_successes} vs. n {n}')
            if consecutive_successes >= n:
                logging.info('Learned!')
                break
        else:
            continue
        break
    if epoch >= 9:
        logging.warning('')
        logging.warning(' Expired!')
        logging.warning('')
    return theta[:-1], theta[-1], errs, thetas

if __name__ == '__main__':
    # X = np.array([[-1, -1], [1, 0], [-1, 1.5]])
    # Y = np.array([1, -1, 1])
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    Y = [0, 0, 0, 1]
    # X = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    # Y = [0,0,0,0,0,0,0,1]
    # X = [[0,0], [0,1], [1,0], [1,1]]
    # Y = [0,0,0,1]
    X = np.array(X)
    # X = X + 1
    Y = np.array(Y)
    Y = -1 + 2 * Y
    theta, theta_0, errs, thetas = perceptron(X, Y, use_bias=True)
    # theta, theta_0, errs, thetas = perceptron(X, Y, use_bias=True, start=-1, theta=np.array([0.7] * len(X[0])), theta_0 = -2)
    print('\nResult of Perceptron algorithm on:')
    print(f'X: {X}')
    print(f'Y: {Y}')
    print('='*60)
    print(f'theta: {theta}')
    print(f'theta_0: {theta_0}')
    print(f'err_count: {errs}')
    print(f'theta progression: {thetas}')

