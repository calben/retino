from retino.utils import produce_bounded_random_point
import retino
import numpy as np


class PostSynapticCell(object):
    def __init__(self, id, origin=None, size=retino.POSTSYNAPTIC_RADIUS, tectum_size_x=retino.TECTUM_SIZE_X,
                 tectum_size_y=retino.TECTUM_SIZE_Y):
        self.origin = origin
        self.id = id
        if (self.origin is None):
            self.origin = produce_bounded_random_point(tectum_size_x, tectum_size_y)
        self.size = size
        self.activity = 0
        self.synapses = []

    def is_fired(self):
        return self.activity >= retino.POSTSYNAPTIC_CELL_FIRED_THRESHOLD

    def fire(self, amount):
        self.activity += amount
        if self.activity > retino.POSTSYNAPTICCELL_MAX_ACTIVITY:
            self.activity = retino.POSTSYNAPTICCELL_MAX_ACTIVITY

    def flat_line(self):
        self.activity = 0.0

    def tick(self):
        self.activity = self.activity - retino.ACTIVITY_LOSS_FACTOR
        if self.activity < 0.0:
            self.activity = 0.0

    def get_average_mapping(self):
        if len(self.synapses) is 0:
            return np.asarray([-1, -1])
        origins = []
        for synapse in self.synapses:
            origins.append(synapse.axonsegment.owner.target)
        return np.asarray(
                [np.average(list(map(lambda x: x[0], origins))), np.average(list(map(lambda x: x[1], origins)))])
