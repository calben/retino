import retino

class RetinoModelHistoryItem(object):

  def __init__(self):
    axon_table = []
    postsynapse_table = []
    synapse_table = []


class RetinoModel(object):

  def __init__(self, targets=None, target_noise = 1):

    axon_table = []
    postsynapse_table = []
    synapse_table = []

    if(targets == None):
      targets = add_jitter_to_points([np.asarray([retino.TECTUM_SIZE_X/2.0, retino.TECTUM_SIZE_Y/2.0])] * retino.NUMBER_OF_AXONS, 
        (retino.TECTUM_SIZE_X + retino.TECTUM_SIZE_Y)/8)

    

    for i in range(0, len(targets))

