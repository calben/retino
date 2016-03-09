import os
import numpy as np
import pandas as pd

from retino.axon import Axon
from retino.plot import plot_model_summary, plot_model_axons
from retino.postsynapticcell import PostSynapticCell
from retino.utils import generate_jittered_points_on_grid

import retino
import pickle
import time
import pprint

pp = pprint.PrettyPrinter(indent=2)


class Model(object):
    def __init__(self, targets=None, name="", axons=None, postsynapticcells=None, synapses=None):
        self.timestamp = str(time.strftime("%y-%m-%d %H-%M-%S"))
        self.name = name
        self.targets = targets
        self.axons = axons
        self.postsynapticcells = postsynapticcells
        self.synapses = synapses
        self.metadata = {}
        self.iteration = 0
        for k, v in retino.__dict__.items():
            # WARNING: HACK
            # Isolates global vars by checking if uppercase
            if k.isupper():
                self.metadata[k] = v

        if self.targets is None:
            self.targets = generate_jittered_points_on_grid(0, retino.TECTUM_SIZE_X, 0,
                                                            retino.TECTUM_SIZE_Y, retino.AXON_COUNT_SQRT,
                                                            (retino.TECTUM_SIZE_X + retino.TECTUM_SIZE_Y) \
                                                            / retino.AXON_COUNT_SQRT ** 3)
        else:
            self.targets = targets

        if self.axons is None:
            self.axons = [Axon(self, id=i, target=self.targets[i]) for i in range(len(self.targets))]
        else:
            self.axons = axons

        if self.postsynapticcells is None:
            if retino.ORDERED_RANDOM_POSTSYNAPTICCELL_ORIGINS:
                points = generate_jittered_points_on_grid(0, retino.TECTUM_SIZE_X, 0, retino.TECTUM_SIZE_Y,
                                                          retino.POSTSYNAPTIC_COUNT_SQRT,
                                                          (retino.TECTUM_SIZE_X - 0 + retino.TECTUM_SIZE_Y - 0) /
                                                          retino.POSTSYNAPTIC_COUNT_SQRT ** 2)
                self.postsynapticcells = []
                for i in range(0, len(points)):
                    self.postsynapticcells.append(
                            (PostSynapticCell(i, size=retino.POSTSYNAPTIC_RADIUS, origin=points[i])))
            else:
                self.postsynapticcells = []
                for i in range(0, len(targets)):
                    self.postsynapticcells.append(
                            PostSynapticCell(i, size=retino.POSTSYNAPTIC_RADIUS, origin=self.targets[i]))
        else:
            self.postsynapticcells = postsynapticcells

        if self.synapses is None:
            self.synapses = []
        self.activities_df = pd.DataFrame(0, index=np.arange(100), columns=np.arange(100))
        retino.MODEL = self

    def iterate(self, write_to_disk=True, plot_model_axons_to_disk=False, plot_overview_to_disk=False, activities_df=None):
        print("Running model iteration " + str(self.iteration))
        if activities_df is not None:
            self.activities_df = activities_df
            for axon in self.axons:
                df_index = axon.target.astype(np.int)
                if activities_df.ix[df_index[0], df_index[1]] == 1:
                    axon.fire()
        else:
            self.activities_df = pd.DataFrame(0, index=np.arange(100), columns=np.arange(100))
        for axon in self.axons:
            axon.tick()
        for postsynapticcell in self.postsynapticcells:
            postsynapticcell.tick()
        if write_to_disk:
            if not os.path.exists("models/" + self.timestamp):
                os.makedirs("models/" + self.timestamp)
            self.dump("models/" + self.timestamp + "/" + str(self.iteration) + ".pickle")
        if plot_overview_to_disk:
            os.makedirs("models/" + self.timestamp, exist_ok=True)
            plot_model_summary(self, "models/" + self.timestamp + "/" + str(self.iteration))
        if plot_model_axons_to_disk:
            os.makedirs("models/" + self.timestamp, exist_ok=True)
            plot_model_axons(self, "models/" + self.timestamp + "/" + str(self.iteration))
        self.iteration += 1

    def dump(self, location):
        with open(location, 'wb') as f:
            pickle.dump(self, f)

    @property
    def postsynapticcell_mapping_score(self):
        errors = []
        for postsynapticcell in self.postsynapticcells:
            mapping = postsynapticcell.get_average_mapping()
            if mapping[0] is not -1:
                errors.append(np.sum(np.abs(postsynapticcell.origin - mapping)))
        return np.average(errors)

    def __repr__(self):
        return (pp.pformat(vars(self)))
