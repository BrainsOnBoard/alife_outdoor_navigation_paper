import matplotlib.pyplot as plt
import seaborn as sns
import plot_utils

from os import path
from sys import argv,float_info

from plot_vector_field import plot_vector_field

# Check we have at least two arguments
assert len(argv) >= 3

# Read path to routes from first argument
route_path = argv[1]

# Read output csv paths from remaining arguments
output_csv_paths = argv[2:]

# Create column-width figure
fig, axes = plt.subplots(1, len(output_csv_paths), figsize=(plot_utils.double_column_width, 2.5), sharey=True)


# Loop through all axes, data
min_x = float_info.max
max_x = -float_info.max
min_y = float_info.max
max_y = -float_info.max
for i, (a, p) in enumerate(zip(axes, output_csv_paths)):
    # Plot vector field
    data_range = plot_vector_field(p, route_path, a, shared_axes=True)[3]

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
