import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sys import argv

import plot_utils

def load_ridf_data(csv_filename):
    ridf_data = np.loadtxt(csv_filename, delimiter=",", skiprows=1,
                        converters={1: lambda s: float(s[:-3])},
                        dtype={"names": ("pixel", "rotation", "familiarity"),
                                "formats": (np.int, np.float, np.float)})

    # Sort data by angle (so lines don't mess up)
    return ridf_data[np.argsort(ridf_data["rotation"])]

def plot_ridf(ridf_csv_filename, rff_csv_filename=None):
    ridf_data = load_ridf_data(ridf_csv_filename)

    if rff_csv_filename is not None:
        rff_data = load_ridf_data(rff_csv_filename)

    colours = sns.color_palette(n_colors=2)

    # Scale down familiarity
    ridf_data["familiarity"] /= 255.0
    fig, axis = plt.subplots(figsize=(plot_utils.column_width, 2.0))

    actors = [axis.plot(ridf_data["rotation"], ridf_data["familiarity"], color=colours[0])[0]]
    axis.set_xlabel("Rotation [degrees]")
    axis.set_ylabel("Image difference")
    plot_utils.remove_axis_junk(axis, rff_csv_filename is None)

    if rff_csv_filename is not None:
        rff_axis = axis.twinx()
        actors.append(rff_axis.plot(rff_data["rotation"], rff_data["familiarity"], color=colours[1])[0])

        rff_axis.set_ylabel("Familiarity")
        plot_utils.remove_axis_junk(rff_axis)

    #axis.set_ylim((0.0, np.amax(ridf_data["familiarity"])))
    axis.set_xticks([-180, -90, 0, 90, 180])

    return fig, axis, actors

# Plot RIDF with aliasing
alias_ridf_fig, alias_ridf_axis, _ = plot_ridf("aliasing_data.csv")
alias_ridf_axis.axvline(153, linestyle="--", color="gray")
alias_ridf_axis.axvline(15, linestyle="--", color="gray")
alias_ridf_fig.tight_layout(pad=0)

# Plot good RIDF and RFF
good_ridf_fig, _, good_ridf_actors = plot_ridf("good_ridf_data.csv", "good_rff_data.csv")
good_ridf_fig.legend(good_ridf_actors, ["Perfect memory", "InfoMax"], ncol=2, loc="lower center")
good_ridf_fig.tight_layout(pad=0, rect=[0.0, 0.175, 1.0, 1.0])

if not plot_utils.presentation:
    good_ridf_fig.savefig("../figures/good_ridf.eps")
    alias_ridf_fig.savefig("../figures/alias_ridf.eps")
plt.show()
