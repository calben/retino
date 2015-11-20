from retino import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import time


sns.set_style("darkgrid")

def produce_axon_interaction_demos_with_postsynapse_coloring():
  targets = add_jitter_to_points([np.asarray([25.0,25.0])] * 4, 10) 
  targets.extend(add_jitter_to_points([np.asarray([30.0,30.0])] * 4, 10))
  targets.extend(add_jitter_to_points([np.asarray([15.0,25.0])] * 4, 10))
  targets.extend(add_jitter_to_points([np.asarray([25.0,15.0])] * 4, 10))

  dots_origins = list(map(np.asarray, [[25.0] * 2, [30.0] * 2, [35.0] * 2, [40.0] * 2, [45.0] * 2]))
  dots_sizes = [5] * len(dots_origins)

  post_synapses = [PostSynapse(i, size=10, tectum_length=75.0, tectum_width=75.0) for i in range(100)]
  axons = [Axon(id=i, target = targets[i]) for i in range(len(targets))]
  for axon in axons:
    t = time.time()
    for i in range(200):
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=0.0)
      # score = get_average_point_error(axon.target, [p.origin for p in axon.synapses])
      # print("Axon", axon.id, " iter", i, "with score of", score)
    print("Finished Growing Axon", axon.id, "in", (time.time() - t), "s.")

  for i in range(200,400):
    t = time.time()
    for axon in axons:
      dots_index = i % len(dots_origins)
      activity = 0
      if(is_point_within_circle(axon.target, dots_origins[dots_index], dots_sizes[dots_index])):
        activity = 0.3
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=activity)
      total_error = np.average([get_average_point_error(a.target, [p.origin for p in a.synapses]) for a in axons])
    print("Finished cycle", i, "in", time.time() - t, "s.", " Total score", total_error)

  for i in range(0, 40):
    fig, axarr = plt.subplots(2)
    for axon in axons:
      add_post_synapses_to_axarr_by_axon(axon, axarr, i, 75.0, 75.0)
    tm = axons[0].history[i][0]
    dots_index = tm % len(dots_origins)
    axarr[0].set_title("Colored Points by Gradient Along X")
    axarr[1].set_title("Colored Points by Gradient Along Y")
    for ax in axarr:
      ax.set_aspect('equal', 'datalim')
      ax.add_collection(EllipseCollection(widths=dots_sizes[dots_index], heights=[dots_sizes[dots_index]], angles=0, units='xy',
             facecolors='b',
             offsets=dots_origins[dots_index], transOffset=ax.transData, alpha=0.1))
    plt.tight_layout()
    plt.savefig("Plots/synapsesInteractions/ColoredByTarget-" + str(i) + ".png", dpi=200)
    plt.close(fig)

# produce_axon_interaction_demos_with_postsynapse_coloring()

# produce_axon_growth_demos()
