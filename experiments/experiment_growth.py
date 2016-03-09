import os
import time
import numpy as np

from multiprocessing import Process

from retino.axon import Axon
from retino.plot import plot_axon


def produce_axon_growth_demo(id, target, iterations_count):
    t = time.time()
    axon = Axon(None, id=id, target=target)
    for i in range(iterations_count):
        axon.grow()
        output_directory = "../Plots/AxonGrowth/AXON-id=" + str(axon.id) + "-target=" + str(axon.target)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        number = "%04d" % i
        plot_axon(axon, output_directory + "/" + number + ".png", 100.0, 100.0)
    print("Growth demo finished plotting for Axon " + str(id) + " in " + str(time.time() - t))


if __name__ == '__main__':

    targets = np.mgrid[20:100:30, 20:100:30].reshape(2, -1).T
    for i in range(len(targets)):
        p = Process(target=produce_axon_growth_demo, args=(i, targets[i], 300))
        p.start()
        print("Started P", i, "for", targets[i])
