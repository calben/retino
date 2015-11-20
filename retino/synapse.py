import retino.postsynapse
import retino.axonsegment

class synapse(object):

  def __init__(self, id, axonsegment, postsynapse, origin=None, size=1):
    self.origin = origin
    self.id = id
    self.axonsegment = axonsegment
    self.postsynapse = postsynapse
    self.size = size
    self.activity = 0
    self.stability = 10

  def fire(self, amount):
    self.activity += amount
    self.axonsegment.propagate_activity(amount)

  def flat_line(self):
    self.activity = 0.0
