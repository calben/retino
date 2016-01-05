from retino import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
import time
import seaborn as sns

sns.set_style("darkgrid")

def produce_axon_interaction_demos_with_postsynapse_coloring(AXON_SEGMENT_LENGTH_AVG, AXON_SEGMENT_LENGTH_STD, AXON_SEGMENT_NOISE_STD, AXON_SEGMENT_SYNAPSE_COUNT, AXON_SEGMENT_SYNAPSE_POOL_COUNT, AXON_SEGMENT_SYNAPSE_JITTER_STD):
  
  retino.AXON_SEGMENT_LENGTH_AVG         = AXON_SEGMENT_LENGTH_AVG        
  retino.AXON_SEGMENT_LENGTH_STD         = AXON_SEGMENT_LENGTH_STD        
  retino.AXON_SEGMENT_NOISE_STD          = AXON_SEGMENT_NOISE_STD         
  retino.AXON_SEGMENT_SYNAPSE_COUNT      = AXON_SEGMENT_SYNAPSE_COUNT     
  retino.AXON_SEGMENT_SYNAPSE_POOL_COUNT = AXON_SEGMENT_SYNAPSE_POOL_COUNT
  retino.AXON_SEGMENT_SYNAPSE_JITTER_STD = AXON_SEGMENT_SYNAPSE_JITTER_STD

  targets = add_jitter_to_points([np.asarray([50.0,50.0])] * 30, 10) 

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
  
  for i in range(200,800):
    t = time.time()
    for axon in axons:
      dots_index = i % len(dots_origins)
      activity = 0
      if(is_point_within_circle(axon.target, dots_origins[dots_index], dots_sizes[dots_index])):
        activity = 0.3
      axon.grow_cycle(time=i, post_synapses=post_synapses, activity=activity)
      total_error = np.nanmean([get_average_point_error(a.target, [p.origin for p in a.synapses]) for a in axons])
    print("Finished cycle", i, "in", time.time() - t, "s.", " Total score", total_error)
    average_points_error_f.write(",".join([str(get_average_point_error(a.target, [p.origin for p in a.synapses])) for a in axons]) + "\n")


  for i in range(200,len(axons[0].history),20):
    fig, axarr = plt.subplots(2)
    for axon in axons:
      add_post_synapses_to_axarr_by_axon(axon, axarr, i, retino.TECTUM_WIDTH, retino.TECTUM_HEIGHT)
    tm = axons[0].history[i][0]
    dots_index = tm % len(dots_origins)
    axarr[0].set_title("Labelled Synapses by Gradient Along X")
    axarr[1].set_title("Labelled Synapses by Gradient Along Y")
    for ax in axarr:
      ax.set_aspect(1)
      ax.set_xlim([0,retino.TECTUM_WIDTH])
      ax.set_ylim([0,retino.TECTUM_HEIGHT])
      ax.add_collection(EllipseCollection(widths=dots_sizes[dots_index], heights=[dots_sizes[dots_index]], angles=0, units='xy',
             facecolors='b',
             offsets=dots_origins[dots_index], transOffset=ax.transData, alpha=0.1))
    plt.tight_layout()
    output_directory = "Plots/synapsesInteractions" 
    if not os.path.exists(output_directory):
      os.makedirs(output_directory)
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
      ax.add_collection(EllipseCollection(widths=dots_sizes[dots_index], heights=[dots_sizes[dots_index]], angles=0, units='xy',
             facecolors='b',
             offsets=dots_origins[dots_index], transOffset=ax.transData, alpha=0.1))
    plt.tight_layout()
    output_directory = "Plots/synapsesInteractions" 
    if not os.path.exists(output_directory):
      os.makedirs(output_directory)
    plt.savefig(output_directory + "/AverageSynapsesColoredByTarget-" + str(i) + ".png", dpi=200)
    plt.close(fig)

if __name__ == '__main__':
  
  TECTUM_HEIGHT = 100 
  TECTUM_WIDTH = 100
  AXON_SEGMENT_LENGTH_AVG = range(1, 8, 1)
  AXON_SEGMENT_LENGTH_STD = range(0.1, 0.6, 0.1)
  AXON_SEGMENT_NOISE_STD = range(0.2, 1.2, 0.2)
  AXON_SEGMENT_SYNAPSE_COUNT = range(1, 10, 2)
  AXON_SEGMENT_SYNAPSE_POOL_COUNT = range(2, 22, 5)
  AXON_SEGMENT_SYNAPSE_JITTER_STD = range(0.1, 1.1, 0.1)
  NUMBER_OF_AXONS = 10
  NUMBER_OF_POSTSYNAPTIC_NEURONS = 50

  for a in AXON_SEGMENT_LENGTH_AVG:
    for b in AXON_SEGMENT_LENGTH_STD:
      for c in AXON_SEGMENT_NOISE_STD:
        for d in AXON_SEGMENT_SYNAPSE_COUNT:
          for e in AXON_SEGMENT_SYNAPSE_POOL_COUNT:
            for f in AXON_SEGMENT_SYNAPSE_JITTER_STD:
              p = Process(target=produce_axon_interaction_demos_with_postsynapse_coloring, args=(a,b,c,d,e,f,))
              p.start()
              print("Started process for iterative parameter testing")
