import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from glob import glob
from os import path
from sys import argv

from route import load_route
import plot_utils

# Check we have a seingle argument
assert len(argv) == 2
route_path = argv[1]

fig, axis = plt.subplots(figsize=(plot_utils.column_width * 0.5, 2.5))
axis.set_aspect("equal", "box")

# Loop through routes
actors = []
for r in glob(path.join(route_path, "*")):
    # Load route
    _, remaining_coords = load_route(path.join(route_path, path.basename(r)))

    actors.append(axis.plot(remaining_coords[:,0], remaining_coords[:,1])[0])

axis.set_xlabel("X [cm]")
axis.set_ylabel("Y [cm]")

 # Create single-column figure

axis.xaxis.grid(False)
axis.yaxis.grid(False)
sns.despine(ax=axis)

fig.legend(actors, [str(i + 1) for i, _ in enumerate(actors)],
           loc="upper right", ncol=1, frameon=False, borderpad=0.0)

fig.tight_layout(pad=0, rect=[0.1, 0.0, 1.0, 1.0])
if not plot_utils.presentation:
    fig.savefig("../figures/routes.eps")
plt.show()
