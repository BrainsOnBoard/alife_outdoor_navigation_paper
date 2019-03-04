import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.colors import ListedColormap
from os import path
from sys import argv

import plot_utils

def plot_diff(diff, cmap, filename):
    fig, axis = plt.subplots(figsize=(plot_utils.column_width, (plot_utils.column_width / diff.shape[1]) * diff.shape[0]))

    axis.imshow(diff, interpolation="none", cmap=cmap)

    axis.grid(False)
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)

    fig.tight_layout(pad=0)

    if not plot_utils.presentation:
        fig.savefig(filename, dpi=300)

# Check we only get a single argument
assert len(argv) == 2

# Load grid image
grid_image = cv2.imread(path.join(argv[1], "image_grids", "mid_day", "mask", "200_240_mask.png"), cv2.IMREAD_GRAYSCALE)
assert grid_image is not None

route_good = cv2.imread(path.join(argv[1], "routes", "route5", "mask", "unwrapped_1055_mask.png"), cv2.IMREAD_GRAYSCALE)
assert route_good is not None

route_bad = cv2.imread(path.join(argv[1], "routes", "route5", "mask", "unwrapped_180_mask.png"), cv2.IMREAD_GRAYSCALE)
assert route_bad is not None

grid_roll_good = np.roll(grid_image, -5 * 6, axis=1)

grid_roll_bad = np.roll(grid_image, -51 * 6, axis=1)

diff_good = cv2.absdiff(grid_roll_good, route_good)
diff_bad = cv2.absdiff(grid_roll_bad, route_bad)

cmap = ListedColormap(sns.color_palette("Reds", 256))

plot_diff(diff_good, cmap, "../figures/image_diff_good.png")
plot_diff(diff_bad, cmap, "../figures/image_diff_bad.png")

plt.show()
