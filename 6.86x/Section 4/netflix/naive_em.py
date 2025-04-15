"""Mixture model using EM"""
from typing import Tuple
import numpy as np
from sklearn.covariance import log_likelihood

import common
from common import GaussianMixture



def estep(X: np.ndarray, mixture: GaussianMixture) -> Tuple[np.ndarray, float]:
    """E-step: Softly assigns each datapoint to a gaussian component

    Args:
        X: (n, d) array holding the data
        mixture: the current gaussian mixture

    Returns:
        np.ndarray: (n, K) array holding the soft counts
            for all components for all examples
        float: log-likelihood of the assignment
    """
    # E = np.exp(-0.5 * (np.square(np.expand_dims(X, 1) - mixture.mu).sum(axis=2) / np.expand_dims(mixture.var, 1)).sum(axis=2))
    E = np.exp(-0.5 * (np.square(np.expand_dims(X, 1) - mixture.mu).sum(axis=2) / np.expand_dims(mixture.var, 0)))
    P = (1 / (2 * np.pi * mixture.var) ** (X.shape[1]/2) * E) * mixture.p
    probs = P / np.expand_dims(P.sum(axis=1), 1)
    log_likelihood = np.log(P.sum(axis=1)).sum()
    return probs, log_likelihood


def mstep(X: np.ndarray, post: np.ndarray) -> GaussianMixture:
    """M-step: Updates the gaussian mixture by maximizing the log-likelihood
    of the weighted dataset

    Args:
        X: (n, d) array holding the data
        post: (n, K) array holding the soft counts
            for all components for all examples

    Returns:
        GaussianMixture: the new gaussian mixture
    """
    nj = np.sum(post, axis=0)  # shape is (K, )
    p = post.mean(axis=0)

    mu = post.T @ X / np.expand_dims(nj, 1)
    var = (post * ((np.expand_dims(X, 1) - mu)**2).sum(axis=2)).sum(axis=0) / (nj * X.shape[1])
    return GaussianMixture(mu, var, p)




def run(X: np.ndarray, mixture: GaussianMixture,
        post: np.ndarray) -> Tuple[GaussianMixture, np.ndarray, float]:
    """Runs the mixture model

    Args:
        X: (n, d) array holding the data
        post: (n, K) array holding the soft counts
            for all components for all examples

    Returns:
        GaussianMixture: the new gaussian mixture
        np.ndarray: (n, K) array holding the soft counts
            for all components for all examples
        float: log-likelihood of the current assignment
    """
    raise NotImplementedError
