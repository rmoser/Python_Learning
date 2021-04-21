# Script to  actually run the LDA analysis

import my_lda
import pandas as pd
import argparse
import stochastic_lda as slda

# import urllib.request
# from bs4 import BeautifulSoup
import os
import re
import string
# lda.save_abstracts()
import pandas as pd
import numpy as np
import numpy as n
import sys, re, time, string, random, csv, argparse
from scipy.special import psi
from nltk.tokenize import wordpunct_tokenize
from utils import *

# Override one prof
prof = 'Elfar Adalsteinsson'

np.random.seed(10000001)
meanchangethresh = 1e-3
MAXITER = 10000


class SVILDA():
    def __init__(self, K, alpha, eta, tau, kappa, docs, iterations, parsed=True):
        # Docs variables
        self._docs = docs
        self._D = len(self._docs.index)  # Count of docs
        self._vocab = dict(zip(docs.columns, range(self._D)))  # Maps words to column numbers in arrays & matrices
        self._V = len(self._vocab)  # Count of words
        self._parsed = isinstance(self._docs, pd.DataFrame)

        # LDA algorithm tuning parameters
        self._K = K
        self._alpha = alpha
        self._eta = eta
        self._tau = tau
        self._kappa = kappa
        self._iterations = iterations

        # Initialize LDA algorithm state variables
        self.resetSVI()

        if not (0 < self._kappa <= 1):
            print(r"\nERROR: kappa must be in the range (0, 1]: {}\n".format(self._kappa))

    def resetSVI(self):
        # Initialize LDA algorithm state variables
        self._lambda = 1 * n.random.gamma(100., 1. / 100., (self._K, self._V))
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = n.exp(self._Elogbeta)
        self.ct = 0
        self._trace_lambda = {}
        for i in range(self._K):
            self._trace_lambda[i] = [self.computeProbabilities()[i]]
        self._x = [0]

        print(self._lambda.shape)

    def word_num(self, word, readonly=True):
        if word not in self._vocab:
            if readonly is True:
                return None
            # Readonly is false, so add the word
            self._vocab[word] = len(self._vocab)

        # Return the word index
        return self._vocab[word]

    def updateLocal(self, doc):  # word_dn is an indicator variable with dimension V
        # print("words: ", len(words), type(words))
        # print("counts: ", len(counts), type(counts))

        newdoctype = 'S'  # S-series or L-list

        if newdoctype == 'S':
            # newdoc shall be a Pandas Series
            # Compress to only the words with non-zero frequency
            newdoc = doc[doc.values > 0]

            assert n.sum(newdoc) == n.sum(doc)

            phi_d = n.zeros((self._K, self._V))  # Topics x Total Words
            gamma_d = n.random.gamma(100., 1. / 100., (self._K))

            for i in range(self._iterations):
                Elogtheta_d = dirichlet_expectation(gamma_d)
                expElogtheta_d = n.exp(Elogtheta_d)

                for word, count in newdoc.items():
                    w = self.word_num(word)
                    phi_d[:, w] = n.multiply(expElogtheta_d ** count, self._expElogbeta[:, w]) + 1e-100
                    phi_d[:, w] = phi_d[:, w] / n.sum(phi_d[:, w])

                gamma_new = self._alpha + n.sum(phi_d, axis=1)
                meanchange = n.mean(abs(gamma_d - gamma_new))
                if meanchange < meanchangethresh:
                    break

                gamma_d = gamma_new

            return phi_d, newdoc, gamma_d

        else:
            # newdoc is a list of the words, once for each occurrence of the word in the doc
            newdoc = []
            for word in doc.index:
                newdoc += [word] * doc[word]

            # Total words in this doc
            N_d = n.sum(doc)  # Use doc just to be sure

            assert len(newdoc) == N_d

            phi_d = n.zeros((self._K, N_d))  # Topics x Total Words
            gamma_d = n.random.gamma(100., 1. / 100., (self._K))

            for i in range(self._iterations):
                Elogtheta_d = dirichlet_expectation(gamma_d)
                expElogtheta_d = n.exp(Elogtheta_d)

                for m, word in enumerate(newdoc):
                    w = self.word_num(word)
                    phi_d[:, m] = n.multiply(expElogtheta_d, self._expElogbeta[:, w]) + 1e-100
                    phi_d[:, m] = phi_d[:, m] / n.sum(phi_d[:, m])

                gamma_new = self._alpha + n.sum(phi_d, axis=1)
                meanchange = n.mean(abs(gamma_d - gamma_new))
                if meanchange < meanchangethresh:
                    break

                gamma_d = gamma_new

        # print(newdoc)


            return phi_d, newdoc, gamma_d


    def updateGlobal(self, phi_d, newdoc):
        # print 'updating global parameters'
        lambda_d = n.zeros((self._K, self._V))

        for k in range(self._K):
            phi_dk = n.zeros(self._V)  # array of length = word count

            if isinstance(newdoc, pd.Series):
                # doc is pandas Series with words and counts
                for word in newdoc.index:
                    # print word
                    # phi_dk[word] += phi_d[k][m]
                    w = self.word_num(word)  # Word index
                    phi_dk[w] += phi_d[k, w]

            else:
                # doc is a list of words repeated
                for m, word in enumerate(newdoc):
                    # print word
                    # phi_dk[word] += phi_d[k][m]
                    w = self.word_num(word)  # Word index
                    phi_dk[w] += phi_d[k, m]

            lambda_d[k] = self._eta + self._D * phi_dk

        rho = (self.ct + self._tau) ** (-self._kappa)
        self._lambda = (1 - rho) * self._lambda + rho * lambda_d
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = n.exp(self._Elogbeta)

        if self.ct % 10 == 9:
            for i in range(self._K):
                self._trace_lambda[i].append(self.computeProbabilities()[i])
            self._x.append(self.ct)


    def runSVI(self):
        ilen = len(str(self._iterations))  # digits in iteration limit
        dlen = len(str(self._D))  # digits in document count

        for i in range(self._iterations):
            # Why was this D - 1 instead of D?  randint(n) generates values from 0 to n-1 already
            # randint = np.random.randint(0, self._D - 1)
            randint = np.random.randint(0, self._D)

            print("ITERATION {i:{ilen}} of {ni}  running document number {d:{dlen}} of {nd}"
                  .format(i=i, ilen=ilen, ni=self._iterations, d=randint, dlen=dlen, nd=self._D))

            # Column numbers and
            # a Random row from the abstract word count matrix
            doc = self._docs.iloc[randint]  # Pandas Series

            # newdoc is a pandas Series
            phi_doc, newdoc, gamma_d = self.updateLocal(doc)
            self.updateGlobal(phi_doc, newdoc)
            self.ct += 1


    def computeProbabilities(self):
        prob_topics = n.sum(self._lambda, axis=1)
        prob_topics = prob_topics / n.sum(prob_topics)
        return prob_topics


    def getTopics(self, docs=None):
        prob_topics = self.computeProbabilities()  # Prob per topic
        prob_words = n.sum(self._lambda, axis=0)   # Prob per word

        if docs == None:
            docs = self._docs

        results = n.zeros((len(docs), self._K))

        # For each doc
        for i in range(self._D):
            doc = docs.iloc[i]  # Pandas Series for row i
            doc = doc[doc.value > 0]  # Drop words with zero counts to speed up the looping

            # For each topic
            for j in range(self._K):
                doc_probability = 0.0

                # For each word
                for word in doc.index:
                    # Word index in global tables
                    w = self.word_num(word)

                    # Collect list of lambda / word probability
                    doc_probability += n.log(self._lambda[j][w] / prob_words[w]) * doc[word]

                results[i][j] = doc_probability + n.log(prob_topics[j])

        finalresults = n.zeros(len(docs))

        for k in range(len(docs)):
            finalresults[k] = n.argmax(results[k])

        return finalresults, prob_topics


    def calcPerplexity(self, docs=None):
        perplexity = 0.
        doclen = 0.
        if docs == None:
            docs = self._docs
        # if isinstance(docs, pd.DataFrame):
        #     # Convert to Matrix
        #     docs = docs.values
        for _, doc in docs.iterrows():
            _, newdoc, gamma_d = self.updateLocal(doc)

            approx_mixture = n.dot(gamma_d, self._lambda)
            # print n.shape(approx_mixture)
            approx_mixture = approx_mixture / n.sum(approx_mixture)

            log_doc_prob = 0.

            if isinstance(newdoc, pd.Series):
                newdoc = newdoc[newdoc.values > 0]
                for word, count in newdoc.items():
                    w = self.word_num(word)
                    log_doc_prob += n.log(approx_mixture[w]) * count

                perplexity += log_doc_prob
                doclen += sum(newdoc)

            else:
                for word in newdoc:
                    w = self.word_num(word)
                    log_doc_prob += n.log(approx_mixture[w])

                perplexity += log_doc_prob
                doclen += len(newdoc)

            # print perplexity, doclen
        perplexity = n.exp(- perplexity / doclen)
        print(perplexity)
        return perplexity

    def plotTopics(self, perp):
        plottrace(self._x, self._trace_lambda, self._K, self._iterations, perp)


def test(k, iterations):
    #allmydocs = getalldocs("alldocs2.txt")
    profs = ['Elfar Adalsteinsson']
    allmydocs = my_lda.build_word_matrix(profs)
    vocab = list(allmydocs.columns)

    testset = SVILDA(vocab=vocab, K=k, D=len(allmydocs), alpha=0.2, eta=0.2, tau=1024, kappa=0.7, docs=allmydocs,
                     iterations=iterations)
    testset.runSVI()

    finallambda = testset._lambda

    heldoutdocs = getalldocs("testdocs.txt")

    perplexity = testset.calcPerplexity(docs=heldoutdocs)

    with open("temp/%i_%i_%f_results.csv" % (k, iterations, perplexity), "w+") as f:
        writer = csv.writer(f)
        for i in range(k):
            bestwords = sorted(range(len(finallambda[i])), key=lambda j: finallambda[i, j])
            # print bestwords
            bestwords.reverse()
            writer.writerow([i])
            for j, word in enumerate(bestwords):
                writer.writerow([word, vocab.keys()[vocab.values().index(word)]])
                if j >= 15:
                    break
    topics, topic_probs = testset.getTopics()
    testset.plotTopics(perplexity)

    for kk in range(0, len(finallambda)):
        lambdak = list(finallambda[kk, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak)))
        temp = sorted(temp, key=lambda x: x[0], reverse=True)
        # print temp
        print('topic %d:' % (kk))
        # feel free to change the "53" here to whatever fits your screen nicely.
        for i in range(0, 10):
            print('%20s  \t---\t  %.4f' % (vocab.keys()[vocab.values().index(temp[i][1])], temp[i][0]))
        print()

    with open("temp/%i_%i_%f_raw.txt" % (k, iterations, perplexity), "w+") as f:
        # f.write(finallambda)
        for result in topics:
            f.write(str(result) + " \n")
        f.write(str(topic_probs) + " \n")


def test_SVILDA(docs):
    # return SVILDA(list(docs.columns), K=5, D=len(docs), alpha=0.2, eta=0.2, tau=1024, kappa=0.7, docs=docs, iterations=iters, parsed=True)
    # return SVILDA2(docs, K=5, alpha=0.2, eta=0.2, tau=1024, kappa=0.7, iterations=500)

    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-K', '--topics', help='number of topics, defaults to 10', required=True)
    parser.add_argument('-m', '--mode', help='mode, test | normal', required=True)
    parser.add_argument('-v', '--vocab', help='Vocab file name, .csv', default="dictionary.csv", required=False)
    parser.add_argument('-d', '--docs', help='file with list of docs, .txt', default="alldocs.txt", required=False)
    parser.add_argument('-a', '--alpha', help='alpha parameter, defaults to 0.2', default=0.2, required=False)
    parser.add_argument('-e', '--eta', help='eta parameter, defaults to 0.2', default=0.2, required=False)
    parser.add_argument('-t', '--tau', help='tau parameter, defaults to 1024', default=1024, required=False)
    parser.add_argument('-k', '--kappa', help='kappa parameter, defaults to 0.7', default=0.7, required=False)
    parser.add_argument('-n', '--iterations', help='number of iterations, defaults to 10000', default=10000,
                        required=False)

    args = parser.parse_args()

    K = int(args.topics)
    mode = str(args.mode)
    vocab = str(args.vocab)
    docs = str(args.docs)
    alpha = float(args.alpha)
    eta = float(args.eta)
    tau = float(args.tau)
    kappa = float(args.kappa)
    iter = int(args.iterations)

    if mode == "test":
        test(K, iter)
    else:
        assert vocab is not None, "no vocab"
        assert docs is not None, "no docs"
        docs = my_lda.build_word_matrix()
        docs = my_lda.calc_freqs(docs)
        D = len(docs)
        # vocab = getVocab(vocab)
        vocab = dict(zip(docs.columns, range(docs.shape[1])))

        # self, K, D, alpha, eta, tau, kappa, docs, iterations
        lda_inst = SVILDA(K=K, alpha=alpha, eta=eta, tau=tau, kappa=kappa, docs=docs,
                     iterations=iter)

        lda_inst._parsed = isinstance(docs, pd.DataFrame)

        lda_inst.runSVI()

        return lda_inst


if __name__ == '__main__':
    main()


