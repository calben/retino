import os
import time
import numpy as np

from multiprocessing import Process

from retino.axon import Axon
from retino.plot import plot_axon
from retino.model import Model
import retino

def produce_axon_growth_demo(id, targets, iterations_count):
    model = Model(name="testing_activity", targets=targets)
    t = time.time()
    for i in range(iterations_count):
        if i > 20:
            axon_indexes_to_fire = np.random.choice(len(targets), len(targets)/8)
            for index in axon_indexes_to_fire:
                model.axons[index].fire()
        model.iterate(write_to_disk=False)
        if i % 50 == 0:
            for axon in model.axons:
                output_directory = "../results/Plots/AxonGrowth/AXON-id=" + str(axon.id) + "-target=" + str(axon.target)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                number = "%04d" % i
                plot_axon(axon, output_directory + "/" + number + ".png", 100.0, 100.0)
    print("Activity demo finished plotting for Axon " + str(id) + " in " + str(time.time() - t))


if __name__ == '__main__':
    targets = np.mgrid[20:100:10, 20:100:10].reshape(2, -1).T
    i = 0
    p = Process(target=produce_axon_growth_demo, args=(i, targets, 600))
    p.start()
    print("Started P", i, "for", targets)
