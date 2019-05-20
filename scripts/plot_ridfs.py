import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sys import argv

import plot_utils

def load_ridf_data(csv_filename, scale_familiarity):
    ridf_data = np.loadtxt(csv_filename, delimiter=",", skiprows=1,
                        converters={1: lambda s: float(s[:-3])},
                        dtype={"names": ("pixel", "rotation", "familiarity"),
                                "formats": (np.int, np.float, np.float)})

    # Sort data by angle (so lines don't mess up)
    ridf_data = ridf_data[np.argsort(ridf_data["rotation"])]

    # Scale down familiarity
    if scale_familiarity:
        ridf_data["familiarity"] /= 255.0

    return ridf_data

def plot_ridf(ridf_csv_filename, ridf2_csv_filename=None, ridf2_infomax=False):
    ridf_data = load_ridf_data(ridf_csv_filename, True)

    if ridf2_csv_filename is not None:
        ridf2_data = load_ridf_data(ridf2_csv_filename, not ridf2_infomax)

    colours = sns.color_palette(n_colors=2)

    fig, axis = plt.subplots(figsize=(plot_utils.column_width, 2.0))

    actors = [axis.plot(ridf_data["rotation"], ridf_data["familiarity"], color=colours[0])[0]]
    axis.set_xlabel("Rotation [degrees]")
    axis.set_ylabel("Image difference")
    plot_utils.remove_axis_junk(axis, not ridf2_infomax)

    if ridf2_csv_filename is not None:
        if ridf2_infomax:
            ridf2_axis = axis.twinx()
            actors.append(ridf2_axis.plot(ridf2_data["rotation"], ridf2_data["familiarity"], color=colours[1])[0])
            ridf2_axis.set_ylabel("Familiarity")
            plot_utils.remove_axis_junk(ridf2_axis)
        else:
            actors.append(axis.plot(ridf2_data["rotation"], ridf2_data["familiarity"], color=colours[1])[0])

    axis.set_xticks([-180, -90, 0, 90, 180])

    return fig, axis, actors

# Plot RIDF with aliasing
alias_ridf_fig, alias_ridf_axis, _ = plot_ridf("aliasing_data.csv")
alias_ridf_axis.axvline(153, linestyle="--", color="gray")
alias_ridf_axis.axvline(15, linestyle="--", color="gray")
alias_ridf_axis.set_title("A", loc="left")
alias_ridf_fig.tight_layout(pad=0, rect=[0.0, 0.175, 1.0, 1.0])

# Plot good RIDF and RFF
good_ridf_fig, _, good_ridf_actors = plot_ridf("good_ridf_data.csv", "good_rff_data.csv", True)
good_ridf_fig.legend(good_ridf_actors, ["Perfect Memory", "Infomax"], ncol=2, loc="lower center", frameon=False)
good_ridf_fig.tight_layout(pad=0, rect=[0.0, 0.175, 1.0, 1.0])

route3_fig, route3_axis, route3_actors = plot_ridf("route3_unwrapped_data.csv", "route3_mask_data.csv")
route3_axis.set_title("A", loc="left")
route3_fig.legend(route3_actors, ["Raw image", "Binary image"], ncol=2, loc="lower center", frameon=False)
route3_fig.tight_layout(pad=0, rect=[0.0, 0.175, 1.0, 1.0])

if not plot_utils.presentation:
    good_ridf_fig.savefig("../figures/good_ridf.eps")
    alias_ridf_fig.savefig("../figures/alias_ridf.eps")
    route3_fig.savefig("../figures/route3_ridf.eps")
plt.show()
