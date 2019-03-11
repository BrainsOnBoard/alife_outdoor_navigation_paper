import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from os import path
from sys import argv

from route import load_route
import plot_utils

def plot_vector_field(output_csv_path, route_path, axis, cmap, highlighted_arrows=None, shared_axes=False):
    # Read output
    output_data = np.loadtxt(output_csv_path, delimiter=",", skiprows=1, usecols=(0, 1, 2),
                            converters={0: lambda s: float(s[:-3]),
                                        1: lambda s: float(s[:-3]),
                                        2: lambda s: float(s[:-4])},
                            dtype={"names": ("x", "y", "best_heading"),
                                    "formats": (np.float, np.float, np.float)})

    # Split input path into directory and file title
    output_dir, output_filename = path.split(output_csv_path)
    output_title = path.splitext(output_filename)[0]

    # Split output file title into pre-defined components
    _, route_name, memory, image_input = output_title.split("_")

    # Load route
    coords, remaining_coords = load_route(path.join(route_path, route_name), image_input)


    # Create single-column figure

    axis.set_aspect("equal", "box")

    data_range = (np.amin(output_data["x"]), np.amax(output_data["x"]),
                  np.amin(output_data["y"]), np.amax(output_data["y"]))
    if not shared_axes:
        # Set axis range to match that of grid
        axis.set_xlim(data_range[:2])
        axis.set_ylim(data_range[2:])

        axis.set_ylabel("Y [cm]")

    axis.set_xlabel("X [cm]")

    axis.xaxis.grid(False)
    axis.yaxis.grid(False)

    # Create (initially all false) mask to select highlighted arrows
    highlight_mask = np.zeros(len(output_data), dtype=bool)
    non_highlight_mask = np.ones(len(output_data), dtype=bool)

    # If any highlighted arrows are specified
    if highlighted_arrows is not None:
        # Loop through their coordinates
        for (x, y) in highlighted_arrows[0]:
            # Build mask to select coordinates
            mask = (output_data["x"] == x) & (output_data["y"] == y)
            assert np.sum(mask) == 1

            # Or mask with highlight mask
            highlight_mask = np.logical_or(highlight_mask, mask)

        # Build NON highlight mask
        non_highlight_mask  = np.logical_not(highlight_mask)

    # Plot quivers showing vector field
    heading_radians = np.radians(output_data["best_heading"])
    u = np.cos(heading_radians)
    v = np.sin(heading_radians)


    axis.quiver(output_data["x"][non_highlight_mask], output_data["y"][non_highlight_mask],
                u[non_highlight_mask], v[non_highlight_mask],
                angles="xy", zorder=5)

    if highlighted_arrows is not None:
        axis.quiver(output_data["x"][highlight_mask], output_data["y"][highlight_mask],
                    u[highlight_mask], v[highlight_mask],
                    angles="xy", zorder=5, scale=10.0, width=0.015, color=cmap[highlighted_arrows[1]])

    # Plot route data
    axis.plot(coords[:,0], coords[:,1], zorder=1, color=cmap[1])
    axis.plot(remaining_coords[:,0], remaining_coords[:,1], zorder=3, color=cmap[0])

    first_x = remaining_coords[0, 0]
    first_y = remaining_coords[0, 1]
    dir_x = remaining_coords[1, 0] - first_x
    dir_y = remaining_coords[1, 1] - first_y
    scale = 100.0 / np.sqrt((dir_x * dir_x) + (dir_y * dir_y))
    dir_x *= scale
    dir_y *= scale
    axis.arrow(first_x - dir_x, first_y - dir_y, dir_x, dir_y,
            color=cmap[2], length_includes_head=True, head_width=30.0, zorder=7)

    return route_name, memory, image_input, data_range


if __name__ == "__main__":
    # Check we have at least a single argument
    assert len(argv) >= 2

    output_csv_path = argv[1]
    route_path = argv[2] if (len(argv) >= 3) else "routes"

    # Create column-width figure
    fig, axis = plt.subplots(figsize=(plot_utils.double_column_width * 0.25, 3.0))

    # Configure palette
    colours = sns.color_palette(n_colors=3)

    # Plot vector field
    route_name, memory, image_input = plot_vector_field(output_csv_path, route_path, axis, colours)[:3]

    fig.tight_layout(pad=0)
    if not plot_utils.presentation:
        fig.savefig("../figures/vector_field_" + route_name + "_" + memory + "_" + image_input + ".eps")
    plt.show()
