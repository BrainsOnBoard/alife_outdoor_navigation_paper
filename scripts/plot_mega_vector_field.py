import matplotlib.pyplot as plt
import seaborn as sns
import plot_utils

from os import path
from sys import argv,float_info

from plot_vector_field import plot_vector_field

# Check we have a seingle argument
assert len(argv) == 2

# Read path to routes from first argument
route_path = argv[1]

# List of output CSV paths to plot for figure
output_csv_paths = ["benchmark_results/output_route3_PerfectMemory_mask.csv",
                    "benchmark_results/output_route5_PerfectMemory_mask.csv",
                    "benchmark_results/output_route5_PerfectMemoryConstrained_mask.csv",
                    "benchmark_results/output_route5_InfoMaxConstrained_mask.csv"]
# Create column-width figure
fig, axes = plt.subplots(1, len(output_csv_paths), figsize=(plot_utils.double_column_width, 2.5), sharey=True)

# Create suitable palette
colours = sns.color_palette(n_colors=5)

highlighted_arrows = [([(480.0, 720.0)], 3),
                      ([(600.0, 720.0)], 3),
                      ([(600.0, 720.0)], 3),
                      None]
# Loop through all axes, data
min_x = float_info.max
max_x = -float_info.max
min_y = float_info.max
max_y = -float_info.max
for i, (a, p, h) in enumerate(zip(axes, output_csv_paths, highlighted_arrows)):
    # Plot vector field
    data_range = plot_vector_field(p, route_path, a, colours, shared_axes=True, highlighted_arrows=h)[3]

    # Set title
    a.set_title(chr(ord("A") + i), loc="left")

    # Update bounds
    min_x = min(min_x, data_range[0])
    max_x = max(max_x, data_range[1])
    min_y = min(min_y, data_range[2])
    max_y = max(max_y, data_range[3])

cross_kwargs = {"s": 60, "marker": "x", "linewidths": 0.1, "color": colours[3], "zorder": 0, "edgecolors": "none"}

# Add crosses marking locations at which further analysis is performed
#axes[0].scatter([480.0], [720.0], **cross_kwargs)
#axes[1].scatter([600.0], [720.0], **cross_kwargs)
#axes[2].scatter([600.0], [720.0], **cross_kwargs)

# Apply bounds to all axes
for a in axes:
    a.set_xlim((min_x, max_x))
    a.set_ylim((min_y, max_y))

# Add y axis label to first plot
axes[0].set_ylabel("Y [cm]")

fig.tight_layout(pad=0)
if not plot_utils.presentation:
    fig.savefig("../figures/vector_field.eps")
plt.show()
