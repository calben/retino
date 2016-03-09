TECTUM_SIZE_X = 100.0
TECTUM_SIZE_Y = 100.0

# the number of axons in the model (note this is a sqrt)
AXON_COUNT_SQRT = 10

# minimum distance from a target an axon can be considered to have
# used to avoid some algorithms dividing by very small values
AXON_MINIMUM_DISTANCE_FROM_TARGET = 4.0

# maximum activation for an axon, determines how long an axon remains fired
AXON_MAXIMUM_ACTIVITY = 2.25

# how much activation means an axon is "fired"
AXON_ACTIVITY_FIRED_THRESHHOLD = 1.0

# average length of each axon segment, higher is less accurate but faster to run, recommend 1 to 3
AXON_SEGMENT_LENGTH_AVG = 2

# determines how much noise to add to segment length, recommend 0.2 to 0.8
AXON_SEGMENT_LENGTH_STD = 0.5

# determines how much noise is added to the growth direction
AXON_SEGMENT_GROWTH_DIRECTION_NOISE_STD = 1.0

# number of synapses attempted per segment grown
AXON_SEGMENT_SYNAPSE_COUNT = 1

# number of points generated along the segment to choose from for growing the synapse
AXON_SEGMENT_SYNAPSE_POOL_COUNT = 3

# amount of jitter to apply to the synapse position- mostly for plotting purposes
AXON_SEGMENT_SYNAPSE_JITTER_STD = 0.4

# amount to destabilise every segment per tick
AXON_SEGMENT_DESTABILISATION_FACTOR = 1

# amount to stabilise all the segments up the tree when a segment grows
AXON_SEGMENT_GROWTH_STABILISATION_FACTOR = 3

####

# IF True then axon growth targeting by gradient will be reduced when an axon
# is growing within some radius of the target
GRADIENT_REDUCED_TARGETING_BY_THRESHOLD = False
GRADIENT_REDUCED_TARGETING_K = 30
GRADIENT_REDUCED_TARGETING_H = 5
GRADIENT_REDUCED_TARGETING_BASE = 0.2

# IF targeting is limited by a threshold, determines the radius around the target this takes effect
GRADIENT_ACCURACY_THRESHHOLD = 10.0

GRADIENT_REDUCED_TARGETING_BY_DISTANCE = True

####

# sqrt number of how many post synaptic cells should be included in the model
POSTSYNAPTIC_COUNT_SQRT = 20

# IF True, post synaptic cells   will be lined up directly with the growing axon
POSTSYNAPTICCELLS_ON_TARGETS = True

# IF True, post synaptic cells will be in a semi-random grid
ORDERED_RANDOM_POSTSYNAPTICCELL_ORIGINS = True

# size of post synapses by radius
POSTSYNAPTIC_RADIUS = 10

POSTSYNAPTIC_CELL_FIRED_THRESHOLD = 1.0

POSTSYNAPTICCELL_MAX_ACTIVITY = 1.75

ACTIVITY_LOSS_FACTOR = 0.25
RETROGRADE_SIGNAL_LOSS_FACTOR = 0.25

DESIRED_DIRECTION_WEIGHT = 0.8
REDUCED_DESIRED_DIRECTION_WEIGHT = 0.3
MOMENTUM_DIRECTION_WEIGHT = 1.0

RANDOM_ORIGIN_NODE_BETA = 20
RANDOM_ORIGIN_NODE_ALPHA = 1

ASYNCHRONOUS_STIMULATION_GROWTH_RATE = 0.16
ASYNCHRONOUS_STIMULATION_LOSS_RATE = 0.14
SYNCHRONOUS_STIMULATION_GROWTH_RATE = 0.13
SYNCHRONOUS_STIMULATION_LOSS_RATE = 0.12
NO_STIMULATION_GROWTH_RATE = 0.13
NO_STIMULATION_LOSS_RATE = 0.09

SYNAPSE_ACTIVITY_TRANSFER_MULTIPLIER = 0.003
SYNAPSE_RETROGRADE_SIGNAL_THRESHOLD = 5.0
AXON_SEGMENT_GO_AWAY_SIGNAL_THRESHOLD = 10.0

MODEL_ITERATION_GRANULARITY = 5

SYNAPSE_ATTEMPT_GOLDILOCKS_RADIUS = 100.0

MODEL = None

DEBUG = False