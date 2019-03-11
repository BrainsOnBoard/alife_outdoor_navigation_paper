import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.colors import ListedColormap
from os import path
from sys import argv

import plot_utils

def plot_diff(diff, cmap, filename, subtitle):
    fig, axis = plt.subplots(figsize=(plot_utils.column_width, (plot_utils.column_width / diff.shape[1]) * diff.shape[0]))

    axis.imshow(diff, interpolation="none", cmap=cmap)

    axis.grid(False)
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    axis.set_title(subtitle, loc="left", pad=-8.0)
    sns.despine(ax=axis, left=True, bottom=True)

    fig.tight_layout(pad=0)

    if not plot_utils.presentation:
        fig.savefig(filename, dpi=300)

def plot_comparison(grid_filename1, image_filename1, roll1, output_filename1,
                    grid_filename2, image_filename2, roll2, output_filename2):
    # Load grid images
    grid_image1 = cv2.imread(grid_filename1, cv2.IMREAD_GRAYSCALE)
    assert grid_image1 is not None
    grid_image2 = cv2.imread(grid_filename2, cv2.IMREAD_GRAYSCALE)
    assert grid_image2 is not None

    # Load route images
    route1_image = cv2.imread(image_filename1, cv2.IMREAD_GRAYSCALE)
    assert route1_image is not None
    route2_image = cv2.imread(image_filename2, cv2.IMREAD_GRAYSCALE)
    assert route2_image is not None

    # Create rolled versions of grid images
    grid_roll1 = np.roll(grid_image1, roll1, axis=1)
    grid_roll2 = np.roll(grid_image2, roll2, axis=1)

    # Calculate difference images
    diff1 = np.subtract(grid_roll1, route1_image, dtype=np.int32)
    diff2 = np.subtract(grid_roll2, route2_image, dtype=np.int32)

    # Build a suitable colour map
    cmap = ListedColormap(sns.color_palette("RdBu", 256))

    # Plot difference images
    plot_diff(diff1, cmap, output_filename1, "B")
    plot_diff(diff2, cmap, output_filename2, "C")

# Check we only get a single argument
assert len(argv) == 2

grid_filename = path.join(argv[1], "image_grids", "mid_day", "mask", "200_240_mask.png")
plot_comparison(grid_filename, path.join(argv[1], "routes", "route5", "mask", "unwrapped_180_mask.png"), -51 * 6, "../figures/image_diff_bad.png",
                grid_filename, path.join(argv[1], "routes", "route5", "mask", "unwrapped_1055_mask.png"), -5 * 6, "../figures/image_diff_good.png")

plot_comparison(path.join(argv[1], "image_grids", "mid_day", "unwrapped", "160_240.jpg"), path.join(argv[1], "routes", "route3", "unwrapped", "unwrapped_727.jpg"), -81 * 6, "../figures/route3_unwrapped_image_diff.png",
                path.join(argv[1], "image_grids", "mid_day", "mask", "160_240_mask.png"), path.join(argv[1], "routes", "route3", "mask", "unwrapped_1006_mask.png"), -61 * 6, "../figures/route3_mask_image_diff.png")


plt.show()
