from retino import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import time
import seaborn as sns
from multiprocessing import *

sns.set_style("darkgrid")

def produce_axon_growth_demo(id, target, iterations_count):
  t = time.time()
  axon = Axon(id=id, target = target)
  for i in range(iterations_count):
    axon.grow_cycle(time=i, post_synapses=[], activity=0.0)
  print("Growth demo finished growing for Axon " + str(id) + " in " + str(time.time() - t))
  t = time.time()
  plot_axon_growth(axon, "Plots/AxonGrowth", 100.0, 100.0, granularity=10)
  print("Growth demo finished plotting for Axon " + str(id) + " in " + str(time.time() - t))

def produce_axon_demos_with_postsynapse_coloring(targets):
  t = time.time()
  post_synapses = [PostSynapse(i, size=20, tectum_length=75.0, tectum_width=75.0) for i in range(100)]
  axons = [Axon(id=i, target = targets[i]) for i in range(len(targets))]
  for axon in axons:
    t = time.time()
    for i in range(200):
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=0.0)
    print("Finished Axon ", axon.id, " in ", time.time() - t, "s.")

  for i in range(0, 20):
    fig, axarr = plt.subplots(2)
    for axon in axons:
      add_post_synapses_to_axarr_by_axon(axon, axarr, i, 75.0, 75.0)
    axarr[0].set_title("Colored Points by Gradient Along X")
    axarr[1].set_title("Colored Points by Gradient Along Y")
    for ax in axarr:
      ax.set_aspect('equal', 'datalim')
      ax.set_xlim([0,75.0])
      ax.set_ylim([0,75.0])
    plt.tight_layout()
    plt.savefig("Plots/synapses/ColoredByTarget-" + str(i) + ".png", dpi=200)
    plt.close(fig)
    print("Finished ColoredByTarget-" + str(i) + " in " + str(time.time() - t))

if __name__ == '__main__':
  
  targets = np.mgrid[20:100:30,20:100:30].reshape(2,-1).T
  for i in range(len(targets)):
    p = Process(target=produce_axon_growth_demo, args=(i, targets[i],300))
    p.start()
    print("Started P",i,"for",targets[i])

  targets = np.mgrid[20:100:20,20:100:20].reshape(2,-1).T
  targets = add_jitter_to_points(targets, 5)
  p = Process(target=produce_axon_demos_with_postsynapse_coloring, args=(targets,))
  p.start()
  print("Started process for postsynapse colouring")
