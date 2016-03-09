import numpy as np
import retino
from retino.synapse import Synapse
from retino.utils import get_unit_direction_vector, get_unit_vector, cart_to_pol, pol_to_cart, \
    select_item_from_list_by_beta_distribution, generate_random_points_along_line, \
    choose_random_circle_as_connection_index, rising_hill_function
import sys
import gc


class Axon(object):
    def __init__(self, model, id=None, target=np.array([0.0, 0.0]), fake_target=None):
        self.model = model
        self.id = id
        self.target = target
        self.fake_target = fake_target
        self.use_fake_target = True if fake_target is not None else False
        self.segments = []
        self.synapses = []
        self.activity = 0

        if (len(self.segments) == 0):
            midpoint = retino.TECTUM_SIZE_Y / 2
            origin = np.asarray([0.0, midpoint + target[1] / 15]) if target[1] > midpoint \
                else np.asarray([0.0, midpoint - target[1] / 15])
            self.segments.append(AxonSegment(self.id * 10000, None, self, origin=origin,
                                             end=np.add(origin, np.array([0.1, 0.1])), branch_number=0))

        self.growth_rate = 1
        self.distance_of_branch_closest_to_target = 1000

    def grow(self):
        if retino.DEBUG:
            print("Grow cycle for", self.id)
        for i in range(self.growth_rate * retino.MODEL_ITERATION_GRANULARITY):
            segment_of_origin = self.segments[
                select_item_from_list_by_beta_distribution(len(self.segments), retino.RANDOM_ORIGIN_NODE_BETA -
                                                           (
                                                               retino.RANDOM_ORIGIN_NODE_BETA / self.distance_of_branch_closest_to_target),
                                                           retino.RANDOM_ORIGIN_NODE_ALPHA)]
            segment_of_origin.stabilise_axonsegment(retino.AXON_SEGMENT_GROWTH_STABILISATION_FACTOR)
            segment_of_origin.extend_new_segment(self.segments[-1].id + 1, self, self.get_current_targeting())
            if not segment_of_origin.stability > self.segments[-1].stability:
                print("Origin stability", segment_of_origin.stability, "child stability", self.segments[-1].stability)
            if (np.linalg.norm(
                        self.segments[
                            -1].origin - self.get_current_targeting()) < self.distance_of_branch_closest_to_target):
                self.distance_of_branch_closest_to_target = np.linalg.norm(
                        self.segments[-1].origin - self.get_current_targeting())
                if self.distance_of_branch_closest_to_target < retino.AXON_MINIMUM_DISTANCE_FROM_TARGET:
                    self.distance_of_branch_closest_to_target = retino.AXON_MINIMUM_DISTANCE_FROM_TARGET

    def get_current_targeting(self):
        if self.use_fake_target:
            return self.fake_target
        else:
            return self.target

    def fire(self, activity=retino.AXON_MAXIMUM_ACTIVITY):
        self.activity = activity
        self.segments[0].fire(activity)

    def tick(self):
        self.grow()
        self.segments[0].destabilise_axonsegment()
        self.activity -= retino.ACTIVITY_LOSS_FACTOR
        if self.activity < 0.0:
            self.activity = 0.0


class AxonSegment(object):
    def __init__(self, id: int, parent, owner, origin=np.array([0.0, 0.0]),
                 end=np.array([0.0, 0.0]), branch_number=-1,
                 stability=retino.AXON_SEGMENT_GROWTH_STABILISATION_FACTOR):
        self.id = id
        self.parent = parent
        self.owner = owner
        self.origin = origin
        self.end = end
        self.stability = stability
        self.branch_number = branch_number
        self.synapses = []
        self.children = []
        if parent is not None:
            parent.children.append(self)
        self.go_away_signal = 0.0

    def is_going_away(self):
        return self.go_away_signal > retino.AXON_SEGMENT_GO_AWAY_SIGNAL_THRESHOLD

    def calculate_desired_and_momentum_weights(self, distance):
        desired_weight = 0.0 if self.is_going_away() else retino.DESIRED_DIRECTION_WEIGHT
        momentum_weight = 0.6 if self.is_going_away() else retino.MOMENTUM_DIRECTION_WEIGHT
        if self.is_going_away():
            if retino.GRADIENT_REDUCED_TARGETING_BY_DISTANCE:
                momentum_weight = rising_hill_function(distance, retino.GRADIENT_REDUCED_TARGETING_K,
                                                       retino.GRADIENT_REDUCED_TARGETING_H) + \
                                  retino.GRADIENT_REDUCED_TARGETING_BASE
            elif retino.GRADIENT_REDUCED_TARGETING_BY_THRESHOLD and distance < retino.GRADIENT_ACCURACY_THRESHHOLD:
                momentum_weight = retino.REDUCED_DESIRED_DIRECTION_WEIGHT
        return desired_weight, momentum_weight

    def extend_new_segment(self, id: int, owner: Axon, target: np.ndarray):
        new_segment_origin = self.end

        distance_from_target = np.linalg.norm(new_segment_origin - owner.target)
        desired_weight, momentum_weight = self.calculate_desired_and_momentum_weights(distance_from_target)

        desired_direction = get_unit_direction_vector(new_segment_origin, target)
        momentum_direction = get_unit_direction_vector(self.origin, self.end)
        desired_and_momentum = desired_weight * desired_direction + momentum_weight * momentum_direction
        unit_desired_and_momentum = get_unit_vector(desired_and_momentum)
        prenoise_pol = cart_to_pol(unit_desired_and_momentum)[1]

        r = np.random.normal(retino.AXON_SEGMENT_LENGTH_AVG, retino.AXON_SEGMENT_LENGTH_STD, size=1)[0]
        noise = np.random.normal(0, retino.AXON_SEGMENT_GROWTH_DIRECTION_NOISE_STD, size=1)[0]
        if self.is_going_away():
            self.noise = np.random.normal(0, 2, size=1)[0]
        theta = prenoise_pol + noise
        cart_result = pol_to_cart(np.asarray([r, theta]))

        new_segment_end = new_segment_origin + cart_result

        new_segment = AxonSegment(id, self, owner, origin=new_segment_origin, end=new_segment_end)
        if np.linalg.norm(new_segment.end - target) < retino.SYNAPSE_ATTEMPT_GOLDILOCKS_RADIUS:
            if owner.model is not None:
                new_segment.attempt_synapses()
        owner.segments.append(new_segment)

    def attempt_synapses(self):
        postsynapticcells = self.owner.model.postsynapticcells
        origins = generate_random_points_along_line(self.origin, cart_to_pol(self.end - self.origin),
                                                    retino.AXON_SEGMENT_SYNAPSE_POOL_COUNT,
                                                    retino.AXON_SEGMENT_SYNAPSE_COUNT,
                                                    retino.AXON_SEGMENT_SYNAPSE_JITTER_STD)
        for origin in origins:
            i = choose_random_circle_as_connection_index(origin, [p.origin for p in postsynapticcells],
                                                         [p.size for p in postsynapticcells])
            if i is not None:
                connection = Synapse(i, self, i, origin=origin)
                self.synapses.append(connection)
                self.owner.synapses.append(connection)
                postsynapticcells[i].synapses.append(connection)

    def destabilise_axonsegment(self, amount=retino.AXON_SEGMENT_DESTABILISATION_FACTOR):
        self.stability -= amount
        if (self.stability <= 0):
            if self.children:
                raise ValueError("Why does an axon segment that's being destroyed have children?")
            self.owner.segments.remove(self)
            self.parent.children.remove(self)
            for s in self.synapses:
                s.destabilise_synapse(99)
        for child in self.children:
            child.destabilise_axonsegment(amount)

    def stabilise_axonsegment(self, amount):
        self.stability += amount
        if (self.parent != None):
            self.parent.stabilise_axonsegment(amount)

    def fire(self, activity):
        for synapse in self.synapses:
            synapse.notify_fired(activity)
        for segment in self.children:
            segment.fire(activity)
