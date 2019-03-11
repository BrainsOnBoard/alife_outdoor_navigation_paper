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
colours = sns.color_palette(n_colors=8)

highlighted_arrows = [[(480.0, 720.0, 3)],
                      [(600.0, 720.0, 3)],
                      [(600.0, 720.0, 3)],
                      []]
highlighted_snapshots = [[],
                         [(180, 153.0, 6)],
                         [(1055, 15.0, 6)],
                         []]

# Loop through all axes, data
min_x = float_info.max
max_x = -float_info.max
min_y = float_info.max
max_y = -float_info.max
for i, (a, p, h, s) in enumerate(zip(axes, output_csv_paths, highlighted_arrows, highlighted_snapshots)):
    # Plot vector field
    data_range = plot_vector_field(p, route_path, a, colours,
                                   shared_axes=True, highlighted_arrows=h, highlighted_snapshots=s)[3]

    # Set title
    a.set_title(chr(ord("A") + i), loc="left")

    # Update bounds
    min_x = min(min_x, data_range[0])
    max_x = max(max_x, data_range[1])
    min_y = min(min_y, data_range[2])
    max_y = max(max_y, data_range[3])

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
