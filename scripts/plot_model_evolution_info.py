import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

sns.set_style("ticks")

dfs = [pd.read_csv("models/" + x + "/info.csv", index_col=0) for x in
       ["16-03-04 02-15-14", "16-03-04 02-15-18"]]
print([df for df in dfs])
for i in range(len(dfs[0].columns)):
    fix, ax = plt.subplots(1, figsize=[5, 5])
    col = dfs[0].columns[i]
    print("Plotting", col)
    sns.tsplot([df[col] for df in dfs], ax=ax)
    ax.set_title(col)
    sns.despine(offset=5)
    plt.tight_layout()
    plt.savefig("figs/" + col + ".pdf")
