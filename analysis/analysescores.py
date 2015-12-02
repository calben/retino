import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("average-points-error.csv")
fig = plt.figure()
df.mean(axis=1).plot()
plt.savefig("average-points-error.pdf")
