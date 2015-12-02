import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
from retino.retinoutil import *

def convert_post_synapse_activity_to_rgb(activity):
  if(activity > .5):
    return [1]*3
  else:
    return [.2 + activity]*3

def convert_activity_to_rgb(activity):
  if(activity > .4):
    return [0]*3
  else:
    return [.4 - activity]*3

def plot_post_synapses(output_file, post_synapses):
  fig, ax = plt.subplots(1, figsize=(8,6), facecolor="#D6D6D6")
  ax.set_axis_bgcolor("#242424")
  colors = [convert_post_synapse_activity_to_rgb(x.activity) for x in post_synapses]
  sizes = [x.size * 50 for x in post_synapses]
  offsets = [(x.origin[0],x.origin[1]) for x in post_synapses]
  ax.scatter([x.origin[0] for x in post_synapses], [x.origin[1] for x in post_synapses], 
    color=colors, s=sizes, alpha=0.3)
  plt.savefig(output_file)
  plt.close(fig)

def add_post_synapses_to_axis(post_synapses, ax):
  sizes = [x.size * 50 for x in post_synapses]
  offsets = [(x.origin[0],x.origin[1]) for x in post_synapses]
  colors = [convert_post_synapse_activity_to_rgb(x.activity) for x in post_synapses]
  ax.scatter([x.origin[0] for x in post_synapses], [x.origin[1] for x in post_synapses], 
    color=colors, s=sizes, alpha=0.3)


def add_axon_to_axis(axon, ax):
  colors = [convert_activity_to_rgb(segment.activity) for segment in axon.segments]
  line_collection = mc.LineCollection(segments_to_lines(axon.segments), colors=list(colors), linewidths=3, alpha=.6)
  ax.add_collection(line_collection)
  ax.scatter(axon.target[0], axon.target[1], s=40, color="y")

def add_axon_postsynapse_connection_to_axis(axon, ax, index, tectum_length, tectum_width):
  color = postsynapse_color_for_axon(axon, index, tectum_length if index == 0 else tectum_width)

def convert_ndpoint_to_gradients(point, bounds):
  colors = [convert_linepoint_to_gradient_color(point[i], "rainbow", bounds[i]) for i in range(len(point))]
  return colors

def convert_linepoint_to_gradient_color(position, colormap_name, bound):
  cmap = plt.get_cmap(colormap_name)
  return cmap(position/bound)

def plot_axon_growth(axon, output_directory, xlim, ylim, granularity=1):
    output_directory = output_directory + "/AXON-id=" + str(axon.id) + "-target=" + str(axon.target)
    if not os.path.exists(output_directory):
      os.makedirs(output_directory)
    for history in axon.history[::granularity]:
      time = history[0]
      lines = history[1]
      activities = history[2]
      number = "%04d" % time
      fig, ax = plt.subplots(1, figsize=(8,6))
      colors = [convert_activity_to_rgb(activity) for activity in activities]
      line_collection = mc.LineCollection(lines, colors=list(colors), linewidths=2, alpha=.8)
      ax.add_collection(line_collection)
      ax.scatter(axon.target[0], axon.target[1], s=20, c="r")
      ax.set_xlim([0,xlim])
      ax.set_ylim([0,ylim])
      ax.set_aspect(xlim/ylim)
      plt.tight_layout()
      plt.savefig(output_directory + "/" + number + ".png", dpi=100, pad_inches=0)
      plt.close(fig)

def add_post_synapses_to_axarr_by_axon(axon, axarr, time, xlim, ylim):
  history = axon.history[time]
  points = history[3]
  colors = convert_ndpoint_to_gradients(axon.target, [xlim, ylim])
  for i in range(len(axarr)):
    axarr[i].scatter([p[0] for p in points], [p[1] for p in points],
    color = colors[i], s=5, alpha=.4)

def add_average_post_synapse_to_axarr_by_axon(axon, axarr, time, xlim, ylim):
  history = axon.history[time]
  points = history[3]
  p = get_average_of_points(points)
  colors = convert_ndpoint_to_gradients(axon.target, [xlim, ylim])
  for i in range(len(axarr)):
    axarr[i].scatter(p[0],p[1],
    color = colors[i], s=5, alpha=.4)
