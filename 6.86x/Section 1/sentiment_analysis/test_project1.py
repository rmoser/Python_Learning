import os
import sys
import time
import traceback

from winnt import TRANSACTIONMANAGER_QUERY_INFORMATION

import project1 as p1
import numpy as np
import pytest

verbose = False

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
        return False
    if not np.isreal(res):
        log(red("FAIL"), ex_name, ": does not return a real number, type: ", type(res))
        return False
    if res != pytest.approx(exp_res):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return False
    return True


def equals(x, y):
    if type(y) == np.ndarray or type(x) == np.ndarray:
        return (x == pytest.approx(y)).all()
    return x == pytest.approx(y)

def check_tuple(ex_name, f, exp_res, *args, **kwargs):
    try:
        res = f(*args, **kwargs)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False
    if not type(res) == tuple:
        log(red("FAIL"), ex_name, ": does not return a tuple, type: ", type(res))
        return False
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected a tuple of size ", len(exp_res), " but got tuple of size", len(res))
        return False
    if not all(equals(x, y) for x, y in zip(res, exp_res)):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return False
    return True

def check_array(ex_name, f, exp_res, *args):
    try:
        res = f(*args)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False
    if not type(res) == np.ndarray:
        log(red("FAIL"), ex_name, ": does not return a numpy array, type: ", type(res))
        return False
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected an array of shape ", exp_res.shape, " but got array of shape", res.shape)
        return False
    if not all(equals(x, y) for x, y in zip(res, exp_res)):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return False
    return True

def check_list(ex_name, f, exp_res, *args):
    try:
        res = f(*args)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False
    if not type(res) == list:
        log(red("FAIL"), ex_name, ": does not return a list, type: ", type(res))
        return False
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected a list of size ", len(exp_res), " but got list of size", len(res))
        return False
    if not all(equals(x, y) for x, y in zip(res, exp_res)):
        log(red("FAIL"), ex_name, ": incorrect answer. Expected", exp_res, ", got: ", res)
        return False
    return True


def test_get_order_00():
    ex_name = "Get order 00"
    if not check_list(
            ex_name, p1.get_order,
            [0], 1):
        log("You should revert `get_order` to its original implementation for this test to pass")
        return False
    if not check_list(
            ex_name, p1.get_order,
            [1, 0], 2):
        log("You should revert `get_order` to its original implementation for this test to pass")
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_hinge_loss_single_00():
    ex_name = "Hinge loss single 00"

    feature_vector = np.array([1, 2])
    label, theta, theta_0 = 1, np.array([-1, 1]), -0.2
    exp_res = 1 - 0.8
    if not check_real(
            ex_name, p1.hinge_loss_single,
            exp_res, feature_vector, label, theta, theta_0):
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_hinge_loss_single_01():
    ex_name = "Hinge loss single 01"

    feature_vector = np.array([0.13018489, 0.45342815, 0.47727826, 0.47838207, 0.24782531, 0.95400403, 0.60135646, 0.21863698 ,0.50490517, 0.22274132])
    label = -1
    theta = np.array([0.38406916, 0.11027105, 0.10476069, 0.10451897, 0.20175502, 0.05241068, 0.08314536, 0.22868958, 0.0990285,  0.22447564])
    theta_0 = 0.5
    exp_res = 2.
    if not check_real(
            ex_name, p1.hinge_loss_single,
            exp_res, feature_vector, label, theta, theta_0):
        return False
    log(green("PASS"), ex_name, "")
    return True


def test_hinge_loss_full_00():
    ex_name = "Hinge loss full 00"

    feature_vector = np.array([[1, 2], [1, 2]])
    label, theta, theta_0 = np.array([1, 1]), np.array([-1, 1]), -0.2
    exp_res = 1 - 0.8
    if not check_real(
            ex_name, p1.hinge_loss_full,
            exp_res, feature_vector, label, theta, theta_0):
        return False

    log(green("PASS"), ex_name, "")
    return True


def test_perceptron_single_update_00():
    ex_name = "Perceptron single update 00"

    feature_vector = np.array([1, 2])
    label, theta, theta_0 = 1, np.array([-1, 1]), -1.5
    exp_res = (np.array([0, 3]), -0.5)
    if not check_tuple(
            ex_name, p1.perceptron_single_step_update,
            exp_res, feature_vector, label, theta, theta_0):
        return False

    feature_vector = np.array([1, 2])
    label, theta, theta_0 = 1, np.array([-1, 1]), -1
    exp_res = (np.array([0, 3]), 0)
    if not check_tuple(
            ex_name + " (boundary case)", p1.perceptron_single_step_update,
            exp_res, feature_vector, label, theta, theta_0):
        return False

    log(green("PASS"), ex_name, "")
    return True


def test_perceptron_00():
    ex_name = "Perceptron 00"

    feature_matrix = np.array([[1, 2]])
    labels = np.array([1])
    T = 1
    exp_res = (np.array([1, 2]), 1)
    if not check_tuple(
            ex_name, p1.perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2], [-1, 0]])
    labels = np.array([1, 1])
    T = 1
    exp_res = (np.array([0, 2]), 2)
    if not check_tuple(
            ex_name, p1.perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2]])
    labels = np.array([1])
    T = 2
    exp_res = (np.array([1, 2]), 1)
    if not check_tuple(
            ex_name, p1.perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2], [-1, 0]])
    labels = np.array([1, 1])
    T = 2
    exp_res = (np.array([0, 2]), 2)
    if not check_tuple(
            ex_name, p1.perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    log(green("PASS"), ex_name, "")
    return True


def test_average_perceptron_00():
    ex_name = "Average perceptron 00"

    feature_matrix = np.array([[1, 2]])
    labels = np.array([1])
    T = 1
    exp_res = (np.array([1, 2]), 1)
    if not check_tuple(
            ex_name, p1.average_perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2], [-1, 0]])
    labels = np.array([1, 1])
    T = 1
    exp_res = (np.array([-0.5, 1]), 1.5)
    if not check_tuple(
            ex_name, p1.average_perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2]])
    labels = np.array([1])
    T = 2
    exp_res = (np.array([1, 2]), 1)
    if not check_tuple(
            ex_name, p1.average_perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    feature_matrix = np.array([[1, 2], [-1, 0]])
    labels = np.array([1, 1])
    T = 2
    exp_res = (np.array([-0.25, 1.5]), 1.75)
    if not check_tuple(
            ex_name, p1.average_perceptron,
            exp_res, feature_matrix, labels, T):
        return False

    log(green("PASS"), ex_name, "")
    return True

def test_pegasos_single_step_update_00():
    ex_name = "Pegasos single step update 00"

    feature_vector = np.array([1, 2])
    label, theta, theta_0 = 1, np.array([-1, 1]), -1.5
    L = 0.2
    eta = 0.1
    exp_res = (np.array([-0.88, 1.18]), -1.4)
    if not check_tuple(
            ex_name, p1.pegasos_single_step_update,
            exp_res,
            feature_vector, label, L, eta, theta, theta_0):
        return False

    feature_vector = np.array([1, 1])
    label, theta, theta_0 = 1, np.array([-1, 1]), 1
    L = 0.2
    eta = 0.1
    exp_res = (np.array([-0.88, 1.08]), 1.1)
    if not check_tuple(
            ex_name +  " (boundary case)", p1.pegasos_single_step_update,
            exp_res,
            feature_vector, label, L, eta, theta, theta_0):
        return False

    feature_vector = np.array([1, 2])
    label, theta, theta_0 = 1, np.array([-1, 1]), -2
    L = 0.2
    eta = 0.1
    exp_res = (np.array([-0.88, 1.18]), -1.9)
    if not check_tuple(
            ex_name, p1.pegasos_single_step_update,
            exp_res,
            feature_vector, label, L, eta, theta, theta_0):
        return False

    log(green("PASS"), ex_name, "")


def test_pegasos_00():
    ex_name = "Pegasos 00"

    feature_matrix = np.array([[1, 2]])
    labels = np.array([1])
    T = 1
    L = 0.2
    exp_res = (np.array([1, 2]), 1)
    if not check_tuple(
            ex_name, p1.pegasos,
            exp_res, feature_matrix, labels, T, L):
        return False

    feature_matrix = np.array([[1, 1], [1, 1]])
    labels = np.array([1, 1])
    T = 1
    L = 1
    exp_res = (np.array([1-1/np.sqrt(2), 1-1/np.sqrt(2)]), 1)
    if not check_tuple(
            ex_name, p1.pegasos,
            exp_res, feature_matrix, labels, T, L):
        return False

    log(green("PASS"), ex_name, "")
    return True

def test_classify_00():
    ex_name = "Classify 00"

    feature_matrix = np.array([[1, 1], [1, 1], [1, 1]])
    theta = np.array([1, 1])
    theta_0 = 0
    exp_res = np.array([1, 1, 1])
    if not check_array(
            ex_name, p1.classify,
            exp_res, feature_matrix, theta, theta_0):
        return False

    feature_matrix = np.array([[-1, 1]])
    theta = np.array([1, 1])
    theta_0 = 0
    exp_res = np.array([-1])
    if not check_array(
            ex_name + " (boundary case)", p1.classify,
            exp_res, feature_matrix, theta, theta_0):
        return False

    log(green("PASS"), ex_name, "")
    return True

def test_classifier_accuracy_00():
    ex_name = "Classifier accuracy 00"

    train_feature_matrix = np.array([[1, 0], [1, -1], [2, 3]])
    val_feature_matrix = np.array([[1, 1], [2, -1]])
    train_labels = np.array([1, -1, 1])
    val_labels = np.array([-1, 1])
    exp_res = 1, 0
    T=1
    if not check_tuple(
            ex_name, p1.classifier_accuracy,
            exp_res,
            p1.perceptron,
            train_feature_matrix, val_feature_matrix,
            train_labels, val_labels,
            T=T):
        return False

    train_feature_matrix = np.array([[1, 0], [1, -1], [2, 3]])
    val_feature_matrix = np.array([[1, 1], [2, -1]])
    train_labels = np.array([1, -1, 1])
    val_labels = np.array([-1, 1])
    exp_res = 1, 0
    T=1
    L=0.2
    if not check_tuple(
            ex_name, p1.classifier_accuracy,
            exp_res,
            p1.pegasos,
            train_feature_matrix, val_feature_matrix,
            train_labels, val_labels,
            T=T, L=L):
        return False

    log(green("PASS"), ex_name, "")
    return True

def test_bag_of_words_00():
    ex_name = "Bag of words 00"

    texts = [
        "He loves to walk on the beach",
        "There is nothing better"]

    try:
        res = p1.bag_of_words(texts)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return False

    if not type(res) == dict:
        log(red("FAIL"), ex_name, ": does not return a tuple, type: ", type(res))
        return False

    vals = sorted(res.values())
    exp_vals = list(range(len(res.keys())))
    if vals != exp_vals:
        log(red("FAIL"), ex_name, ": wrong set of indices. Expected: ", exp_vals, " got ", vals)
        return False


    keys = sorted(res.keys())
    exp_keys = ['beach', 'better', 'he', 'is', 'loves', 'nothing', 'on', 'the', 'there', 'to', 'walk']
    stop_keys = ['beach', 'better', 'loves', 'nothing', 'walk']

    if keys == exp_keys:
        log(yellow("WARN"), ex_name, ": does not remove stopwords:", [k for k in keys if k not in stop_keys])
        return False

    if keys != stop_keys:
        log(red("FAIL"), ex_name, ": keys are missing:", [k for k in stop_keys if k not in keys], " or are not unexpected:", [k for k in keys if k not in stop_keys])
        return False

    log(green("PASS"), ex_name, " stopwords removed")
    return True

def test_extract_bow_feature_vectors_00():
    ex_name = "Extract bow feature vectors 00"
    texts = [
        "He loves her ",
        "He really really loves her"]
    keys = ["he", "loves", "her", "really"]
    dictionary = {k:i for i, k in enumerate(keys)}
    exp_res = np.array(
        [[1, 1, 1, 0],
        [1, 1, 1, 1]])
    non_bin_res = np.array(
        [[1, 1, 1, 0],
        [1, 1, 1, 2]])


    try:
        res = p1.extract_bow_feature_vectors(texts, dictionary)
    except NotImplementedError:
        log(red("FAIL"), ex_name, ": not implemented")
        return

    if not type(res) == np.ndarray:
        log(red("FAIL"), ex_name, ": does not return a numpy array, type: ", type(res))
        return
    if not len(res) == len(exp_res):
        log(red("FAIL"), ex_name, ": expected an array of shape ", exp_res.shape, " but got array of shape", res.shape)
        return

    log(green("PASS"), ex_name)

    if (res == exp_res).all():
        log(yellow("WARN"), ex_name, ": uses binary indicators as features")
    elif (res == non_bin_res).all():
        log(green("PASS"), ex_name, ": correct non binary features")
    else:
        log(red("FAIL"), ex_name, ": unexpected feature matrix")
        return

def main():
    log(green("PASS"), "Import project1")
    try:
        test_get_order_00()
        test_hinge_loss_single_00()
        test_hinge_loss_single_01()
        test_hinge_loss_full_00()
        test_perceptron_single_update_00()
        test_perceptron_00()
        test_average_perceptron_00()
        test_pegasos_single_step_update_00()
        test_pegasos_00()
        test_classify_00()
        test_classifier_accuracy_00()
        test_bag_of_words_00()
        test_extract_bow_feature_vectors_00()
    except Exception:
        log_exit(traceback.format_exc())

if __name__ == "__main__":
    main()
