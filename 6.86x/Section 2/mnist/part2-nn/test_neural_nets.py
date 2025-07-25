import pytest
import neural_nets as nn
import numpy as np

def test_train_0():
    n = nn.NeuralNetwork()
    n.train_neural_network()
    assert n.test_neural_network()

def test_train_1():
    n = nn.NeuralNetwork()
    # n.training_points = [((-8, -3), -11), ((-9, 3), -6), ((1, -3), -2), ((-10, 4), -6), ((-8, -4), -12), ((1, 8), 9), ((7, -10), -3), ((-3, 5), 2), ((4, -9), -5), ((6, 4), 10)]
    n.training_points = [((-2, 9), 7), ((-10, -4), -14), ((-1, -9), -10), ((-1, 5), 4), ((8, -8), 0), ((2, 5), 7), ((8, -10), -2), ((-5, -9), -14), ((4, -5), -1), ((8, 9), 17)]
    n.learning_rate = 0.002

    atol = 1e-6

    # Epoch 0
    i = 0
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.80041998, 0.63162252], [0.80041998, 0.63162252], [0.80041998, 0.63162252]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.31264518, 0.31264518, 0.31264518]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.07176489], [-0.07176489], [-0.07176489]]), atol=atol)

    # Epoch 1
    i = 1
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.81303142, 0.69183592], [0.81303142, 0.69183592], [0.81303142, 0.69183592]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.45207453, 0.45207453, 0.45207453]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06540675], [-0.06540675], [-0.06540675]]), atol=atol)

    # Epoch 2
    i = 2
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.79853165, 0.70416552], [0.79853165, 0.70416552], [0.79853165, 0.70416552]]),atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44532753, 0.44532753, 0.44532753]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06586759], [-0.06586759], [-0.06586759]]), atol=atol)

    # Epoch 3
    i = 3
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.78851699, 0.71551144], [0.78851699, 0.71551144], [0.78851699, 0.71551144]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44556275, 0.44556275, 0.44556275]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06588224], [-0.06588224], [-0.06588224]]), atol=atol)

    # Epoch 4
    i = 4
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.7806748, 0.72386837], [0.7806748, 0.72386837], [0.7806748, 0.72386837]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44526672, 0.44526672, 0.44526672]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06589504], [-0.06589504], [-0.06589504]]), atol=atol)

    # Epoch 5
    i = 5
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.77462336, 0.73025421], [0.77462336, 0.73025421], [0.77462336, 0.73025421]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44513758, 0.44513758, 0.44513758]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06586748], [-0.06586748], [-0.06586748]]), atol=atol)

    # Epoch 6
    i = 6
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.76993923, 0.73513742], [0.76993923, 0.73513742], [0.76993923, 0.73513742]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44505657, 0.44505657, 0.44505657]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06581052], [-0.06581052], [-0.06581052]]), atol=atol)

    # Epoch 7
    i = 7
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.76631135, 0.73888741], [0.76631135, 0.73888741], [0.76631135, 0.73888741]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.4450077, 0.4450077, 0.4450077]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.06572952], [-0.06572952], [-0.06572952]]), atol=atol)

    # Epoch 8
    i = 8
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.76349971, 0.74177524], [0.76349971, 0.74177524], [0.76349971, 0.74177524]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44497684, 0.44497684, 0.44497684]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.0656294], [-0.0656294], [-0.0656294]]), atol=atol)

    # Epoch 9
    i = 9
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[0.76131969, 0.74400418], [0.76131969, 0.74400418], [0.76131969, 0.74400418]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[0.44495633, 0.44495633, 0.44495633]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[-0.0655142], [-0.0655142], [-0.0655142]]), atol=atol)


def test_train_2():
    n = nn.NeuralNetwork()
    n.training_points = [((2, 1), 10), ((3, 3), 21), ((4, 5), 32), ((6, 6), 42)]
    n.learning_rate = 0.001
    atol = 1e-6

    # Epoch 0
    i = 0
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[1.002, 1.001], [1.002, 1.001], [1.002, 1.001]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[1.003, 1.003, 1.003]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[0.001], [0.001], [0.001]]), atol=atol)

    # Epoch 1
    i = 1
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[1.01077397, 1.00977397], [1.01077397, 1.00977397], [1.01077397, 1.00977397]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[1.02052462, 1.02052462, 1.02052462]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[0.00392466], [0.00392466], [0.00392466]]), atol=atol)

    # Epoch 2
    i = 2
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[1.02772391, 1.03096139], [1.02772391, 1.03096139], [1.02772391, 1.03096139]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[1.05829312, 1.05829312, 1.05829312]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[0.00816214], [0.00816214], [0.00816214]]), atol=atol)

    # Epoch 3
    i = 3
    x, y = n.training_points[i]
    n.train(x[0], x[1], y)
    np.testing.assert_allclose(n.input_to_hidden_weights, np.matrix([[1.04523414, 1.04847162], [1.04523414, 1.04847162], [1.04523414, 1.04847162]]), atol=atol)
    np.testing.assert_allclose(n.hidden_to_output_weights, np.matrix([[1.09237808, 1.09237808, 1.09237808]]), atol=atol)
    np.testing.assert_allclose(n.biases, np.matrix([[0.01108051], [0.01108051], [0.01108051]]), atol=atol)
