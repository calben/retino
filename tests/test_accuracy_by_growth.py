from retino import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import time
import seaborn as sns

sns.set_style("darkgrid")

def produce_axon_growth_accuracy_demos_with_postsynapse_coloring():
  targets = add_jitter_to_points([np.asarray([40.0,40.0])] * 20, 10) 
  targets.extend(add_jitter_to_points([np.asarray([40.0,60.0])] * 20, 10)) 
  targets.extend(add_jitter_to_points([np.asarray([60.0,40.0])] * 20, 10)) 
  targets.extend(add_jitter_to_points([np.asarray([60.0,60.0])] * 20, 10))

  dots_origins = list(map(np.asarray, [[25.0] * 2, [30.0] * 2, [35.0] * 2, [40.0] * 2, [45.0] * 2]))
  dots_sizes = [5] * len(dots_origins)

  post_synapses = [PostSynapse(o[0], size=10, origin=o) for o in targets]
  axons = [Axon(id=i, target = targets[i]) for i in range(len(targets))]
  for axon in axons:
    t = time.time()
    for i in range(200):
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=0.0)
      # score = get_average_point_error(axon.target, [p.origin for p in axon.synapses])
      # print("Axon", axon.id, " iter", i, "with score of", score)
    print("Finished Growing Axon", axon.id, "in", (time.time() - t), "s.")


  average_points_error_f = open('average-points-error.csv', 'w')
  average_points_error_f.write(",".join("axon-" + str(x.id) + "average-points-error" for x in axons) + "\n")
  
  for i in range(200,400):
    t = time.time()
    for axon in axons:
      dots_index = i % len(dots_origins)
      activity = 0
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=activity)
      total_error = np.nanmean([get_average_point_error(a.target, [p.origin for p in a.synapses]) for a in axons])
    print("Finished cycle", i, "in", time.time() - t, "s.", " Total score", total_error)
    average_points_error_f.write(",".join([str(get_average_point_error(a.target, [p.origin for p in a.synapses])) for a in axons]) + "\n")

  output_directory = "Plots/GrowthAccuracyPostSynapses" 
  if not os.path.exists(output_directory):
    os.makedirs(output_directory)
  for i in range(0,len(axons[0].history),20):
    fig, axarr = plt.subplots(2, figsize=(5,8))
    for axon in axons:
      add_post_synapses_to_axarr_by_axon(axon, axarr, i, retino.TECTUM_WIDTH, retino.TECTUM_HEIGHT, size=20)
    tm = axons[0].history[i][0]
    dots_index = tm % len(dots_origins)
    axarr[0].set_title("Labelled Synapses by Gradient Along X")
    axarr[1].set_title("Labelled Synapses by Gradient Along Y")
    for ax in axarr:
      ax.set_aspect(1)
      ax.set_xlim([0,retino.TECTUM_WIDTH])
      ax.set_ylim([0,retino.TECTUM_HEIGHT])
    plt.tight_layout()
    plt.savefig(output_directory + "/AllSynapsesColoredByTarget-" + str(i) + ".png", dpi=200)
    plt.close(fig)

    fig, axarr = plt.subplots(2)
    for axon in axons:
      add_average_post_synapse_to_axarr_by_axon(axon, axarr, i, retino.TECTUM_WIDTH, retino.TECTUM_HEIGHT)
    tm = axons[0].history[i][0]
    dots_index = tm % len(dots_origins)
    axarr[0].set_title("Labelled Average Synapse by Gradient Along X")
    axarr[1].set_title("Labelled Average Synapse by Gradient Along Y")
    for ax in axarr:
      ax.set_aspect(1)
      ax.set_xlim([0,retino.TECTUM_WIDTH])
      ax.set_ylim([0,retino.TECTUM_HEIGHT])
    plt.tight_layout()
    plt.savefig(output_directory + "/AverageSynapsesColoredByTarget-" + str(i) + ".png", dpi=200)
    plt.close(fig)

produce_axon_growth_accuracy_demos_with_postsynapse_coloring()
