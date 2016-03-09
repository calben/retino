import pickle
import pandas as pd
import sys
from retino.utils import *
from retino.plot import *

sys.setrecursionlimit(1500)

info = pd.DataFrame({"PSC Mapping Score": []})
info.index.name = "Iteration"

# model = Model(targets=[np.asarray([60.0, 50.0])])
with open("models/16-03-08 15-40-17/100.pickle", "rb") as f:
    model = pickle.load(f)
model.timestamp += "-activity"
# model = Model(postsynapticcells=[PostSynapticCell(1, size=100, origin=np.asarray([50.0, 50.0]))])
for i in range(101):
    activities_df = pd.DataFrame(0, index=np.arange(100), columns=np.arange(100))
    activities_df.ix[(5 * i) % 100: (5 * i + 10) % 100] = 1
    if i % 50 == 0:
        model.iterate(write_to_disk=True, plot_overview_to_disk=True,
                      activities_df=activities_df)
    else:
        model.iterate(write_to_disk=False, plot_model_axons_to_disk=False, activities_df=activities_df)
    if i % 5 == 0:
        plot_model_activity_summary(model,  "models/" + model.timestamp + "/" + str(i) + "-activitysummary.png")
    # else:
    #     activities_df = pd.DataFrame(0, index=np.arange(100), columns=np.arange(100))
    #     activities_df.ix[i - 5 % 1000:i + 5 % 1000] = 1
    #     model.iterate(plot_to_disk=True, activities_df=activities_df)
    #     model.iterate(write_to_disk=False)
    info = info.append(pd.Series({"PSC Mapping Score": model.postsynapticcell_mapping_score}, name=i))
    info.to_csv("models/" + model.timestamp + "/info.csv")
