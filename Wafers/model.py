import Wafers
import numpy as np
import matplotlib.pyplot as plt
import scipy


def test():
    w = Wafers.Wafer("A", 123)
    w.generate_array_map(1.5, 2.5)

    # fig = w.plot()
    return w

def run(lot=None):
    if lot is None:
        raise ValueError("Pass a Lot object containing Wafers for analysis.")

    lot = Wafers.Lot("ALL")
    for wafer in lot():
        lot.add_wafer(wafer)
    data = lot.die_isbad_vector()
    means = data.mean(axis=0)  # Mean for each position
    stddevs = data.std(axis=0)

    if any(stddevs == 0.):
        # stddevs += np.min(stddevs[np.nonzero(stddevs)]) * 0.0001  # Adjust to avoid zero stddev
        stddevs += np.min(stddevs[np.nonzero(stddevs)]) * np.random.normal(size=len(stddevs)) * 0.0001  # Adjust to avoid zero stddev

    w0 = lot.wafers[0].__deepcopy__()
    w1 = w0.__deepcopy__()

    X, evals, evecs = PCA(data)
    v0 = evecs.T[0] * X[0][0]
    v1 = evecs.T[0] * X[80][0]

    for die, val in zip(w0.die, np.bool8(v0)):
        die.bin = val * 8

    for die, val in zip(w1.die, np.bool8(v1)):
        die.bin = val * 8

    w0.plot()
    w1.plot()
    plt.show()

    # w.set_param_vector(means)
    # w.plot(z='param')
    # plt.show()


    # A = (data - means)
    # A = (data - means) / stddevs
    # # Again add small noise terms to help SVD converge
    # A += np.mean(means) * np.random.normal(size=(len(lot.wafers), len(means))) * 0.0001
    #
    # L = A * A.T
    # (eigvals, eigvecs) = np.linalg.eig(L)


    # Flatten so we can make covariance matrix
    # A = np.asmatrix([a.flatten() for a in ndata])
    # L = A * A.T
    #
    # # Looks like the eigenvectors come back normalized already
    # (eigvals, eigvecs) = np.linalg.eig(L)
    #
    # # Sort values/vectors here, drop if eigenvalue is zero
    #
    # # Sort the eigenvalues
    # keep = np.argsort(eigvals)[::-1]  # argsort returns in ascending order, so we reverse the result
    # keep = [k for k, i in enumerate(keep) if eigvals[i] > 1e-4]
    # eigvals = eigvals[keep]
    # eigvecs = np.asarray([e[0, keep] for e in eigvecs])
    #
    # X = A.T * eigvecs
    # Y = X / np.sqrt(eigvals)
    # C = np.array([y.reshape((300, 300)) for y in Y.T])

    return lot, data, X, evals, evecs


def gfa(shape=(2, 3), defect=None):
    if defect is None:
        defect = defect_q3

    if not callable(defect):
        raise ValueError("defect function required.")

    lot = Wafers.Lot("ALL")
    for i in range(20):
        w = Wafers.Wafer("", i)
        lot.add_wafer(w)
        w.generate_array_map(*shape)
        if i >= 10:
            defect(w)
    return lot


def defect_q3(wafer, bin=8):
    if not len(wafer):
        raise ValueError
    for die in wafer:
        if die.x <= 0 and die.y <= 0:
            die.bin = bin


def defect_top_edge(wafer, bin=8):
    if not wafer:
        raise ValueError

    for die in wafer:
        if die.y == wafer.y_max:
            die.bin = bin


def defect_xy(wafer, bin=8, xy=(1, 1)):
    if not xy in wafer:
        raise ValueError(f"Coord {xy} not in Wafer {wafer}")
    if xy in wafer:
        wafer[xy].bin = bin



def PCA(data, dims_rescaled_data=2):
    """
    returns: data transformed in 2 dims/columns + regenerated original data
    pass in: data as 2D NumPy array
    """
    import numpy as np
    from scipy import linalg as la
    m, n = data.shape
    # mean center the data
    means = data.mean(axis=0)
    ndata = data - means
    # calculate the covariance matrix
    R = np.cov(ndata, rowvar=False)
    # calculate eigenvectors & eigenvalues of the covariance matrix
    # use 'eigh' rather than 'eig' since R is symmetric,
    # the performance gain is substantial
    evals, evecs = la.eigh(R)
    # sort eigenvalue in decreasing order
    idx = np.argsort(evals)[::-1]
    evecs = evecs[:, idx]
    # sort eigenvectors according to same index
    evals = evals[idx]
    # select the first n eigenvectors (n is desired dimension
    # of rescaled data array, or dims_rescaled_data)
    evecs = evecs[:, :dims_rescaled_data]
    # carry out the transformation on the data using eigenvectors
    # and return the re-scaled data, eigenvalues, and eigenvectors
    X = np.dot(evecs.T, data.T).T
    rec_data = evecs.T * X + means
    return X, evals, evecs, rec_data


def test_PCA(data, dims_rescaled_data=2):
    '''
    test by attempting to recover original data array from
    the eigenvectors of its covariance matrix & comparing that
    'recovered' array with the original data
    '''
    m, n = data.shape
    _, _, eigenvectors = PCA(data, dim_rescaled_data=2)
    data_recovered = np.dot(eigenvectors, m).T
    data_recovered += data_recovered.mean(axis=0)
    assert np.allclose(data, data_recovered)


def plot_pca(data):
    from matplotlib import pyplot as MPL
    clr1 = '#2026B2'
    fig = MPL.figure()
    ax1 = fig.add_subplot(111)
    data_resc, _, _ = PCA(data)
    ax1.plot(data_resc[:, 0], data_resc[:, 1], '.', mfc=clr1, mec=clr1)
    MPL.show()


if __name__ == "__main__":
    # test()
    # plt.ioff()
    # plt.show()
    # plt.savefig(r"c:\temp\d.png")

    lot = gfa()
    lot[0].plot()
