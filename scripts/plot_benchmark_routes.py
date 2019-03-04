import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import read_csv

import plot_utils

sns.set(context="paper")
sns.set_style("whitegrid", {"font.family":"serif", "font.serif":"Times New Roman"})

data = read_csv("benchmark_results/output.csv", delimiter=",", skipinitialspace=True,
                converters={"RMSE":lambda s: float(s[:-4])})


# Filter out skymask and horizon (which we don't care about)
data = data.query("(variant != 'skymask') and (variant != 'horizon')")

# Group data by route
bars = data.groupby(["Route name"])

# Loop through groups
data = []
for n, d in bars:
    data.extend((n, "%s\n%s" % (m, v), r)
                for m, v, r in zip(d["memory type"].values, d["variant"].values, d["RMSE"].values))

fig, axis = plt.subplots(figsize=(plot_utils.double_column_width, 3.0),
                         frameon=False)
axis.set_ylabel("RMSE [degrees]")

plot_utils.plot_grouped_bars(data, 8, fig, axis, num_legend_col=4)
if not plot_utils.presentation:
    fig.savefig("../figures/route_benchmark.eps")
plt.show()
