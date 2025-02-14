import project1
import project1 as p1
import test_project1
import utils
import numpy as np
import pytest

from project1 import accuracy
from test_project1 import test_classifier_accuracy_00

#-------------------------------------------------------------------------------
# Data loading. There is no need to edit code in this section.
#-------------------------------------------------------------------------------

train_data = utils.load_data('reviews_train.tsv')
val_data = utils.load_data('reviews_val.tsv')
test_data = utils.load_data('reviews_test.tsv')

train_texts, train_labels = zip(*((sample['text'], sample['sentiment']) for sample in train_data))
val_texts, val_labels = zip(*((sample['text'], sample['sentiment']) for sample in val_data))
test_texts, test_labels = zip(*((sample['text'], sample['sentiment']) for sample in test_data))

try:
    dictionary = p1.bag_of_words(train_texts)
    dictionary2 = p1.bag_of_words(train_texts, remove_stopword=True)
except:
    dictionary = None
    dictionary2 = None

MODE = 2
if dictionary:
    if MODE == 2:
        d = dictionary2
        binarize = False
    else:
        d = dictionary
        binarize = True

    train_bow_features = p1.extract_bow_feature_vectors(train_texts, d, binarize=binarize)
    val_bow_features = p1.extract_bow_feature_vectors(val_texts, d, binarize=binarize)
    test_bow_features = p1.extract_bow_feature_vectors(test_texts, d, binarize=binarize)

#-------------------------------------------------------------------------------
# Problem 5
#-------------------------------------------------------------------------------

# toy_features, toy_labels = toy_data = utils.load_toy_data('toy_data.tsv')
#
# T = 10
# L = 0.2
#
# thetas_perceptron = []
# thetas_avg_perceptron = []
# thetas_pegasos = []
#
# for x in range(1, 5):
#     thetas_perceptron.append(p1.perceptron(toy_features, toy_labels, T*x))
#     thetas_avg_perceptron.append(p1.average_perceptron(toy_features, toy_labels, T*x))
#     thetas_pegasos.append(p1.pegasos(toy_features, toy_labels, T*x, L))
#
# # def converged(model_name, thetas):
# #     for i, (a, b) in enumerate(zip(thetas[:-1], thetas[1:])):
# #         if a[0] == pytest.approx(b[0], 0.1) and a[1] == pytest.approx(b[1], 0.02):
# #             print(f'{model_name} converged at epoch {i+1}')
# #             break
# #     else:
# #         print(f'{model_name} did not converge')
# #
# # converged('Perceptron', thetas_perceptron)
# # converged('Average Perceptron', thetas_avg_perceptron)
# # converged('Pegasos', thetas_pegasos)
#
# def plot_toy_results(algo_name, thetas):
#     print('\ntheta for', algo_name, 'is', ', '.join(map(str,list(thetas[0]))))
#     print('theta_0 for', algo_name, 'is', str(thetas[1]))
#     utils.plot_toy_data(algo_name, toy_features, toy_labels, thetas)
#
# plot_toy_results('Perceptron', thetas_perceptron)
# plot_toy_results('Average Perceptron', thetas_avg_perceptron)
# plot_toy_results('Pegasos', thetas_pegasos)
# utils.plt.show()

#-------------------------------------------------------------------------------
# Problem 7
#-------------------------------------------------------------------------------
#
# T = 10
# L = 0.01
#
# pct_train_accuracy, pct_val_accuracy = \
#    p1.classifier_accuracy(p1.perceptron, train_bow_features, val_bow_features, train_labels,val_labels,T=T)
# print("{:35} {:.4f}".format("Training accuracy for perceptron:", pct_train_accuracy))
# print("{:35} {:.4f}".format("Validation accuracy for perceptron:", pct_val_accuracy))
#
# avg_pct_train_accuracy, avg_pct_val_accuracy = \
#    p1.classifier_accuracy(p1.average_perceptron, train_bow_features,val_bow_features,train_labels,val_labels,T=T)
# print("{:43} {:.4f}".format("Training accuracy for average perceptron:", avg_pct_train_accuracy))
# print("{:43} {:.4f}".format("Validation accuracy for average perceptron:", avg_pct_val_accuracy))
#
# avg_peg_train_accuracy, avg_peg_val_accuracy = \
#    p1.classifier_accuracy(p1.pegasos, train_bow_features,val_bow_features,train_labels,val_labels,T=T,L=L)
# print("{:50} {:.4f}".format("Training accuracy for Pegasos:", avg_peg_train_accuracy))
# print("{:50} {:.4f}".format("Validation accuracy for Pegasos:", avg_peg_val_accuracy))

#-------------------------------------------------------------------------------
# Problem 8
#-------------------------------------------------------------------------------
#
# data = (train_bow_features, train_labels, val_bow_features, val_labels)
#
# # values of T and lambda to try
# Ts = [1, 5, 10, 15, 25, 50]
# Ls = [0.001, 0.01, 0.1, 1, 10]
#
# pct_tune_results = utils.tune_perceptron(Ts, *data)
# print('perceptron valid:', list(zip(Ts, pct_tune_results[1])))
# print('best = {:.4f}, T={:.4f}'.format(np.max(pct_tune_results[1]), Ts[np.argmax(pct_tune_results[1])]))
#
# avg_pct_tune_results = utils.tune_avg_perceptron(Ts, *data)
# print('avg perceptron valid:', list(zip(Ts, avg_pct_tune_results[1])))
# print('best = {:.4f}, T={:.4f}'.format(np.max(avg_pct_tune_results[1]), Ts[np.argmax(avg_pct_tune_results[1])]))
#
# # fix values for L and T while tuning Pegasos T and L, respective
# fix_L = 0.01
# peg_tune_results_T = utils.tune_pegasos_T(fix_L, Ts, *data)
# print('Pegasos valid: tune T', list(zip(Ts, peg_tune_results_T[1])))
# print('best = {:.4f}, T={:.4f}'.format(np.max(peg_tune_results_T[1]), Ts[np.argmax(peg_tune_results_T[1])]))
#
# fix_T = Ts[np.argmax(peg_tune_results_T[1])]
# peg_tune_results_L = utils.tune_pegasos_L(fix_T, Ls, *data)
# print('Pegasos valid: tune L', list(zip(Ls, peg_tune_results_L[1])))
# print('best = {:.4f}, L={:.4f}'.format(np.max(peg_tune_results_L[1]), Ls[np.argmax(peg_tune_results_L[1])]))

# utils.plot_tune_results('Perceptron', 'T', Ts, *pct_tune_results)
# utils.plot_tune_results('Avg Perceptron', 'T', Ts, *avg_pct_tune_results)
# utils.plot_tune_results('Pegasos', 'T', Ts, *peg_tune_results_T)
# utils.plot_tune_results('Pegasos', 'L', Ls, *peg_tune_results_L)

#-------------------------------------------------------------------------------
# Use the best method (perceptron, average perceptron or Pegasos) along with
# the optimal hyperparameters according to validation accuracies to test
# against the test dataset. The test data has been provided as
# test_bow_features and test_labels.
#-------------------------------------------------------------------------------

T = 25
L = 0.0100

model = project1.pegasos(train_bow_features, train_labels, T, L)
train_accuracy = accuracy(project1.classify(train_bow_features, model[0], model[1]), train_labels)
val_accuracy = accuracy(project1.classify(val_bow_features, model[0], model[1]), val_labels)
test_accuracy = accuracy(project1.classify(test_bow_features, model[0], model[1]), test_labels)
# test_accuracy = project1.classifier_accuracy(project1.pegasos, train_bow_features, test_bow_features, train_labels, test_labels, T=T, L=L)

print(f'Pegasos test accuracy with T: {T} L: {L} => {test_accuracy}')

#-------------------------------------------------------------------------------
# Assign to best_theta, the weights (and not the bias!) learned by your most
# accurate algorithm with the optimal choice of hyperparameters.
#-------------------------------------------------------------------------------
#
# best_theta = model[0] # Your code here
# wordlist   = [word for (idx, word) in sorted(zip(dictionary.values(), dictionary.keys()))]
# sorted_word_features = utils.most_explanatory_word(best_theta, wordlist)
# print("Most Explanatory Word Features")
# print(sorted_word_features[:10])
