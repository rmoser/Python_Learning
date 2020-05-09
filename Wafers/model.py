import Wafers
import numpy as np
import matplotlib.pyplot as plt
import scipy


def test():
    w = Wafers.Wafer("A", 123)
    w.generate_array_map(1.5, 2.5)

    # fig = w.plot()
    return w

def run0():
    lot = Wafers.Lot("ALL")
    for wafer in batch0():
        lot.add_wafer(wafer)
    data = lot.die_isbad_vector()
    means = data.mean(axis=0)  # Mean for each position
    stddevs = data.std(axis=0)

    if any(stddevs == 0.):
        stddevs += np.min(stddevs[np.nonzero(stddevs)]) * 0.0001

    ndata = (data - means) / stddevs

    return lot, data, ndata

def batch0(shape=(2, 3)):
    wafers = []
    for i in range(100):
        w = Wafers.Wafer("ALL", i)
        wafers.append(w)
        w.generate_array_map(*shape)
        if i >= 80:
            defect_q3(w)
    return wafers


def defect_q3(wafer, bin=8):
    if not wafer._die:
        raise ValueError
    for die in wafer._die.values():
        if die.x <= 0 and die.y <= 0:
            die.bin = bin


def defect_top_edge(wafer, bin=8):
    if not wafer._die:
        raise ValueError

    for die in wafer._die.values():
        if die.y == wafer.y_max:
            die.bin = bin


def defect_xy(wafer, bin=8, xy=(1, 1)):
    if not wafer._die:
        raise ValueError
    wafer._die[xy].bin = bin


if __name__ == "__main__":
    test()
    plt.ioff()
    plt.show()
    #plt.savefig(r"c:\temp\d.png")
