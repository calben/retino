import numpy as np

from unittest import TestCase

import retino
from retino.utils import *


class TestUtils(TestCase):
    def test_generate_evenly_spaced_grid(self):
        points = np.asarray([[6.25, 6.25],
                             [6.25, 31.25],
                             [6.25, 56.25],
                             [6.25, 81.25],
                             [31.25, 6.25],
                             [31.25, 31.25],
                             [31.25, 56.25],
                             [31.25, 81.25],
                             [56.25, 6.25],
                             [56.25, 31.25],
                             [56.25, 56.25],
                             [56.25, 81.25],
                             [81.25, 6.25],
                             [81.25, 31.25],
                             [81.25, 56.25],
                             [81.25, 81.25]])
        result = generate_evenly_spaced_grid(0, 100, 0, 100, 4)
        assert (np.all(points - result) == False)

    def test_generate_random_points_distribution_in_space(self):
        points = generate_random_points_distribution_in_space(0,100,0,100, 10)
        print(points)
        assert(True)
