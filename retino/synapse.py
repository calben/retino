from retino import *

class synapse(object):

  def __init__(self, id, axonsegment, postsynapse, origin=None, size=1):
    self.origin = origin
    self.id = id
    self.axonsegment = axonsegment
    self.postsynapse = postsynapse
    self.size = size
    self.activity = 0
    self.stability = 50

  def fire(self, amount):
    self.activity += amount
    self.axonsegment.propagate_activity(amount)
    if(self.activity > 1):
      self.stability = self.stability + 0.2

  def degrade(self, amount):
    self.stability = self.stability - amount
    if self.stability <= 0:
      self.axonsegment.synapses.remove(self)
      self.axonsegment.owner.synapses.remove(self)
      self.postsynapse.synapses.remove(self)

  def flat_line(self):
    self.activity = 0.0
