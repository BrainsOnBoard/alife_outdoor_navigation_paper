import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from collections import defaultdict
from glob import glob
from os import path
from pandas import read_csv
from scipy.stats import iqr

import plot_utils

# Loop through output files from benchmark
data = None
for r in sorted(glob("benchmark_results/output_*.csv")):
    # Split result path into directory and file title
    output_dir, output_filename = path.split(r)
    output_title = path.splitext(output_filename)[0]

    # Split result file title into pre-defined components
    _, route_name, memory, image_input = output_title.split("_")

    # Skip image inputs we're not discussing
    if image_input == "horizon" or image_input == "skymask":
        continue

    # Read error
    errors = np.loadtxt(r, delimiter=",", skiprows=1, usecols=3,
                         converters={3: lambda s: float(s[:-3])},
                         dtype=np.float)

    # Build compound numpy array from this
    frame = np.empty(errors.shape, dtype={"names": ["route_name", "variant", "error"],
                                          "formats": ["U64", "U64", np.float]})
    frame["route_name"][:] = route_name
    frame["variant"][:] = "%s\n%s" % (memory, image_input)
    frame["error"][:] = np.abs(errors)

    # If there's existing data stack on top
    if data is None:
        data = frame
    else:
        data = np.hstack((data, frame))


fig, axis = plt.subplots(figsize=(plot_utils.double_column_width, 3.0),
                         frameon=False)
axis.set_ylabel("Absolute angular error\n[degrees]")

sns.boxplot(x=data["route_name"], y=data["error"], hue=data["variant"],
            ax=axis, saturation=1.0, linewidth=1.0)

# **HACK** remove unwanted AXIS legend
axis.get_legend().remove()

# Add in figure legend
fig.legend(loc="lower center", ncol=4)

# Set tight layout and save
fig.tight_layout(pad=0, rect=[0.0, 0.3, 1.0, 1.0])

if not plot_utils.presentation:
    fig.savefig("../figures/route_benchmark.eps")
plt.show()
