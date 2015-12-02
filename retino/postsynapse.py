from retino.retinoutil import *
import numpy as np

class PostSynapse(object):

  def __init__(self, id, origin=None, size=10, tectum_length = 0, tectum_width = 0):
    self.origin = origin
    self.id = id
    if(self.origin == None):
      self.origin = produce_bounded_random_point(tectum_length, tectum_width)
    self.size = size
    self.activity = 0
    self.synapses = []

  def fire(self, amount):
    self.activity += amount
#    if(self.activity > 1.0):
#      for c in self.synapses:
#        c.send_stabiliser(3.0)

  def flat_line(self):
    self.activity = 0.0

  def add_postsynapticconnecion(self, connection):
    self.synapses.append(connection)
