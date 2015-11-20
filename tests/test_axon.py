from retino.axon import *

import numpy as np

axon = Axon(id=0)
  
def test_add_segment():
  count = len(axon.segments)
  axon.add_segment(AxonSegment(0, axon.segments[0], axon))
  assert(len(axon.segments) - count == 1)
