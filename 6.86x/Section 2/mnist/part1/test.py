import os
import sys
import time
import traceback
import numpy as np
import linear_regression
import svm
import softmax
import features
import kernel
import pytest

sys.path.append("..")
import utils

verbose = False

epsilon = 1e-6

def green(s):
    return '\033[1;32m%s\033[m' % s

def yellow(s):
    return '\033[1;33m%s\033[m' % s

def red(s):
    return '\033[1;31m%s\033[m' % s

def log(*m):
    print(" ".join(map(str, m)))

def log_exit(*m):
    log(red("ERROR:"), *m)
    exit(1)


def check_real(ex_name, f, exp_res, *args):
    try:
        res = f(*args)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return True
    if not np.isreal(res):
        log(red("FAIL"), ex_name, ": does not return a real number, type: ", type(res))
        return True
    if not -epsilon < res - exp_res < epsilon:
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return True


def equals(x, y):
    if type(y) == np.ndarray:
        return (np.abs(x - y) < epsilon).all()
    return -epsilon < x - y < epsilon

def check_tuple(ex_name, f, exp_res, *args, **kwargs):
    try:
        res = f(*args, **kwargs)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return True
    if not type(res) == tuple:
        log(red("FAIL"), ex_name, ": does not return a tuple, type: ", type(res))
        return True
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected a tuple of size ", len(exp_res), " but got tuple of size", len(res))
        return True
    if not all(equals(x, y) for x, y in zip(res, exp_res)):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return True

def check_array(ex_name, f, exp_res, *args):
    try:
        res = f(*args)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return True
    if not type(res) == np.ndarray:
        log(red("FAIL"), ex_name, ": does not return a numpy array, type: ", type(res))
        return True
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected an array of shape ", exp_res.shape, " but got array of shape", res.shape)
        return True
    if not equals(res, exp_res):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)

        return True

def check_list(ex_name, f, exp_res, *args):
    try:
        res = f(*args)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return True
    if not type(res) == list:
        log(red("FAIL"), ex_name, ": does not return a list, type: ", type(res))
        return True
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected a list of size ", len(exp_res), " but got list of size", len(res))
        return True
    if not all(equals(x, y) for x, y in zip(res, exp_res)):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return True

def test_get_mnist():
    ex_name = "Get MNIST data"
    try:
        train_x, train_y, test_x, test_y = utils.get_MNIST_data()
    except:
        return False
    log(green("PASS"), ex_name, "")
    return True

def test_closed_form():
    ex_name = "Closed form"
    X = np.arange(1, 16).reshape(3, 5)
    Y = np.arange(1, 4)
    lambda_factor = 0.5
    exp_res = np.array([-0.03411225,  0.00320187,  0.04051599,  0.07783012,  0.11514424])
    if check_array(
            ex_name, linear_regression.closed_form,
            exp_res, X, Y, lambda_factor):
        return False
    
    log(green("PASS"), ex_name, "")
    return True

def test_svm():
    ex_name = "One vs rest SVM"
    n, m, d = 5, 3, 7
    train_x = np.random.random((n, d))
    test_x = train_x[:m]
    train_y = np.zeros(n)
    train_y[-1] = 1
    exp_res = np.zeros(m)

    if check_array(
            ex_name, svm.one_vs_rest_svm,
            exp_res, train_x, train_y, test_x):
        return False

    train_y = np.ones(n)
    train_y[-1] = 0
    exp_res = np.ones(m)

    if check_array(
            ex_name, svm.one_vs_rest_svm,
            exp_res, train_x, train_y, test_x):
        return False

    log(green("PASS"), ex_name, "")
    return True

def test_multiclass_svm():
    ex_name = "Multiclass SVM"
    n, m, d = 5, 3, 7
    train_x = np.array([[0.29087021, 0.1649736 ],
         [0.45068798, 0.40304487],
         [0.53760048, 0.57655876],
         [0.28993813, 0.16875203],
         [0.3980612,  0.86839299],
         [0.7490192,  0.63884393],
         [0.0431254,  0.15980304],
         [0.03386161, 0.38220864],
         [0.9052881,  0.25358574],
         [0.12967331, 0.90296403],
         [0.56721915, 0.15687449],
         [0.60600038, 0.68375902],
         [0.92566856, 0.09316889],
         [0.65841199, 0.97523585],
         [0.63912303, 0.06522407],
         [0.35148469, 0.11085943],
         [0.62008728, 0.15500833],
         [0.295813,   0.7433626 ],
         [0.58372923, 0.9989265 ]])

    test_x = np.array([[0.52183717, 0.84654142],
         [0.65560648, 0.90323288],
         [0.47521366, 0.87920547],
         [0.85568627, 0.70372036],
         [0.64518017, 0.53015849],
         [0.04387028, 0.64394258],
         [0.21739479, 0.69990023],
         [0.52183753, 0.97196831],
         [0.76143541, 0.43401942],
         [0.84397804, 0.1109593 ],
         [0.92796873, 0.40050702],
         [0.81709363, 0.76002849]])

    train_y = np.array(list(map(float, '6 5 7 2 5 7 3 7 4 0 4 4 1 3 6 3 5 3 8'.split())))
    exp_res = np.array(list(map(float, '3 3 3 4 3 3 3 3 4 4 4 3'.split())))

    if check_array(
            ex_name, svm.multi_class_svm,
            exp_res, train_x, train_y, test_x):
        return False

    # train_y = np.ones(n)
    # train_y[-1] = 0
    # exp_res = np.ones(m)
    #
    # if check_array(
    #         ex_name, svm.multi_class_svm,
    #         exp_res, train_x, train_y, test_x):
    #     return

    log(green("PASS"), ex_name, "")
    return True

def test_compute_probabilities():
    ex_name = "Compute probabilities"
    n, d, k = 3, 5, 7
    X = np.arange(0, n * d).reshape(n, d)
    zeros = np.zeros((k, d))
    temp = 0.2
    exp_res = np.ones((k, n)) / k
    if check_array(
            ex_name, softmax.compute_probabilities,
            exp_res, X, zeros, temp):
        return False

    theta = np.arange(0, k * d).reshape(k, d)
    softmax.compute_probabilities(X, theta, temp)
    exp_res = np.zeros((k, n))
    exp_res[-1] = 1
    if check_array(
            ex_name, softmax.compute_probabilities,
            exp_res, X, theta, temp):
        return False

    log(green("PASS"), ex_name, "")
    return True


def test_compute_cost_function_0():
    ex_name = "Compute cost function"
    n, d, k = 3, 5, 7
    X = np.arange(0, n * d).reshape(n, d)
    Y = np.arange(0, n)
    zeros = np.zeros((k, d))
    temp = 0.2
    lambda_factor = 0.5
    exp_res = 1.9459101490553135
    if check_real(
            ex_name, softmax.compute_cost_function,
            exp_res, X, Y, zeros, lambda_factor, temp):
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_compute_cost_function_1():
    ex_name = "Compute cost function 1"
    X = np.array([
        [ 1.,  9., 74., 62., 66., 51., 25., 30., 54., 53., 29.],
        [ 1., 42., 55., 17., 39., 47., 29., 46., 68., 94., 19.],
        [ 1., 46., 30., 58., 35., 93., 36., 41., 60., 53., 17.],
        [ 1., 93., 77., 57., 49., 15., 81., 67., 54., 46., 87.],
        [ 1., 15., 97., 39., 45.,  6., 88., 21., 32., 54., 16.],
        [ 1., 17., 93., 81.,  3., 76., 87., 26., 23., 39., 97.],
        [ 1., 87., 55., 24., 32., 68., 89., 31., 97., 69., 51.],
        [ 1., 76., 89., 25.,  1., 38., 70., 52., 71., 45., 85.],
        [ 1., 15., 73., 41.,  8., 43., 36., 78., 25., 38., 49.],
        [ 1.,  4., 17., 43., 34., 96., 39., 99., 79.,  6., 93.]
    ])

    theta = np.array([
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [0.27, 10.908, 17.82, 12.069, 8.424, 14.391, 15.66, 13.257, 15.201, 13.419, 14.661],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629],
        [-0.03, -1.212, -1.98, -1.341, -0.936, -1.599, -1.74, -1.473, -1.689, -1.491, -1.629]
    ])

    Y = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    temp = 1.0
    lambda_factor = 0.0001
    exp_res = 0.105967
    if check_real(
            ex_name, softmax.compute_cost_function,
            exp_res, X, Y, theta, lambda_factor, temp):
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_run_gradient_descent_iteration():
    ex_name = "Run gradient descent iteration"
    n, d, k = 3, 5, 7
    X = np.arange(0, n * d).reshape(n, d)
    Y = np.arange(0, n)
    zeros = np.zeros((k, d))
    alpha = 2
    temp = 0.2
    lambda_factor = 0.5
    exp_res = np.zeros((k, d))
    exp_res = np.array([
       [ -7.14285714,  -5.23809524,  -3.33333333,  -1.42857143, 0.47619048],
       [  9.52380952,  11.42857143,  13.33333333,  15.23809524, 17.14285714],
       [ 26.19047619,  28.0952381 ,  30.        ,  31.9047619 , 33.80952381],
       [ -7.14285714,  -8.57142857, -10.        , -11.42857143, -12.85714286],
       [ -7.14285714,  -8.57142857, -10.        , -11.42857143, -12.85714286],
       [ -7.14285714,  -8.57142857, -10.        , -11.42857143, -12.85714286],
       [ -7.14285714,  -8.57142857, -10.        , -11.42857143, -12.85714286]
    ])

    if check_array(
            ex_name, softmax.run_gradient_descent_iteration,
            exp_res, X, Y, zeros, alpha, lambda_factor, temp):
        return False
    softmax.run_gradient_descent_iteration(X, Y, zeros, alpha, lambda_factor, temp)
    log(green("PASS"), ex_name, "")
    return True


def test_update_y():
    ex_name = "Update y"
    train_y = np.arange(0, 10)
    test_y = np.arange(9, -1, -1)
    exp_res = (
            np.array([0, 1, 2, 0, 1, 2, 0, 1, 2, 0]),
            np.array([0, 2, 1, 0, 2, 1, 0, 2, 1, 0])
            )
    if check_tuple(
            ex_name, softmax.update_y,
            exp_res, train_y, test_y):
        return False

    log(green("PASS"), ex_name, "")
    return True

###Correction note:  check_project_onto_PC fucntion have been modified since release.
def test_project_onto_PC():
    ex_name = "Project onto PC"
    X = np.array([
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9],
        [4, 8, 12],
    ])
    x_centered, feature_means = features.center_data(X)
    pcs = features.principal_components(x_centered)
    exp_res = -1 * np.array([
        [-5.61248608, 0],
        [-1.87082869, 0],
        [1.87082869, 0],
        [5.61248608, 0],
    ])
    n_components = 2
    if check_array(
            ex_name, features.project_onto_PC,
            exp_res, X, pcs, n_components, feature_means):
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_polynomial_kernel():
    ex_name = "Polynomial kernel"
    n, m, d = 3, 5, 7
    c = 1
    p = 2
    X = np.random.random((n, d))
    Y = np.random.random((m, d))
    try:
        K = kernel.polynomial_kernel(X, Y, c, d)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False
    flag = True
    for i in range(n):
        for j in range(m):
            exp = (X[i] @ Y[j] + c) ** d
            got = K[i][j]
            if (not equals(exp, got)):
                log(
                    red("FAIL"), ex_name,
                    ": values at ({}, {}) do not match. Expected {}, got {}"
                    .format(i, j, exp, got)
                )
                flag = False
    if not flag:
        return False
    log(green("PASS"), ex_name, "")
    return True

def test_rbf_kernel():
    ex_name = "RBF kernel"
    n, m, d = 3, 5, 7
    gamma = 0.5
    X = np.random.random((n, d))
    Y = np.random.random((m, d))
    try:
        K = kernel.rbf_kernel(X, Y, gamma)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False
    flag = True
    for i in range(n):
        for j in range(m):
            exp = np.exp(-gamma * (np.linalg.norm(X[i] - Y[j]) ** 2))
            got = K[i][j]
            if (not equals(exp, got)):
                log(
                    red("FAIL"), ex_name,
                    ": values at ({}, {}) do not match. Expected {}, got {}"
                    .format(i, j, exp, got)
                )
                flag = False
    if not flag:
        return False
    log(green("PASS"), ex_name, "")
    return True

def main():
    log(green("PASS"), "Import mnist project")
    try:
        test_get_mnist()
        test_closed_form()
        test_svm()
        test_multiclass_svm()
        test_compute_probabilities()
        test_compute_cost_function_0()
        test_compute_cost_function_1()
        test_run_gradient_descent_iteration()
        test_update_y()
        test_project_onto_PC()
        test_polynomial_kernel()
        test_rbf_kernel()
    except Exception:
        log_exit(traceback.format_exc())

if __name__ == "__main__":
    main()
