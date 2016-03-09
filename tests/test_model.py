from unittest import TestCase

import retino
import pickle
import numpy as np
import pandas as pd
import sys

from retino.model import Model
from retino.utils import *
from retino.postsynapticcell import PostSynapticCell


class TestModel(TestCase):
    def test_dump(self):
        model = Model()
        model.dump("model.pickle")
        with open("model.pickle", 'rb') as f:
            assert (len(pickle.load(f).axons) is retino.AXON_COUNT_SQRT ** 2)

    def test_iterate(self):
        # model = Model(targets=[np.asarray([60.0, 50.0])])
        model = Model()
        # model = Model(postsynapticcells=[PostSynapticCell(1, size=100, origin=np.asarray([50.0, 50.0]))])
        for i in range(400):
            if i % 10 == 0:
                if i % 20 == 0:
                    activities_df = pd.DataFrame(0, index=np.arange(100), columns=np.arange(100))
                    activities_df.ix[i-5 % 1000:i+5 % 1000] = 1
                    model.iterate(plot_overview_to_disk=True, activities_df=activities_df)
                else:
                    model.iterate(plot_overview_to_disk=True)
            else:
                model.iterate(write_to_disk=False)
            print("Model Score", model.postsynapticcell_mapping_score)
        assert (len(model.axons[0].segments) > 1)

    def test_default_targets(self):
        model = Model()
        print(model)
        assert (True)
