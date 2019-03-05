import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sys import argv

import plot_utils

ridf_data = np.loadtxt("aliasing_data.csv", delimiter=",", skiprows=1,
                       converters={1: lambda s: float(s[:-3])},
                       dtype={"names": ("pixel", "rotation", "familiarity"),
                              "formats": (np.int, np.float, np.float)})

# Sort data by angle (so lines don't mess up)
ridf_data = ridf_data[np.argsort(ridf_data["rotation"])]

#familiarity_order = np.argsort(ridf_data["familiarity"])
#print(ridf_data["rotation"][familiarity_order][:10])

# Scale down familiarity
ridf_data["familiarity"] /= 255.0
fig, axis = plt.subplots(figsize=(plot_utils.column_width, 2.0))

axis.plot(ridf_data["rotation"], ridf_data["familiarity"])

axis.axvline(153, linestyle="--", color="gray")
axis.axvline(15, linestyle="--", color="gray")

axis.set_xlabel("Rotation [degrees]")
axis.set_ylabel("Image difference")
axis.set_xticks([-180, -90, 0, 90, 180])
plot_utils.remove_axis_junk(axis)

fig.tight_layout(pad=0)

if not plot_utils.presentation:
    fig.savefig("../figures/alias_ridf.eps")
plt.show()