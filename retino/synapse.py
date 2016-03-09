import retino
import gc


class Synapse(object):
    def __init__(self, id, axonsegment, postsynapse, origin=None, size=1):
        self.origin = origin
        self.id = id
        self.axonsegment = axonsegment
        self._postsynapticcell = postsynapse
        self.size = size
        self.stability = 50

    def postsynapticcell(self):
        return self.axonsegment.owner.model.postsynapticcells[self._postsynapticcell]

    def notify_fired(self, amount):
        self.postsynapticcell().fire(amount * retino.SYNAPSE_ACTIVITY_TRANSFER_MULTIPLIER)

    def destabilise_synapse(self, amount):
        self.stability = self.stability - amount
        if self.stability <= 0:
            self.axonsegment.synapses.remove(self)
            self.axonsegment.owner.synapses.remove(self)
            self.postsynapticcell().synapses.remove(self)
            self.axonsegment = None

    def tick(self):
        self.retrograde_signal = self.retrograde_signal - retino.RETROGRADE_SIGNAL_LOSS_FACTOR
