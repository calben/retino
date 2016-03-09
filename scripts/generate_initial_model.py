import retino
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

from retino.model import Model
from retino.utils import *
from retino.postsynapticcell import PostSynapticCell

sys.setrecursionlimit(1500)

info = pd.DataFrame({"PSC Mapping Score": []})
info.index.name = "Iteration"

model = Model(targets=np.mgrid[30:81:5, 30:81:5].reshape(2, -1).T)
# model = Model()
# model = Model(postsynapticcells=[PostSynapticCell(1, size=100, origin=np.asarray(o)) for o in
#                                 np.mgrid[50:60:2, 50:60:2].reshape(2, -1).T])
for i in range(601):
    if i % 50 == 0:
        model.iterate(plot_overview_to_disk=True)
    elif i % 10 == 0:
        model.iterate(write_to_disk=False, plot_model_axons_to_disk=True)
    else:
        model.iterate(write_to_disk=False)
    info = info.append(pd.Series({
        "PSC Mapping Score": model.postsynapticcell_mapping_score,
        "Average Segments Per Axon": np.average(np.asarray([len(x.segments) for x in model.axons]))
    }, name=i))
    info.to_csv("models/" + model.timestamp + "/info.csv")

sns.set_style("ticks")

df = pd.read_csv("models/" + model.timestamp + "/info.csv", index_col=0)
fig, axes = plt.subplots(1, len(df.columns), figsize=(10, 5))
for i in range(len(df.columns)):
    df[df.columns[i]].plot(ax=axes[i])
    axes[i].set_title(df.columns[i])
sns.despine(offset=5)
plt.tight_layout()
plt.savefig("models/" + model.timestamp + "/evolution-info.pdf")
