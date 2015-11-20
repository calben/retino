import retino.retinoutil
from retino.axonsegment import *

import numpy as np
import os
import subprocess

class Axon(object):

  branching_stabilisation = 8
  tectum_length = 300.0
  tectum_width = 100.0

  def __init__(self, id=None, target=np.array([0.0,0.0])):
    self.id = id
    self.target = target
    self.segments = []
    self.synapses = []
    if(len(self.segments) == 0):
      origin = None
      if(target[1] > Axon.tectum_width/2):
        origin = np.array([0.0,Axon.tectum_width/2 + target[1]/15])
      else:
        origin = np.array([0.0,Axon.tectum_width/2 - target[1]/15])
      self.segments.append(AxonSegment(self.id * 10000, None, self, origin=origin, end=np.add(origin, np.array([0.1, 0.1]))))

    self.history = []
    self.growth_rate = 1

  def add_segment(self, segment):
    self.segments.append(segment)

  def add_synapse(self, connection):
    self.synapses.append(connection)

  def grow_cycle(self, time, post_synapses, activity = 0.0):
    for i in range(self.growth_rate):
      current_lines = [[tuple(segment.origin), tuple(segment.end)] for segment in self.segments]
      line_activities = [segment.activity for segment in self.segments]
      synapses_points = [p.origin for p in self.synapses]
      synapses_activities = [p.activity for p in self.synapses]
      self.history.append([time, current_lines, line_activities, synapses_points, synapses_activities])
      for segment in self.segments:
        segment.destabilise()
      self.grow(time, post_synapses)
      self.segments[0].send_activity(activity)

  def flat_line(self):
    for segment in self.segments:
      segment.activity = 0

  def grow(self, time, post_synapses):
    segment_of_origin = self.segments[select_item_from_list_by_beta_distribution(len(self.segments), 8, 1)]
    segment_of_origin.stabilise(Axon.branching_stabilisation)
    segment_of_origin.grow(self.segments[-1].id + 1, self, self.target, post_synapses)

  def __repr__(self):
    items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
    return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

