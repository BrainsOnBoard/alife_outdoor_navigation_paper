import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from collections import defaultdict
from glob import glob
from os import path
from pandas import read_csv
from scipy.stats import iqr

import plot_utils

#route_data = defaultdict(dict)
route_data = []
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

    errors = np.abs(errors)
    # C
    variant = "%s\n%s" % (memory, image_input)
    route_data.append((route_name, variant, np.median(errors), np.std(errors)))


fig, axis = plt.subplots(figsize=(plot_utils.double_column_width, 3.0),
                         frameon=False)
axis.set_ylabel("RMSE [degrees]")

plot_utils.plot_grouped_bars(route_data, 8, fig, axis, num_legend_col=4, legend_pad=0.3)
if not plot_utils.presentation:
    fig.savefig("../figures/route_benchmark.eps")
plt.show()
