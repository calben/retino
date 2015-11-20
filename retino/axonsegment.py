import numpy as np
import pandas as pd

class AxonSegment(object):

  def __init__(self, id, parent, owner, origin=np.array([0.0,0.0]), end=np.array([0.0,0.0]), stability=5):
    self.id = id
    self.parent = parent
    self.owner = owner
    self.origin = origin
    self.end = end
    self.stability = stability
    self.activity = 0
    self.synapses = []
    self.children = []
    if(parent != None):
      parent.add_child(self)

  def add_child(self, axon_segment):
    self.children.append(axon_segment)

  def add_synapse(self, connection):
    self.synapses.append(connection)

  def grow(self, id, owner, target, post_synapses):
    new_segment_origin = self.end

    desired_direction_weight = 1.1
    momentum_direction_weight = 1
    desired_direction = get_unit_direction_vector(new_segment_origin, target)
    momentum_direction = get_unit_direction_vector(self.origin, self.end)
    desired_and_momentum = desired_direction_weight * desired_direction + momentum_direction_weight * momentum_direction
    desired_and_momentum = get_unit_vector(desired_and_momentum)
    prenoise_pol = cart_to_pol(desired_and_momentum)[1]

    r = np.random.normal(3.0,0.5, size=1)[0]
    noise = np.random.normal(0,.8,size=1)[0]
    theta = prenoise_pol + noise
    cart_result = pol_to_cart(np.asarray([r,theta]))

    new_segment_end = new_segment_origin + cart_result

    new_segment = AxonSegment(id, self, owner, origin=new_segment_origin, end=new_segment_end)
    if(np.linalg.norm(new_segment.end - target) < 15):
      new_segment.grow_post_synaptic_connections(post_synapses)
    owner.add_segment(new_segment)

  def grow_post_synaptic_connections(self, post_synapses):
    origins = generate_random_points_along_line(self.origin, cart_to_pol(self.end - self.origin), 100, 5)
    for origin in origins:
      i = choose_random_circle_as_connection_index(origin, [p.origin for p in post_synapses], 
        [p.size for p in post_synapses])
      if(i != None):
        connection = synapse(i, self, post_synapses[i], origin=origin)
        self.synapses.append(connection)
        self.owner.add_synapse(connection)

  def destabilise(self):
    self.stability -= 1
    if(self.stability <= 0):
      self.owner.segments.remove(self)
      [self.owner.synapses.remove(c) for c in self.synapses]

  def stabilise(self, amount):
    self.stability += amount
    if(self.parent != None):
      self.parent.stabilise(amount)

  def propagate_activity(self, amount):
    self.activity += amount
    if(self.parent != None):
      self.parent.propagate_activity(amount)

  def send_activity(self, amount):
    self.activity += amount
    for connection in self.synapses:
      connection.postsynapse.fire(amount)
    for child in self.children:
      child.send_activity(amount)

  def __repr__(self):
    items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
    return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

